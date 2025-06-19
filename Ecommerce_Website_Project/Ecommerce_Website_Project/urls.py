"""
URL configuration for Ecommerce_Website_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Ecommerce_Website_Application.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    
    #Admin_Side

    path('admin/', admin.site.urls),

    
    #General_Guest -Register_Users -Logins -Logoutss
        
    path('',about,name="about"),
    path('about/',about,name="about"),
    
    path('register_buyer/',register_buyer,name="register_buyer"),
    path('register_seller/',register_seller,name="register_seller"),
    
    path('login_buyer/',login_buyer,name="login_buyer"),
    path('login_seller/',login_seller,name="login_seller"),
    
    path('logout_buyer/',logout_buyer,name="logout_buyer"),
    path('logout_seller/',logout_seller,name="logout_seller"),
    

    #Buyer_Side **Show** -Products -Sellers -Categories
    
    path('buyer/',buyer,name="buyer"),
    path('buyer/<str:id>',loadproduct,name="loadproduct"),
    
    path('shops/',shops,name="shops"),
    path('shops/<str:id>',loadshop,name="loadshop"),
    
    path('categories/',categories,name="categories"),
    path('categories/<str:id>',loadcategory,name="loadcategory"),


    #Buyer_Side **Cart** **Checkout** **Orders**
    
    path('cart/',cart,name="cart"),
    path('checkout/',checkout,name="checkout"),
    
    path('orders/',orders,name="orders"),


    #Seller_Side **Show** -MyProducts -MyCategories
    
    path('seller/',seller,name="seller"),
    path('seller/<str:id>',loadmyproduct,name="loadmyproduct"),
    
    path('mycategories/',mycategories,name="mycategories"),
    path('mycategories/<str:id>',loadmycategory,name="loadmycategory"),
    

    #Seller_Side **Add** **Manage** -Products

    path('register_product/',register_product,name="register_product"),
    
    path('manageproducts/',manageproducts,name="manageproducts"),
    path('modifyproduct/',modifyproducts,name="modifyproducts"),
    path('deleteproduct/',deleteproducts,name="deleteproducts"),
    
    path('myorders/',myorders,name="myorders"),

    path('reports/',reports,name="reports"),
    path('generate_order_csv/',generate_order_csv,name="generate_order_csv"),
    path('generate_product_csv/',generate_product_csv,name="generate_product_csv"),
    path('generate_order_pdf/',generate_order_pdf,name="generate_order_pdf"),
    path('generate_product_pdf/',generate_product_pdf,name="generate_product_pdf"),
]

urlpatterns += static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root =settings.STATIC_ROOT)
