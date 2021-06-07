from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.conf import settings




# Create your models here.




class stock_ticker(models.Model):
    company_name = models.CharField(max_length=300, blank=False, null=False)
    stock_symbol = models.CharField(max_length=50, primary_key=True, blank=False)
    country = models.CharField(max_length=150, blank=True, null=True)
    ipo_year = models.SmallIntegerField(blank=True, null=True)
    sector = models.CharField(max_length=300, blank=True, null=True)
    industry = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.company_name




class eod_stock_price(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=50, blank=False, null=False)
    #ticker = models.ForeignKey(stock_ticker, on_delete=CASCADE)
    opening_price = models.DecimalField(max_digits=10, decimal_places=2)
    closing_price = models.DecimalField(max_digits=10, decimal_places=2)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return ('{} - {} - {}'.format(self.ticker, self.date, self.user.username))




class intraday_stock_price(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    ticker = models.CharField(max_length=50, blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.user.username







