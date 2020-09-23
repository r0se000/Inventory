"""manageproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
import manageapp.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', manageapp.views.input, name='input'),
    path('inputadd/', manageapp.views.input_add, name='input_add'),
    path('output/', manageapp.views.output, name='output'),
    path('outputadd/', manageapp.views.output_add, name='output_add'),
    path('search/', manageapp.views.search, name='search'),
    path('search_date/', manageapp.views.search_date, name='search_date'),
    path('dsearch_result/', manageapp.views.dsearch_result, name='dsearch_result'),
    path('psearch_result/', manageapp.views.psearch_result, name='psearch_result'),
    path('delete/', manageapp.views.delete, name='delete'),
    path('delete_result/', manageapp.views.delete_result, name='delete_result'),
    path('delete_ok/', manageapp.views.delete_ok, name='delete_ok'),
]
