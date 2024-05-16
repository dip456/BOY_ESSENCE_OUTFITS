from django.db import models

from authentication.models import MyCustomerModel
from seller.models import MyProductsModel
from master.models import baseModel

# Create your models here.
class MyCartModel(baseModel):
    customer_id = models.ForeignKey(MyCustomerModel, on_delete=models.CASCADE)
    product_id = models.ForeignKey(MyProductsModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
