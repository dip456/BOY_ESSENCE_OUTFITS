from django.contrib import admin
from django.urls import path

from .views import base_page_view
from .views import index_page_view
from .views import login_page_view
from .views import ragistration_page_view
from .views import contactus_page_view
from .views import about_page_view

urlpatterns = [
    path('base/',base_page_view,name='base_page_view'),
    path('',index_page_view,name='index_page_view'),
    path('login/',login_page_view,name='login_page_view'),
    path('ragistration/',ragistration_page_view,name='ragistration_page_view'),
    path('contact/',contactus_page_view,name='contactus_page_view'),
    path('about/',about_page_view,name='about_page_view'),
]