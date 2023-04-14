from django.db import models
from django.contrib.auth.models import User
import datetime
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):
    USER_TYPE = (
        ('Customer', 'Customer'),
        ('Administrator', 'Administrator'),
        ('Others', 'Others')
    )
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=1000, blank=True, choices=USER_TYPE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Products(models.Model):
    CATEGORY = (
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE'),
        ('UNISEX', 'UNISEX')
    )
    AVAILABILITY = (
        ('AVAILABLE', 'AVAILABLE'),
        ('OUT OF STOCK', 'OUT OF STOCK')
    )
    product = models.CharField(max_length=100, blank= False)
    price = models.DecimalField(max_length=100, decimal_places=  2, max_digits=20)
    category = models.CharField(choices=CATEGORY, max_length=100)
    availability = models.CharField(choices=AVAILABILITY, max_length= 100)
    description = RichTextField()
    images = models.ImageField(upload_to='images/')
    shipping_fee = models.DecimalField(max_length=100, decimal_places=  2, max_digits=20)

    def __str__(self):
        return self.product

class Carts(models.Model):
    item = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    user = models.ForeignKey(CustomUser, on_delete= models.CASCADE)

    def _str_(self):
        self.item.product

    @property
    def total(self):
        price = self.item.price
        quantity = self.quantity
        total = price * quantity
        return total        
    
    
class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=10000000, blank=True)

class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Out-for-delivery', 'Out-for-delivery'),
        ('Delivered', 'Delivered')
    )
    ordered_item = models.ForeignKey(Products, on_delete= models.CASCADE)
    ordered_date = models.DateField()
    user = models.ForeignKey(CustomUser, on_delete= models.CASCADE)
    ref = models.CharField(max_length=100000, blank=True)
    order_status = models.CharField(choices=STATUS,  max_length=100, blank=True)
    delivery_date = models.DateField(blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)

    @property
    def estimated_days(self):
        ordered_date = self.ordered_date
        delivery_date = self.delivery_date
        if delivery_date == " ":
            return "Not Available"
        else:
            day = delivery_date - ordered_date
       
            return day.days

        

    @property
    def remaining_days(self):
        delivery_date = self.delivery_date
        if delivery_date == " ":
            return "Not Available"
        else:
            today = datetime.date.today()
            day = delivery_date - today
       
            return day.days
      

    @property
    def total(self):
        price = self.ordered_item.price
        quantity = self.quantity
        total = price * quantity
        return total   


    def _str_(self):
        self.ordered_item


class Feedbacks(models.Model):
    name = models.CharField(max_length=1000000, blank=True)
    email = models.EmailField()
    message = models.CharField(max_length=1000000000, blank=True)
    date = models.DateTimeField()


class Newsletter(models.Model):
    email = models.EmailField()
    date = models.DateTimeField()


class Wishlist(models.Model):
    item = models.ForeignKey(Products, on_delete=models.CASCADE)
    date = models.DateField()
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    
    @property
    def total(self):
        return self.item.price