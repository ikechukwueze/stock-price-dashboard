from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import fields
from stockanalytics.models import eod_stock_price, intraday_stock_price, stock_ticker


from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget



### One time import of stock symbols and company data

class stock_ticker_resources(resources.ModelResource):
    class Meta:
        model = stock_ticker
        import_id_fields = ('stock_symbol',)
        fields = ('company_name', 'stock_symbol', 'country', 'ipo_year', 'sector', 'industry')
        #exclude = ('id',)
        


class stock_ticker_importexport_admin(ImportExportModelAdmin):
    resource_class = stock_ticker_resources



class eod_stock_price_resources(resources.ModelResource):

    #ticker_foreignkey = fields.Field(column_name='ticker', attribute='ticker', widget=ForeignKeyWidget(stock_ticker, 'stock_symbol'))

    class Meta:
        model = eod_stock_price
        #fields = ('ticker', 'opening_price', 'closing_price', 'high', 'low', 'date',)
        #exclude = ('id',)


class eod_stock_price_importexport_admin(ImportExportModelAdmin):
    resource_class = eod_stock_price_resources




class stock_ticker_customize_admin(UserAdmin):
    list_display = ('stock_symbol', 'company_name',)
    search_fields = ('company_name', 'stock_symbol',)
    ordering = ('stock_symbol',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()



class eod_customize_admin(UserAdmin):
    list_display = ('ticker', 'opening_price', 'closing_price', 'high', 'low', 'date',)
    search_fields = ('ticker',)
    ordering = ('date',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()






#class eod_admin(UserAdmin):
#    list_display = ('ticker.stock_symbol')
#    search_fields = ('ticker.stock_symbol')



# Register your models here.
admin.site.register(stock_ticker, stock_ticker_importexport_admin)#stock_ticker_customize_admin)
admin.site.register(eod_stock_price)#, eod_customize_admin)#eod_stock_price_importexport_admin)
admin.site.register(intraday_stock_price)






