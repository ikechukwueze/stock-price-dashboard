
from django.db.models.functions.datetime import TruncMonth
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from requests.api import request
from .models import eod_stock_price, stock_ticker, intraday_stock_price

from decimal import Decimal

from django.http import JsonResponse
import datetime

#from .models import eod_stock_price
from django.db.models import Avg

from django.contrib.auth.decorators import login_required
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages #import messages
from django.contrib.auth.forms import AuthenticationForm #add this


from djqscsv import render_to_csv_response

# Create your views here.


api_key = '808a4a6d2e2eff1e4ec4a91be5a03807'
#api_key = '4C3TN4PJPEIT9AW0'
#https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&outputsize=full&apikey=key
from requests import get


@login_required(login_url='/login')
def dashboard(request):
	

	stock_symbols = stock_ticker.objects.all()

	context = {'stock_symbols':stock_symbols}
	context['user_data'] = []

	user_tickers = list(eod_stock_price.objects.filter(user=request.user).values_list('ticker', flat=True).distinct())
	#print(user_tickers)

	i = 0
	


	for ticker in user_tickers:
		d = eod_stock_price.objects.filter(user=request.user, ticker=ticker, date__gt=datetime.date(2019, 12, 31)).annotate(month=TruncMonth("date"))
		
		#convert datetime.date to string
		graph_labels = [stock.date.strftime('%m-%d-%Y') for stock in d.order_by('date')]
		graph_data = [float(stock.closing_price) for stock in d.order_by('date')]

		barchart_queryset = d.values('month').annotate(avg_price=Avg('closing_price'))
	
		barchart_labels = [m['month'].strftime('%m-%d-%Y') for m in barchart_queryset]
		barchart_data = [round(float(d['avg_price']), 2) for d in barchart_queryset]

		latest_data = intraday_stock_price.objects.filter(user=request.user, ticker=ticker).latest('datetime')
		latest_price = round(float(latest_data.price), 2)
		latest_time = datetime.datetime.strftime(latest_data.datetime, '%H:%M %m-%d-%Y')
		
		latest_data = {'price':latest_price, 'time':latest_time}
		
		
		c = {'name':ticker, 'id':i, 'latest_data': latest_data, 'graph_labels': graph_labels, 'graph_data' : graph_data, 'bar_labels': barchart_labels, 'bar_data': barchart_data }
		
		context['user_data'].append(c)
		i=i+1
	
	
	return render(request, 'stockanalytics/index.html', context)













def register_page(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("dashboard_page")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	
	form = NewUserForm
	#print(dir(form))
	return render(request, 'stockanalytics/register.html', {"register_form":form})




def login_page(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("dashboard_page")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request, 'stockanalytics/login.html', {"login_form":form})




def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("login")







def filter_chart(request):

	if request.is_ajax and request.method == "GET":
		start_date = request.GET['start_date']
		end_date = request.GET['end_date']
		selected = request.GET['selected']

		print(start_date, selected)

		#error = messages.error(request,"Invalid date")
		

		data = eod_stock_price.objects.filter(user=request.user, ticker=selected, date__range=[start_date, end_date]).annotate(month=TruncMonth("date"))
		#print(data)
		if len(data) == 0:
			return JsonResponse({'response':'error'})
		else:

			#convert datetime.date to string
			graph_labels = [stock.date.strftime('%m-%d-%Y') for stock in data.order_by('date')]
			graph_data = [float(stock.closing_price) for stock in data.order_by('date')]
			
			
			barchart_queryset = data.values('month').annotate(avg_price=Avg('closing_price'))
			
			barchart_labels = [m['month'].strftime('%m-%d-%Y') for m in barchart_queryset]
			barchart_data = [round(float(d['avg_price']), 2) for d in barchart_queryset]

			return JsonResponse({'response': {'name':selected, 'graph_labels': graph_labels, 'graph_data' : graph_data, 'bar_labels': barchart_labels, 'bar_data': barchart_data }}, status = 200)


		




def add_stock(request):
	if request.method == "POST":
		
		start_date = request.POST['start_date']
		#end_date = request.POST['end_date']
		ticker = request.POST['selected']

		if not eod_stock_price.objects.filter(user=request.user, ticker=ticker).exists():

			date_format = '%Y-%m-%d'
			today_datetime = datetime.datetime.today()
			start_date_datetime = datetime.datetime.strptime(start_date, date_format)
			#end_date_datetime = datetime.datetime.strptime(end_date, date_format)
			

			#if (start_date_datetime >= end_date_datetime) or (start_date_datetime > today_datetime):
			#	messages.error(request, 'Invalid dates.')
			#	return redirect('/')

			if start_date_datetime > today_datetime:
				messages.error(request, 'Invalid date.')
				return redirect('/')

			#if start_date_datetime < end_date_datetime > today_datetime:
			#	end_date = datetime.datetime.strftime(today_datetime, date_format)
			#print('date check passed')


			
			#url = 'http://api.marketstack.com/v1/eod?access_key={}&symbols={}&date_from={}&date_to={}&limit=1000'.format(api_key, ticker, start_date, end_date)
			
			url = 'http://api.marketstack.com/v1/eod?access_key={}&symbols={}&date_from={}&limit=1000'.format(api_key, ticker, start_date)

			print('data gotten from api')

			try:
				api_response = get(url).json()
				data = api_response['data']

				for s in data:
					stock_data = eod_stock_price()

					if not eod_stock_price.objects.filter(user=request.user, ticker=s['symbol'], date=s['date'].split('T')[0]).exists():
						#print('doesnt exist')
						stock_data.high = s['high']
						stock_data.low = s['low']
						stock_data.opening_price = s['open']
						stock_data.closing_price = s['close']
						stock_data.date = s['date'].split('T')[0]
						stock_data.ticker = s['symbol']
						stock_data.user = request.user
						

						stock_data.save()
						#print('saving stock data')

					"""
					try:
						print('doing a check')
						check = eod_stock_price.objects.get(user=request.user, ticker=s['symbol'], date=s['date'].split('T')[0])
						print('check failed', check.date)
					except:
						stock_data.high = s['high']
						stock_data.low = s['low']
						stock_data.opening_price = s['open']
						stock_data.closing_price = s['close']
						stock_data.date = s['date'].split('T')[0]
						stock_data.ticker = s['symbol']
						stock_data.user = request.user

						stock_data.save()
						#print(s['high'], 'saved')
					"""

				
				price_time = get_stock_price(ticker)
				print('printing price and time next')

				

				current_price = intraday_stock_price()
				current_price.ticker = ticker
				current_price.price = Decimal(price_time[0].replace("," , ""))
				current_price.datetime = price_time[1]
				current_price.user = request.user
				print('intra_day_save?')
				current_price.save()
				print('intra_day_savd')
				print(intraday_stock_price.objects.filter(user=request.user, ticker=ticker))

				messages.success(request, "Data successfully added.")
				
				return redirect('/')
			
			except:
				messages.error(request,"An error has occurred.")
				return redirect('/')
		
		else:
			messages.error(request,"Stock already exists")
			return redirect('/')


	return redirect('/')






def delete_stocks(request):
	if request.method == "POST":
		stock_records_to_delete = request.POST.getlist('check-box-item')
		#print(stock_record_to_delete)

		for stock in stock_records_to_delete:
			eod_stock_price.objects.filter(user=request.user, ticker=stock).delete()
			intraday_stock_price.objects.filter(user=request.user, ticker=stock).delete()

		return redirect('/')







def export_data(request):
	if request.method == "POST":
		stock_records_to_export = request.POST.getlist('check-box-item')
		print(stock_records_to_export)

		
		
		for stock in stock_records_to_export:
			data = eod_stock_price.objects.filter(user=request.user, ticker=stock).values('date', 'ticker', 'opening_price', 'closing_price', 'high', 'low')
			return render_to_csv_response(data, filename=stock)









def refresh_stock_price(request):
	user_tickers = list(eod_stock_price.objects.filter(user=request.user).values_list('ticker', flat=True).distinct())
	print(user_tickers)

	import time
	for ticker in user_tickers:
		price_time = get_stock_price(ticker)
		print(price_time)

		current_price = intraday_stock_price()
		current_price.ticker = ticker
		current_price.price = Decimal(price_time[0].replace("," , ""))
		current_price.datetime = price_time[1]
		current_price.user = request.user
		current_price.save()
		print(intraday_stock_price.objects.filter(ticker=ticker))

		time.sleep(0.5)

		
	return redirect('/')


















def get_stock_price(ticker):
	#cap_ticker = ticker.capitalize()
	from bs4 import BeautifulSoup as bs
	#from requests import get
	url = "https://finance.yahoo.com/quote/{}?p=PLUG&.tsrc=fin-srch".format(ticker)
	headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}


	try:
		page = get(url, headers=headers)
	except:
		return("Couldn't get price. Please check ticker")
	page_content = page.content
	soup = bs(page_content, features="html.parser")
	f = soup.findAll('span', attrs={'class':"Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"})[0]
	price = f.get_text()

	from datetime import datetime
	now = datetime.now()
	#t = datetime.strftime(now, '%H:%M %d-%m-%y')
	return [price, now]


