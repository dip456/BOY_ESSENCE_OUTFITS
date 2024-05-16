from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings








from authentication.models import MyCustomerModel
from authentication.models import MyAddressModel
from master.utils.BOY_VALIDATORS.email_password import is_valid_email,is_valid_password
from master.utils.BOY_PAYMENTGAT.razorpay_payment import client
from master.utils.BOY_RANDOM.otp import generate_new_otp
from seller.models import MyProductsModel
from seller.models import MyCategoriesModel
from buyer.models import MyCartModel





import os
import uuid




def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'customer_id' not in request.session:
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
                return render(request,'buyer/otp_verify.html',context)
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
                    return render(request,'buyer/otp_verify.html',context)
    return render(request,'buyer/otp_verify.html')



def login_page_view(request):
    if request.method == 'POST':
        email_ = request.POST['email']
        password_ = request.POST['password']
        if is_valid_email(email_):
            try:
                get_MyCustomer = MyCustomerModel.objects.get(email=email_)
            except MyCustomerModel.DoesNotExist:
                messages.warning(request, "User does not exist.")
                return redirect('login_page_view')
            else:
                if get_MyCustomer:
                    if get_MyCustomer.password == password_:
                        print(get_MyCustomer.customer_id, "Added")
                        request.session['customer_id'] = get_MyCustomer.customer_id
                        messages.success(request, "Now, you are login .")
                        return redirect('index_page_view')
                    else:
                        messages.warning(request, "Email or Password is not match.")
                        return redirect('login_page_view')
        else:
                messages.warning(request, "Invalid Email.")
                return redirect('login_page_view')
            


    return render(request,'buyer/login.html')


@login_required
def profile_page_view(request):
    if 'customer_id' in request.session:
        customer_id_ = request.session['customer_id']
        try:
            get_MyCustomer = MyCustomerModel.objects.get(customer_id=customer_id_)
            get_address = MyAddressModel.objects.get(customer_id=customer_id_)
            print(get_address.curent_address, "----")
            context = {
                'get_customer': get_MyCustomer,
                'get_address': get_address
            }
            return render(request, 'buyer/profile.html', context)
        except ObjectDoesNotExist:
            print("Customer or Address does not exist for the given ID")
            return render(request, 'buyer/profile.html', {'error_message': 'Customer or Address does not exist.'})
    else:
        print("Customer ID does not exist in the session")
        return redirect('login_page_view')
                



@login_required
def logout(request):
    # request.session.clear()
    del request.session['customer_id']
    messages.success(request, "Now, you are logged out.")
    return redirect('login_page_view')

def update_personal_info(request):
    print("here....")
    if request.method == 'POST':
        firstname_ = request.POST['firstname']
        lastname_ = request.POST['lastname']
        mobile_ = request.POST['mobile']

        try:
            get_MyCustomer = get_object_or_404(MyCustomerModel, customer_id=request.session['customer_id'])
        except MyCustomerModel.DoesNotExist:
            messages.warning(request, 'User does not exist.')
            return redirect('profile_page_view')
        else:
            get_MyCustomer.firstname = firstname_
            get_MyCustomer.lastname = lastname_
            get_MyCustomer.mobile = mobile_
            get_MyCustomer.save()
            messages.success(request, 'Profile data updated.')
            return redirect('profile_page_view')
        


@login_required
def add_address_view(request):
    c_add = request.POST['curent_address']
    ct = request.POST['city']
    ps = request.POST['pincode']
    stt = request.POST['state']

    try:
        get_MyCustomer = get_object_or_404(MyCustomerModel, customer_id=request.session['customer_id'])
    except MyCustomerModel.DoesNotExist:
        messages.warning(request, 'User does not exist.')
        return redirect('profile_page_view')
    else:
        new_address = MyAddressModel.objects.create(
            customer_id_id=get_MyCustomer.customer_id,
            curent_address=c_add,
            city=ct,
            pincode=ps,
            state=stt
        )
        new_address.save()
        get_MyCustomer.is_added_address = True
        get_MyCustomer.save()
        messages.success(request, 'Address added')
        return redirect('profile_page_view')
    

def base_page_view(request):
    return render(request,'buyer/base.html')

def index_page_view(request):
    return render(request,'buyer/index.html')


def contactus_page_view(request):
    return render(request,'buyer/contact.html')


def about_page_view(request):
    return render(request,'buyer/about.html')

    
@login_required
def my_shopping_page(request):
    categoris = MyCategoriesModel.objects.all()
    products = MyProductsModel.objects.all()
    context = {
        'products':products,
        'categoris':categoris
    }
    return render(request,'buyer/categories.html',context)


@login_required
def cart_page_view(request):
    cartItems = MyCartModel.objects.filter(customer_id_id=request.session['customer_id'])
    print(cartItems)
    context = {
        'cartItems':cartItems
    }
    return render(request, 'buyer/cart.html',context)

@login_required
def proceed_pay_view(request):
    return render(request, 'buyer/proceed_to_pay.html')

@login_required
def pay(request,amt):
    amount = int(amt)*100
    data = { "amount": amount, "currency": "INR", "receipt": "order_rcptid_11" }
    p = client.order.create(data=data)   
    print(p)
    return JsonResponse(p)

def prodcut_exist_in_cart(product_id):
    return MyCartModel.objects.filter(product_id=product_id).exists()

@login_required
def add_item_in_cart(request, product_id):
    if not prodcut_exist_in_cart(product_id):
        new_cart_item = MyCartModel.objects.create(
            customer_id_id=request.session['customer_id'],
            product_id_id=product_id
        )
        new_cart_item.save()
        messages.success(request, "item added in cart.")
    else:
        get_cart_item = MyCartModel.objects.get(product_id_id=product_id)
        get_cart_item.quantity += 1
        get_cart_item.save()
    
    return redirect('cart_page_view')

