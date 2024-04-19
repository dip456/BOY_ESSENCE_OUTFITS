from django.shortcuts import render

# Create your views here.
def base_page_view(request):
    return render(request,'buyer/base.html')
