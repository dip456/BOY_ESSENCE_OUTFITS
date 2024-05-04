from django.db import models

from master.models import baseModel

# Create your models here.
class MyCustomerModel(baseModel):
        Customer_id = models.CharField(primary_key=True,max_length=255, blank=True)
        firstName = models.CharField(max_length=255, blank=True)
        lastName = models.CharField(max_length=255, blank=True)
        email = models.EmailField(max_length=255, blank=False, null=False)
        mobile = models.CharField(max_length=255, blank=True)
        password = models.CharField(max_length=255)
        is_activate = models.BooleanField(default=False)
        #is_added_address = models.BooleanField(default=False)
        otp = models.CharField(max_length=10, default="111111")

        def __str__(self):
              return f"{self.Customer_id} - {self.FirstName} {self.LastName}"
        
        def save(self, *args, **kwargs):
               if not self.Customer_id:
                     self.Customer_id = self.generate_customer_id()
               return super(MyCustomerModel, self).save(*args, **kwargs)
        
        def generate_customer_id(self):
              Mylast_customer = MyCustomerModel.objects.order_by('-Customer_id').first()
              if Mylast_customer:
                    last_id = int(Mylast_customer.Customer_id[3:])
                    new_id = last_id + 1
              else:
                   new_id = 1
              return 'BEO{:04d}'.format(new_id)










