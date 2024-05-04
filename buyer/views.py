from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.mail import send_mail


from authentication.models import MyCustomerModel
from master.utils.BOY_VALIDATORS.email_password import is_valid_email,is_valid_password
from master.utils.BOY_RANDOM.otp import generate_new_otp

import os




def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'Customer_id' not in request.session:
            messages.warning(request, "You are not logged in yet.")
            return redirect('login_page_view')
        return view_func(request, *args, **kwargs)
    return wrapper


# Create your views here.

def ragistration_page_view(request):
    if request.method == 'POST':
        email_ = request.POST['email']
        password_ = request.POST['password']
        confirm_password_= request.POST['confirm_password']

        if is_valid_email(email_):
            if password_ == confirm_password_:
                is_valid_passwd,msg = is_valid_password(password_)
                if is_valid_passwd:
                    otp_ = generate_new_otp(6)
                    my_Newcustomer = MyCustomerModel.objects.create(
                        email = email_,
                        password = password_,
                        otp = otp_
                    )
                    my_Newcustomer.save()
                    subject = 'Your One-Time Password (OTP) | BOY_ESSENCE_OUTFITS'
                    message = f"""
                    Dear Customer,

                    Your One-Time Password (OTP) to verify your account is: {otp_}. Please use this code to proceed with the verification process.

                    Thank you.
                    """
                    from_email = os.environ.get('EMAIL_HOST_USER')
                    recipient_list = [f'{email_}']
                    send_mail(subject, message, from_email, recipient_list)
                    context = {
                        'cum_email':email_
                    }
                    messages.warning(request, f"Please check your '{email_}' for the OTP. Enter the received OTP on this confirmation page to verify your email address.")
                    return render(request, 'buyer/otp_verify.html', context)
                else:
                    messages.warning(request, f"{msg}")
                    print(is_valid_password(password_))
                    return redirect('ragistration_page_view')
            else:
                messages.warning(request, "Password and confirm password does not match.")
                return redirect('ragistration_page_view')
        else:
            messages.warning(request, "Invalid Email.")
            return redirect('ragistration_page_view')
    return render(request,'buyer/ragistration.html')

def genrate_otp_page(request):
    if request.method == 'POST':
        email_ = request.POST['email']
        otp_ = request.POST['otp']
        if otp_.isdigit() and len(otp_) == 6:
            try:
                get_MyCustomer = MyCustomerModel.objects.get(email = email_)
            except MyCustomerModel.DoesNotExist:
                messages.warning(request, "User does not exist.")
                context = {
                    'cum_email': email_
                    }
                return render(request,'buyer/otp_verify',context)
            else:
                if get_MyCustomer.otp == otp_:
                    get_MyCustomer.is_activate = True
                    get_MyCustomer.save()
                    messages.success(request, 'Your email has been confirmed. Thank you!')
                    return redirect('login_page_view')
                else:
                    messages.warning(request, "Invalid OTP.")
                    context = {
                        'cum_email':email_
                        }
                    return render(request,'buyer/otp_verify',context)
    return render(request,'buyer/otp_verify')

def login_page_view(request):
    if request.method == 'POST':
        email_ = request.POST['email']
        password_ = request.POST['password']
        if is_valid_email(email_):
            try:
                get_customer = MyCustomerModel.objects.get(email=email_)
            except MyCustomerModel.DoesNotExist:
                messages.warning(request, "User does not exist.")
                return redirect('login_page_view')
            else:
                if get_customer:
                    if get_customer.password == password_:
                        print(get_customer.customer_id, "Added")
                        request.session['customer_id'] = get_customer.customer_id
                        messages.success(request, "Now, you are logged in.")
                        return redirect('index_page_view')
                    else:
                        messages.warning(request, "Email or Password is not match.")
                        return redirect('login_page_view')
        else:
                messages.warning(request, "Invalid Email.")
                return redirect('login_page_view')
            


    return render(request,'buyer/login.html')
                





def base_page_view(request):
    return render(request,'buyer/base.html')

def index_page_view(request):
    return render(request,'buyer/index.html')
def contactus_page_view(request):
    return render(request,'buyer/contact.html')

def about_page_view(request):
    return render(request,'buyer/about.html')

def categories_page(request):
    return render(request,'buyer/categories.html')

def cart_page_view(request):
    return render(request,'buyer/cart.html')
