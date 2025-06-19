from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.http import HttpResponse, FileResponse
from .models import *
from django.contrib import messages
import csv
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Create your views here.
def generate_order_pdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf,pagesize=letter,bottomup=0)
    textob=c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica",16)
    seller_id = request.session.get('seller_id')
    accepted_orders=Order.objects.filter(order_seller_id=seller_id,order_status='Accepted')
    lines = []
    lines.append("All Accepted Orders Report")
    lines.append(" ")
    count=1
    for each in accepted_orders:
        lines.append(str(count))
        lines.append("Buyer Name : "+each.order_buyer_first_name+' '+each.order_buyer_last_name)
        lines.append("Buyer Email : "+each.order_buyer_email)
        lines.append("Buyer Contact : "+str(each.order_buyer_contact))
        lines.append("Buyer Address : ")
        lines.append(each.order_buyer_address)
        lines.append("Product Name : " +each.order_product_name)
        lines.append("Product Price : "+str(each.order_product_price))
        lines.append("Order Quantity : "+str(each.order_quantity))
        lines.append("Order Total : "+str(each.order_total))
        lines.append(" ")
        count+=1
    count=0
    for each in lines:
        textob.textLine(str(each))
        count+=1
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf,as_attachment=True,filename='Generated_Orders_Report.pdf')

def generate_product_pdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf,pagesize=letter,bottomup=0)
    textob=c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica",16)
    seller_id = request.session.get('seller_id')
    Out_Stock=Product.objects.filter(seller_name=seller_id,product_status='Out_of_Stock')
    lines = []
    count=1
    lines.append("All Out of Products Report")
    lines.append(" ")
    for each in Out_Stock:
        lines.append(str(count))
        lines.append("Product Name : "+str(each.product_name))
        lines.append("Product Price : "+str(each.product_price))
        lines.append("Product Description : "+str(each.product_description))
        lines.append(" ")
        count+=1
    count=0
    for each in lines:
        textob.textLine(str(each))
        count+=1
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf,as_attachment=True,filename='Generated_Products_Report.pdf')

def about(request):
    if request.method == "POST":
        email=request.POST['email']
        content=request.POST['content']
        type=request.POST['type']
        if type == "contact":
            new_contact_req = Contact_Request(email=email,purpose=content)
            new_contact_req.save()
        elif type == "feedback":
            new_feedback = Feedback(email=email,feedback=content)
            new_feedback.save()
        return redirect('/about/')
    else:
        return render(request,'about.html')

def register_buyer(request):
    
    if request.method=="POST":
        
        username=request.POST['create_username']
        create_password=request.POST['create_password']
        confirm_password=request.POST['confirm_password']
        type="BUYER"
        
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        gender=request.POST['gender']
        date=request.POST['date']
        aadhaar=request.POST['aadhaar']
        contact=request.POST['contact']
        address=request.POST['address']

        if create_password == confirm_password:
            
            New_User = User.objects.create_user(username=username,password=confirm_password)
            New_User.first_name = type
            New_User.save()
            
            New_Buyer = Buyer(New_User=New_User,first_name=first_name,last_name=last_name,email=email,gender=gender,date=date,aadhaar=aadhaar,contact=contact,address=address)
            New_Buyer.save()    
        
        return redirect('/login_buyer/')
    
    else: 
        return render(request,'register_buyer.html')

def register_seller(request):
    
    if request.method=="POST":
        
        username=request.POST['create_username']
        create_password=request.POST['create_password']
        confirm_password=request.POST['confirm_password']
        type="SELLER"
        
        seller_name=request.POST['seller_name']
        seller_description=request.POST['seller_description']
        logo=request.FILES['logo']
        banner=request.FILES['banner']
        gstin=request.POST['gstin']
        email=request.POST['email']
        contact=request.POST['contact']
        address=request.POST['address']

        if create_password == confirm_password:
            
            New_User = User.objects.create_user(username=username,password=confirm_password)
            New_User.first_name=type
            New_User.save()
            
            New_Seller = Seller(New_User=New_User,seller_name=seller_name,seller_description=seller_description,logo=logo,banner=banner,gstin=gstin,email=email,contact=contact,address=address)
            New_Seller.save()
        
        return redirect('/login_seller/')
    
    else:
        
        return render(request,'register_seller.html')

def login_buyer(request):
    
    if request.method=="POST":
        
        username=request.POST['username']
        password=request.POST['password']
        
        is_buyer = User.objects.get(username=username)
        
        buyer_id = Buyer.objects.get(New_User=is_buyer)

        if is_buyer.first_name == "BUYER":
            
            buyer = authenticate(username=username,password=password)
            
            if buyer:    
                
                login(request,buyer) 
                request.session['type'] = is_buyer.first_name
                request.session['buyer_id']=buyer_id.id
                request.session['buyer_username']=is_buyer.username
                return redirect('/buyer/')
            
            else:
                
                return redirect('/login_buyer/')
        else:
            
            return redirect('/login_buyer/')      
    else:
        
        return render(request,'login_buyer.html')

def login_seller(request):
    
    if request.method=="POST":
        
        username=request.POST['username']
        password=request.POST['password']
        
        is_seller = User.objects.get(username=username)
        seller_id = Seller.objects.get(New_User=is_seller)
        if is_seller.first_name == "SELLER":
            
            seller = authenticate(username=username,password=password)
            
            if seller:    
                
                login(request,seller)  
                request.session['type'] = is_seller.first_name
                request.session['seller_id']=seller_id.id
                request.session['seller_username']=is_seller.username
                return redirect('/seller/')
            
            else:
                
                return redirect('/login_seller/')
        else:
            
            return redirect('/login_seller/') 
    else:
        
        return render(request,'login_seller.html')

def buyer(request):

        if request.method == "GET":
            Product_Data = Product.objects.filter(product_status="In_Stock")
            
            context= {
                'Product_Data' : Product_Data
            }
            cart=request.session.get('cart')
            if not cart:
                request.session['cart'] = {}
            return render(request,'buyer.html',context=context)
        
        elif request.method == "POST":
            
            products = request.POST['Product']
            remove = request.POST.get('remove')
            cart = request.session.get('cart')
            if cart:
                quantity = cart.get(products)
                if quantity:
                    if remove:
                        if quantity<=1:
                            cart.pop(products)
                        else:
                            cart[products] = quantity-1
                    else:
                        cart[products] = quantity+1
                else:
                    cart[products] = 1
            else:
                cart = {}
                cart[products] = 1 
            
            request.session['cart'] = cart
            return redirect('/buyer/')

def shops(request):
    Sellers_Data = Seller.objects.all()
    
    context= {
        'Sellers_Data' : Sellers_Data
    }
    
    return render(request,'shops.html',context=context)

def categories(request):
    Categories_Data = Category.objects.all()

    context= {
        'Categories_Data':Categories_Data
    }

    return render(request,'categories.html',context=context)

def logout_buyer(request):
    logout(request)
    return redirect('/')

def logout_seller(request):
    logout(request)
    return redirect('/')

def seller(request):
    id = request.session.get('seller_id')
    Sellers_Data = Seller.objects.get(id=id)
    Product_Data = Product.objects.filter(seller_name=id,product_status="In_Stock")
    context = {
        'Sellers_Data':Sellers_Data,
        'Product_Data':Product_Data,
    }
    return render(request,'seller.html',context = context)

def register_product(request):
    if request.method=="POST":
        product_seller = request.POST['seller_name']
        product_name = request.POST['product_name']
        product_description = request.POST['product_description']
        product_price = request.POST['product_price']
        product_image = request.FILES['product_image']
        product_category = request.POST['category_name']

        seller_name = Seller.objects.get(seller_name=product_seller)
        category_name = Category.objects.get(category_name=product_category)

        New_Product = Product(seller_name=seller_name,product_name=product_name,product_description=product_description,product_price=product_price,product_img=product_image,category_name=category_name)
        New_Product.save()
        return redirect('/register_product/')
    else:
        id = request.session.get('seller_id')
        Seller_Data = Seller.objects.filter(id=id)
        Category_Data = Category.objects.all()
        context = {'Seller_Data':Seller_Data,'Category_Data':Category_Data}
        return render(request,'register_product.html',context=context)

def loadshop(request,id):
    if request.method == "GET":
        cart=request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
    
        Sellers_Data = Seller.objects.filter(id=id)
        Product_Data = Product.objects.filter(seller_name=id,product_status="In_Stock")
        context = {
            'Sellers_Data':Sellers_Data,
            'Product_Data':Product_Data,
        }
        return render(request,'loadshop.html',context=context)
    elif request.method == "POST":
        products = request.POST['Product']
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(products)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(products)
                    else:
                        cart[products] = quantity-1
                else:
                    cart[products] = quantity+1
            else:
                cart[products] = 1
        else:
            cart = {}
            cart[products] = 1 
        
        request.session['cart'] = cart
        return redirect(f'/shops/{id}')

def loadcategory(request,id):
    if request.method == "GET":
        cart=request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
    
        Category_Data = Category.objects.filter(id=id)
        Product_Data = Product.objects.filter(category_name=id,product_status="In_Stock")
        context = {
            'Product_Data':Product_Data,
            'Category_Data':Category_Data,
        }
        return render(request,'loadcategory.html',context=context)
    elif request.method == "POST":
        products = request.POST['Product']
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(products)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(products)
                    else:
                        cart[products] = quantity-1
                else:
                    cart[products] = quantity+1
            else:
                cart[products] = 1
        else:
            cart = {}
            cart[products] = 1 
        
        request.session['cart'] = cart
        return redirect(f'/categories/{id}')

def loadproduct(request,id):
    if request.method == "GET":
        cart=request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        Product_Data = Product.objects.filter(id=id,product_status="In_Stock")
        return render(request,'loadproduct.html',{'Product_Data':Product_Data})
    elif request.method == "POST":
        products = request.POST['Product']
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(products)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(products)
                    else:
                        cart[products] = quantity-1
                else:
                    cart[products] = quantity+1
            else:
                cart[products] = 1
        else:
            cart = {}
            cart[products] = 1 
        
        request.session['cart'] = cart
        return redirect(f'/buyer/{products}')

def loadguest(request,id):
    Product_Data = Product.objects.filter(id=id)
    return render(request,'loadproduct.html',{'Product_Data':Product_Data})

def cart(request):
    product_ids = list(request.session.get('cart').keys())
    cart_Data = Product.objects.filter(id__in=product_ids)
    return render(request,'cart.html',{"cart_Data": cart_Data})

def checkout(request):
    
    buyer_id=request.session['buyer_id']
    buyer_username=request.session['buyer_username']
    cart = request.session.get('cart')
    
    cur_buser = User.objects.get(username=buyer_username)
    cur_buyer = Buyer.objects.get(id=buyer_id)
    
    product_ids = list(request.session.get('cart').keys())
    quantity= list(request.session.get('cart').values())
    
    cur_product = Product.objects.filter(id__in=product_ids)
    
    count=0
    for each in cur_product:
        
        rorder_quantity=int(quantity[count])
        rorder_total=int(each.product_price * quantity[count])

        cur_suser = User.objects.get(username=each.seller_name)
        cur_seller = Seller.objects.get(New_User=cur_suser)
        
        New_Order = Order(
            order_buyer_id=cur_buyer,
            order_buyer_first_name=cur_buyer.first_name,
            order_buyer_last_name=cur_buyer.last_name,
            order_buyer_email=cur_buyer.email,
            order_buyer_contact=cur_buyer.contact,
            order_buyer_address=cur_buyer.address,
            
            order_seller_id=cur_seller,
            order_seller_name=cur_seller.seller_name,
            order_seller_email=cur_seller.email,
            order_seller_contact=cur_seller.contact,
            order_seller_address=cur_seller.address,
            
            order_product_id=each,
            order_product_name=each.product_name,
            order_product_price=each.product_price,
            order_quantity=rorder_quantity,
            order_total=rorder_total)
        New_Order.save()
        count+=1  
    request.session['cart']={}
    return redirect("/buyer/")

def orders(request):
    if request.method == "GET":
        buyer_id = request.session.get('buyer_id')
        Orders_Data = Order.objects.filter(order_buyer_id=buyer_id,buyer_status=False)
        context= {
            'Orders_Data' : Orders_Data
        }
        return render(request,'orders.html',context=context)
    elif request.method == "POST":
        order_id = request.POST['Order_id']
        set = request.POST['Set']
        edit_order = Order.objects.get(id=order_id)
        if set == 'Cancelled':
            edit_order.order_status = set
            edit_order.save()
        elif set == 'Delete':
            if edit_order.seller_status==True:
                edit_order.delete()
            else:
                edit_order.buyer_status=True
                edit_order.save()
        return redirect('/orders/')

def myorders(request):
    if request.method == "GET":
        seller_id = request.session.get('seller_id')
        Orders_Data = Order.objects.filter(order_seller_id=seller_id,seller_status=False)
        context= {
            'Orders_Data' : Orders_Data
        }
        return render(request,'myorders.html',context=context)
    elif request.method == "POST":
        order_id = request.POST['Order_id']
        set = request.POST['Set']
        edit_order = Order.objects.get(id=order_id)
        if set in ['Accepted','Rejected']:
            edit_order.order_status = set
            edit_order.save()
        elif set == 'Delete':
            if edit_order.buyer_status==True:
                edit_order.delete()
            else:
                edit_order.seller_status=True
                edit_order.save()
        return redirect('/myorders/')

def mycategories(request):
    seller_id = request.session.get('seller_id')
    categories = Product.objects.filter(seller_name=seller_id).values("category_name").distinct()
    listx=[]  
    count=0
    for each in categories:
        listx += list(categories[count].values())
        count+=1
    
    Categories_Data = Category.objects.filter(pk__in=listx)
    context= {
        'Categories_Data':Categories_Data
    }

    return render(request,'mycategories.html',context=context)

def loadmycategory(request,id):
    seller_id = request.session.get('seller_id')
    Category_Data = Category.objects.filter(id=id)
    Product_Data = Product.objects.filter(category_name=id,seller_name=seller_id,product_status="In_Stock")
    context = {
        'Product_Data':Product_Data,
        'Category_Data':Category_Data,
    }
    return render(request,'loadmycategory.html',context=context)

def loadmyproduct(request,id):
    seller_id = request.session.get('seller_id')
    Product_Data = Product.objects.filter(id=id,seller_name=seller_id)
    return render(request,'loadmyproduct.html',{'Product_Data':Product_Data})

def manageproducts(request):
    seller_id = request.session.get('seller_id')
    Product_Data = Product.objects.filter(seller_name=seller_id)
    context = {
        'Product_Data':Product_Data,
    }
    return render(request,'manage_product.html',context=context)

def modifyproducts(request):
    if request.method == "POST":
        product_id = request.POST['product_id']
        status = request.POST['status']
        edit_product = Product.objects.get(id=product_id)
        edit_product.product_status=status
        edit_product.save()
        return redirect('/manageproducts/')
    if request.method == "GET":
        return redirect('/manageproducts/')

def deleteproducts(request):
    if request.method == "POST":
        product_id = request.POST['product_id']
        delete_product = Product.objects.get(id=product_id)
        delete_product.delete()
        return redirect('/manageproducts/')
    if request.method == "GET":
        return redirect('/manageproducts/')

def generate_order_csv(request):
    seller_id = request.session.get('seller_id')
    Orders_Data =  Order.objects.filter(order_seller_id=seller_id,order_status='Accepted')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment;filename=All_Accepted_Orders_Report.csv'
    writer = csv.writer(response)

    writer.writerow(['No','Buyer Name','Buyer Email','Buyer Contact','Buyer Address','Product Name','Product Price','Product Quantity','Total Price'])
    count = 1
    for each in Orders_Data:
        writer.writerow([count,each.order_buyer_first_name+' '+each.order_buyer_last_name,each.order_buyer_email,each.order_buyer_contact,each.order_buyer_address,each.order_product_name,each.order_product_price,each.order_quantity,each.order_total])
        count+=1
    return response

def generate_product_csv(request):
    seller_id = request.session.get('seller_id')
    Product_Data =  Product.objects.filter(seller_name=seller_id,product_status='Out_of_Stock')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment;filename=All_Out_of_Stock_Orders_Report.csv'
    writer = csv.writer(response)

    writer.writerow(['No','Product Name','Prodduct Price','Product Description'])
    count = 1
    for each in Product_Data:
        writer.writerow([count,each.product_name,each.product_price,each.product_description])
        count+=1
    return response

def reports(request):
    return  render(request,'reports.html')