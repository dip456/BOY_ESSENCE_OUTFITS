from django.contrib import admin
from django.urls import path

from.views import base_page_view
from.views import login_page_view

urlpatterns = [
    path('',base_page_view,name='base_page_view'),
    path('login/',login_page_view,name='login_page_view')
]