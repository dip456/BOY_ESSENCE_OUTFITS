from django.shortcuts import render

# Create your views here.
def base_page_view(request):
    return render(request,'buyer/base.html')

def index_page_view(request):
    return render(request,'buyer/index.html')


def login_page_view(request):
    return render(request,'buyer/login.html')

def ragistration_page_view(request):
    return render(request,'buyer/ragistration.html')

def contactus_page_view(request):
    return render(request,'buyer/contact.html')

def about_page_view(request):
    return render(request,'buyer/about.html')
