from django.contrib import admin
from django.urls import path

from.views import base_page_view
from.views import index_page_view
from.views import login_page_view
from.views import ragistration_page_view

urlpatterns = [
    path('',base_page_view,name='base_page_view'),
    path('index/',index_page_view,name='index_page_view'),
    path('login/',login_page_view,name='login_page_view'),
    path('ragistration/',ragistration_page_view,name='ragistration_page_view'),
]