from django.db import models
from django.contrib.auth.models import User

class Contact_Request(models.Model):
    email = models.EmailField(max_length=50)
    purpose = models.TextField(max_length=500)
    def __str__(self):
        return "Contact Request : " + str(self.id)

class Feedback(models.Model):
    email = models.EmailField(max_length=50)
    feedback = models.TextField(max_length=500)
    def __str__(self):
        return "Feedback ID : " + str(self.id)

class Buyer(models.Model):
    New_User = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name= models.CharField(max_length=50)
    email= models.EmailField(max_length=50)
    date = models.DateField()
    gender = models.CharField(max_length=10)
    aadhaar = models.CharField(max_length=12)
    contact = models.CharField(max_length=10)
    address = models.TextField(max_length=400)
    def __str__(self):
        return self.New_User.username

class Seller(models.Model):
    New_User = models.ForeignKey(User, on_delete=models.CASCADE)
    seller_name= models.CharField(max_length=50)
    seller_description= models.CharField(max_length=50)
    logo= models.ImageField(upload_to='Sellers/Logos/')
    banner = models.ImageField(upload_to='Sellers/Banners/')
    gstin = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    contact = models.CharField(max_length=10)
    address = models.TextField(max_length=400)
    def __str__(self):
        return self.New_User.username

class Category(models.Model):
    category_name = models.CharField(max_length=50)
    category_description = models.CharField(max_length=100)
    category_icon = models.ImageField(upload_to='Categories/Icons/',default='')
    category_banner = models.ImageField(upload_to='Categories/Banners/',default='')
    def __str__(self):
        return self.category_name
    
class Product(models.Model):
    seller_name = models.ForeignKey(Seller, on_delete=models.CASCADE) 
    product_name = models.CharField(max_length=50)
    product_description = models.CharField(max_length=100)
    product_price = models.IntegerField(default=1)
    product_img = models.ImageField(upload_to='Products/Images')
    status_choice = [
        ('In_Stock','In Stock'),
        ('Out_of_Stock','Out of Stock'),
    ]
    product_status= models.CharField(max_length=50,choices=status_choice,default='In_Stock')
    category_name = models.ForeignKey(Category,on_delete=models.CASCADE)
    def __str__(self):
        return self.product_name
    
class Order(models.Model):

    order_buyer_id = models.ForeignKey(Buyer,on_delete=models.CASCADE)
    order_buyer_first_name = models.CharField(max_length=250)
    order_buyer_last_name = models.CharField(max_length=250)
    order_buyer_email = models.CharField(max_length=250)
    order_buyer_contact = models.CharField(max_length=250)
    order_buyer_address = models.CharField(max_length=250)

    order_seller_id = models.ForeignKey(Seller,on_delete=models.CASCADE)
    order_seller_name = models.CharField(max_length=250)
    order_seller_email = models.CharField(max_length=250)
    order_seller_contact = models.CharField(max_length=250)
    order_seller_address = models.CharField(max_length=250)

    order_product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    order_product_name = models.CharField(max_length=250)
    order_product_price = models.CharField(max_length=250)
    order_quantity= models.IntegerField()
    order_total= models.IntegerField()

    buyer_status = models.BooleanField(default=False)
    seller_status = models.BooleanField(default=False)

    status_choice = [
        ('Order_Placed','Ordered Placed'),
        ('Cancelled','Cancelled'),
        ('Accepted','Accepted'),
        ('Rejected','Rejected'),
        ('Out_For_Pickup','Out For Pickup'),
        ('Picked_Up','Picked Up'),
        ('Out_For_Delivery','Out For Delivery'),
        ('Delivered','Delivered'),
    ]
    order_status= models.CharField(max_length=50,choices=status_choice,default='Order_Placed')

    def __str__(self):
        return "Order Id : " + str(self.id)