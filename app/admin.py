from django.contrib import admin
from .models import Carts, Products, Order, Address, Feedbacks, Newsletter, Wishlist, CustomUser
# Register your models here.
admin.site.register(Carts)
admin.site.register(Products)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(Feedbacks)
admin.site.register(Newsletter)
admin.site.register(Wishlist)
admin.site.register(CustomUser)