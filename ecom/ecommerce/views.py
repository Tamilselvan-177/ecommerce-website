from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Catagory, Product, Cart, Order
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render
from .models import Product

# views.py

from django.shortcuts import render

def home(request):
    # Fetch all trending products
    trending_products = Product.objects.filter(trending=True)

    # Fetch visible categories
    categories = Catagory.objects.filter(status=False)

    # You can pass the first category to the template or all categories, depending on your needs
    category = categories.first()  # For example, passing the first category

    return render(request, 'shop/home.html', {
        'products': trending_products,
        'categories': categories,
        'category': category  # Pass category to the template
    })


def collections(request):
    categories = Catagory.objects.filter(status=False)  # Fetch active categories
    return render(request, 'shop/collections.html', {"categories": categories})

def collectionsview(request, name):
    try:
        category = Catagory.objects.get(name=name, status=False)  # Use status=False for active categories
        products = Product.objects.filter(category=category, status=True)  # Use status=True for active products
        return render(request, "shop/product/index.html", {"products": products, "category": category})
    except Catagory.DoesNotExist:
        messages.warning(request, "No Such Category Found")
        return redirect('collections')

def register(request):
    return render(request, 'shop/register.html')

def project_details(request, cname, pname):
    try:
        product = Product.objects.get(name=pname, status=True)
        category = Catagory.objects.get(name=cname, status=False)
        return render(request, 'shop/product/product_details.html', {"product": product})
    except (Product.DoesNotExist, Catagory.DoesNotExist):
        messages.warning(request, "No Such Product or Category Found")
        return redirect('collections')

@login_required(login_url='/login/')
def add_to_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
        return redirect('index')

    if product.quantity > 0:
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': 1}
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f"{product.name} quantity updated in your cart.")
        else:
            messages.success(request, f"{product.name} added to your cart.")

        return redirect('cart')
    else:
        messages.error(request, f"Sorry, {product.name} is out of stock.")
        return redirect('index')

@login_required(login_url='/login/')
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.selling_price * item.quantity for item in cart_items)
    
    if request.method == 'POST':
        address = request.POST['address']
        payment_method = request.POST['payment_method']
        
        if cart_items:  # Ensure cart is not empty
            order = Order.objects.create(
                user=request.user,
                address=address,
                payment_method=payment_method,
                total_price=total_price
            )
            
            for item in cart_items:
                item.product.quantity -= item.quantity  # Deduct from stock
                item.product.save()
            
            cart_items.delete()  # Clear cart
            messages.success(request, "Your order has been placed successfully.")
            return redirect('order_confirmation', order_id=order.id)
        else:
            messages.warning(request, "Your cart is empty.")
    
    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total_price': total_price})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Signup successful!")
            return redirect('index')
        else:
            messages.error(request, "There was an error with your signup.")
    else:
        form = UserCreationForm()
    
    return render(request, 'shop/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'shop/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out successfully.")
    return redirect('index')

@login_required(login_url='/login/')
def view_orders(request):
    orders = Order.objects.filter(user=request.user)
    context = {'orders': orders}
    return render(request, 'shop/order.html', context)

@login_required(login_url='/login/')
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'shop/order_confirmation.html', {'order': order})

@login_required(login_url='/login/')
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.selling_price * item.quantity for item in cart_items)
    
    if request.method == 'POST':
        address = request.POST['address']
        payment_method = request.POST['payment_method']
        
        if cart_items:  # Ensure cart is not empty
            order = Order.objects.create(
                user=request.user,
                address=address,
                payment_method=payment_method,
                total_price=total_price
            )
            
            for item in cart_items:
                item.product.quantity -= item.quantity  # Deduct from stock
                item.product.save()
            
            cart_items.delete()  # Clear cart
            messages.success(request, "Your order has been placed successfully.")
            return redirect('order_confirmation', order_id=order.id)
        else:
            messages.warning(request, "Your cart is empty.")
    
    return render(request, 'shop/checkout.html', {'cart_items': cart_items, 'total_price': total_price})
@login_required(login_url='/login/')
def remove_from_cart(request, cart_item_id):
    try:
        cart_item = Cart.objects.get(id=cart_item_id, user=request.user)
        cart_item.delete()
        messages.success(request, "Item removed from your cart.")
    except Cart.DoesNotExist:
        messages.error(request, "This item is not in your cart.")
    return redirect('cart')