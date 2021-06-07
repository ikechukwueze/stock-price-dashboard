
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

django.setup()

from requests import get

from django.contrib.auth import get_user_model

from stockanalytics.models import eod_stock_price

from stockanalytics.views import api_key

from django.contrib.auth import get_user_model






def daily_update():

	print('testing')
	"""
	all_users = get_user_model().objects.all()

	#print(all_users)

	for user_object in all_users:

		print(user_object)

		if eod_stock_price.objects.filter(user=user_object).exists():

			user_tickers = list(eod_stock_price.objects.filter(user=user_object).values_list('ticker', flat=True).distinct())

			#print(user_tickers)

			for ticker in user_tickers:

				try:
					url = 'http://api.marketstack.com/v1/eod/latest?access_key={}&symbols={}'.format(api_key, ticker)
					
					api_response = get(url).json()

					#print('data gotten from api')

					data = api_response['data']
					
					for s in data:
						stock_data = eod_stock_price()

						if not eod_stock_price.objects.filter(user=user_object, ticker=s['symbol'], date=s['date'].split('T')[0]).exists():
							stock_data.high = s['high']
							stock_data.low = s['low']
							stock_data.opening_price = s['open']
							stock_data.closing_price = s['close']
							stock_data.date = s['date'].split('T')[0]
							stock_data.ticker = s['symbol']
							stock_data.user = user_object

							stock_data.save()

					#print('success!!')
								
				except:
					pass
				"""