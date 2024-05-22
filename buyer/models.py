from django.db import models
from django.conf import settings
from django.contrib.auth.models import User



from authentication.models import MyCustomerModel
from seller.models import MyProductsModel
from master.models import baseModel

# Create your models here.
class MyCartModel(baseModel):
    customer_id = models.ForeignKey(MyCustomerModel, on_delete=models.CASCADE)
    product_id = models.ForeignKey(MyProductsModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)



class OrderModel(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    razorpay_order_id = models.CharField(max_length=100)
    razorpay_payment_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Pending')  
    created_at = models.DateTimeField(auto_now_add=True)
