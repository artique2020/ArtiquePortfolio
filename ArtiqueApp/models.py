from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Product_Type(models.Model):
    name = models.CharField(max_length=50)
    Description = models.CharField(max_length=300)
    Is_Active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Products(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    Previous_Rate = models.DecimalField(max_digits=5, decimal_places=2,blank=True)
    Current_Rate = models.DecimalField(max_digits=5, decimal_places=2)
    Main_img = models.ImageField(upload_to='ArtiqueApp/static/images/')
    img1 = models.ImageField(upload_to='ArtiqueApp/static/images/',blank=True)
    img2 = models.ImageField(upload_to='ArtiqueApp/static/images/',blank=True)
    Display_main = models.BooleanField(default=False)
    Product_Type = models.ForeignKey(Product_Type, on_delete=models.CASCADE,default=1)
    Product_code = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.title
    
class Transact_hdr(models.Model):
    StatusType = models.TextChoices('StatusType', 'Pending InProgress Completed Cancelled')
    Status = models.CharField(max_length=500, choices=StatusType.choices)
    Mobile = models.CharField(max_length=500, blank=True)
    Comments  = models.TextField(blank=True)
    Created = models.DateTimeField(auto_now_add=True)
    Datecompleted = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Amount = models.DecimalField(max_digits=5, decimal_places=2,blank=True,default=0)
    Order_date = models.DateTimeField(default=now, blank=True)
   

class Transact_dtl(models.Model):
    Transact_id = models.ForeignKey(Transact_hdr, on_delete=models.CASCADE,default=1)
    Product = models.ForeignKey(Products, on_delete=models.CASCADE,default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Created = models.DateTimeField(auto_now_add=True)
    Current_Rate = models.DecimalField(max_digits=5, decimal_places=2,default=0)
    

class Appointment(models.Model):
    name = models.CharField(max_length=500)
    mobile = models.CharField(max_length=500)
    emailid = models.CharField(max_length=500)
    dt = models.DateField(auto_now=False)
    typ = models.CharField(max_length=500)
    visit_time = models.CharField(max_length=500)
    msg = models.TextField(max_length=1000, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name + "-" + str(self.dt)

class subscriber(models.Model):
    name = models.CharField(max_length=500)
    emailid = models.CharField(max_length=500)
    send_info = models.BooleanField()
    
    def __str__(self):
        return self.emailid