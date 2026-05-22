"""
URL configuration for UPproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from upapp import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('account/', views.account, name='account'),

    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('employee-panel/', views.employee_panel, name='employee_panel'),
    path('courier-panel/', views.courier_panel, name='courier_panel'),

    path('clients/', views.clients_data, name='clients_data'),
    path('couriers/', views.couriers_data, name='couriers_data'),
    path('employees/', views.employees_data, name='employees_data'),
    path('restaurants/', views.restaurants_data, name='restaurants_data'),
    path('menu-edit/', views.menu_edit, name='menu_edit'),
    path('orders-edit/', views.orders_edit, name='orders_edit'),

]