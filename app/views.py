from django.shortcuts import redirect, render
from django.http import HttpResponse
from sympy import Sum
from .models import Carts, Products, Order, Address, Feedbacks, Newsletter, Wishlist, CustomUser
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import datetime
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password



# Create your views here.
def home(request):
    item = Products.objects.all()[:5]
    todays_deal = Products.objects.all().order_by("?")[:4]
    
    return render(request, 'index.html', {"products": item, "todays_deal":todays_deal})

def login(request):
    if request.method == "POST":
        username = request.POST['email']
        password = request.POST['password']
        q = request.GET.get("next")
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            if not request.user.user_type == "Customer":
                messages.error(request, "No account found")
                auth.logout(request)
                return redirect("login")
            if 'next' in request.GET:
                return redirect(q)
            else:
                return redirect("home")
        else:
            messages.info(request, "Incorrect Username or Password")
    return render(request, 'login.html',)

def register(request):
    if request.method == "POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            if CustomUser.objects.filter(username=username).exists():
                messages.info(request, "Username already exists")
            elif CustomUser.objects.filter(email=email).exists():
                messages.info(request, "Email already exists")
            else:
                user= CustomUser.objects.create(first_name=firstname, last_name=lastname, email=email, username=username, password=make_password(password), user_type='Customer')
                user.save()
                messages.info(request, "Account Successfully created")
                    
        else:
            messages.info(request, "Password does not match")
    return render(request, 'register.html')

def about(request):
    return render(request, 'about-us.html')

def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        Feedbacks.objects.create(name=name, email=email, message=message, date=datetime.datetime.now())
        return render(request, 'feedback_sent.html', {"name": name})

        
    return render(request, 'contact.html')

def shop(request):
    if not request.user.user_type == "Customer":
        return redirect("login")
    p = Paginator(Products.objects.all(), 10)
    page = request.GET.get("page")
    item = p.get_page(page)
    
    return render(request, 'shop.html', {"item": item})

def product(request, id):
    if not request.user.user_type == "Customer":
        return redirect("login")
    item = Products.objects.get(pk=id)
    product = Products.objects.all()
    try:
        wishlist_item = Wishlist.objects.get(item=item, user=request.user)
    except Wishlist.DoesNotExist:
        wishlist_item = ""
    if request.method == "POST":
        quantity = request.POST['quantity']
        user = request.user
        cart_item = Products.objects.get(product=request.POST['product'])
        cart = Carts.objects.filter(user=user, item=cart_item).first()
        if cart:
            cart.quantity += int(quantity)
            cart.save()
            return redirect('cart')
        else:
            Carts.objects.create(item=cart_item, user=user, quantity=quantity)
            return redirect('cart')


    else:
        print("")


    return render(request, 'product.html', {"item": item, "products": product, "wishlist": wishlist_item})

@login_required(login_url= '/login/')
def cart(request):
    if not request.user.user_type == "Customer":
        return redirect("login")
    p = Paginator(Carts.objects.filter(user=request.user).all(), 10)
    page = request.GET.get("page")
    cart = p.get_page(page)
    cart_item = Carts.objects.filter(user=request.user).all()
    count = cart_item.count()
    total = sum([c.total for c in cart_item])
    return render(request, 'cart.html', {"carts" : cart, "count": count, "total": total})

@login_required(login_url= '/login/')
def logout(request):
    auth.logout(request)
    return redirect('home')

@login_required(login_url= '/login/')
def remove_from_cart(request, pk):
     if not request.user.user_type == "Customer":
        return redirect("login")
     cart = Carts.objects.get(pk=pk)
     if cart.quantity > 1:
          cart.quantity -= 1
          cart.save()
     else:
         cart.delete()
     return redirect('cart')

@login_required(login_url= '/login/')
def add_to_cart(request, id):
    if not request.user.user_type == "Customer":
        return redirect("login")

    item = Products.objects.get(id=id)
    quantity = 1
    cart_item = Carts.objects.filter(user=request.user, item=item).first()
    if cart_item:
        cart_item.quantity+= int(quantity)
        cart_item.save()
        return redirect("cart")
    else:
        Carts.objects.create(item=item, user=request.user, quantity=quantity)
        return redirect("cart")





@login_required(login_url= '/login/')
def checkout(request):
    if not request.user.user_type == "Customer":
        return redirect("login")
    cart = Carts.objects.filter(user=request.user).all()
    count = cart.count()
    total = sum([c.total for c in cart])
    try:
        address = Address.objects.get(user=request.user)
    except:
        address = "No Address"
    return render(request, 'checkout.html', {"carts" : cart, "count": count, "total": total, "address": address})

@login_required(login_url= '/login/')
def address(request):
    if not request.user.user_type == "Customer":
        return redirect("login")
    if request.method == "POST":
        user = request.user
        shipping_address = request.POST['address']
        Address.objects.create(user=user, shipping_address=shipping_address)
        messages.success(request, "Shipping address successfully added")
   
    return render(request, 'address.html')


@login_required(login_url= '/login/')
def change_address(request):
    if not request.user.user_type == "Customer":
        return redirect("login")
    address = Address.objects.get(user=request.user)
    if request.method == "POST":
        user = request.user
        shipping_address = request.POST['address']
        address.shipping_address = shipping_address
        address.save()
        messages.success(request, "Shipping address successfully updated")
   
    return render(request, 'change_address.html', {"address": address})
    

@login_required(login_url= '/login/')
def payment_successful(request):
    if not request.user.user_type == "Customer":
        return redirect("login")
    ref = request.GET.get("ref")
    items = Carts.objects.filter(user=request.user).all()
    address = Address.objects.get(user=request.user)
    for i in items:
        Order.objects.create(ref=ref, user=request.user, ordered_item=i.item, ordered_date=datetime.date.today(), order_status="Pending", address=address, quantity=i.quantity)

    items.delete()
    return redirect("orders")

@login_required(login_url= '/login/')
def orders(request):
    if not request.user.user_type == "Customer":
        return redirect("login")
    items = Order.objects.filter(user=request.user).all()
    return render(request, 'order.html', {"items": items})

@login_required(login_url= '/login/')
def settings(request):
    if not request.user.user_type == "Customer":
        return redirect("login")
    return render(request, 'settings.html')

def newsletter(request):
    if not request.user.user_type == "Customer":
        return redirect("login")
    if request.method == "POST":
        email = request.POST['email']
        dt = datetime.datetime.now()
        if Newsletter.objects.filter(email=email).exists():
            return render(request, 'newletter_error.html', {"email": email})
        Newsletter.objects.create(email=email, date=dt)
        return render(request, 'newsletter_subscription.html', {"email": email})

@login_required(login_url= '/login/')
def order_product(request, id):
    if not request.user.user_type == "Customer":
        return redirect("login")
    item = Order.objects.filter(user=request.user).get(id=id)
    
    return render(request, 'order_product.html', {"item": item,})



@login_required(login_url= '/login/')
def wishlist(request):
    if not request.user.user_type == "Customer":
        return redirect("login")
    item = Wishlist.objects.filter(user=request.user).all()
    total = sum([c.total for c in item ])
    
    return render(request, 'wishlist.html', {"items": item, "total": total})

@login_required(login_url= '/login/')
def add_to_wishlist(request, id):
    if not request.user.user_type == "Customer":
        return redirect("login")
    item = Products.objects.get(id=id)
    if Wishlist.objects.filter(user=request.user, item=item).exists():
        return render(request, 'wishlist_exist.html', {"item": item})
    else:
        Wishlist.objects.create(item=item, user=request.user, date=datetime.date.today())
        return redirect("product", id=id)

@login_required(login_url= '/login/')
def remove_from_wishlist(request, id):
    if not request.user.user_type == "Customer":
        return redirect("login")
    item =Products.objects.get(id=id)
    wishlist_item = Wishlist.objects.get(item=item)
    wishlist_item.delete()
    return redirect("product", id=id)

@login_required(login_url= '/login/')
def remove_wishlist(request, id):
    if not request.user.user_type == "Customer":
        return redirect("login")
    item = Wishlist.objects.get(id=id)
    item.delete()
    return redirect("wishlist")

@login_required(login_url= '/login/')
def empty_wishlist(request):
    if not request.user.user_type == "Customer":
        return redirect("login")
    items = Wishlist.objects.filter(user=request.user).all()
    items.delete()
    return redirect("wishlist")
    




