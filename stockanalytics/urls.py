from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name="dashboard_page"),
    path('login', views.login_page, name="login"),
    path('register', views.register_page),
    path("logout", views.logout_request, name= "logout"),
    path("filter_chart", views.filter_chart, name="filter_chart"),
    path("add_stock", views.add_stock),
    path("delete_stocks", views.delete_stocks),
    path("export_data", views.export_data),
    path("refresh", views.refresh_stock_price),
    
]