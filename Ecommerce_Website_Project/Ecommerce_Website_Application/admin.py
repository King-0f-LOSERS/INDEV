from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Buyer)
admin.site.register(Seller)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Contact_Request)
admin.site.register(Feedback)