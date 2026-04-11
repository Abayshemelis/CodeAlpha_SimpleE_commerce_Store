from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q 
from django.db import transaction
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Import your models and forms
from .models import Product, Category, ContactMessage, Order, OrderItem
from .cart import Cart
from .forms import LoginForm, ExtendedRegistrationForm

# --- 1. AUTHENTICATION & PROFILE VIEWS ---

def login_user(request):
    """Handles user login and redirects to the user dashboard."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def register_user(request):
    """Handles registration using the Extended form (Email, Phone, Date)."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = ExtendedRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please login to continue.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ExtendedRegistrationForm()
    
    return render(request, 'register.html', {'form': form})
@login_required
def dashboard(request):
    """
    Displays the Two-Column Dashboard. 
    Shows ALL orders for the user sorted by newest first.
    """
    # Change 'order_of' to 'order_by'
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    return render(request, 'dashboard.html', {'orders': orders})

def logout_user(request):
    """Logs out the user and redirects to home."""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')


# --- 2. STORE BROWSING VIEWS ---

def home(request):
    """Main landing page with search and category filtering."""
    categories = Category.objects.all()
    search_query = request.GET.get('search')
    category_slug = request.GET.get('category')
    
    products = Product.objects.filter(is_active=True)
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'home.html', {
        'products': products, 
        'categories': categories,
        'current_category': category_slug
    })

def product_detail(request, pk):
    """Individual product display page."""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})


# --- 3. CART OPERATIONS (AJAX) ---

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty', 1)) 
        product = get_object_or_404(Product, id=product_id)
        
        if product.stock < product_qty:
            return JsonResponse({'error': f'Only {product.stock} items left!'}, status=400)

        cart.add(product=product, quantity=product_qty)
        return JsonResponse({'qty': cart.__len__()})
    return JsonResponse({'error': 'Invalid request'}, status=400) 

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    totals = cart.get_total()
    
    if cart_products:
        for product in cart_products:
            item_id = str(product.id)
            if item_id in cart.cart:
                product.quantity = cart.cart[item_id]['quantity']
            
    return render(request, "cart_summary.html", {"cart_products": cart_products, "totals": totals})

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        cart.update(product=product_id, quantity=product_qty)
        return JsonResponse({'qty': cart.__len__()})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product_id=product_id)
        return JsonResponse({'product': product_id, 'qty': cart.__len__()})
    return JsonResponse({'error': 'Invalid request'}, status=400)


# --- 4. CHECKOUT & ORDERING ---

def checkout(request):
    """Handles the final purchase process and saves order info."""
    if not request.user.is_authenticated:
        messages.warning(request, "Please login first to view the checkout page.")
        return redirect('login')

    cart = Cart(request)
    cart_products = cart.get_prods()
    totals = cart.get_total()

    if not cart_products:
        messages.info(request, "Your cart is empty.")
        return redirect('home')

    if request.method == "POST":
        with transaction.atomic():
            full_name = request.POST.get('full_name')
            email = request.POST.get('email')
            shipping_address = request.POST.get('address')
            city = request.POST.get('city', 'Hawassa')
            # Fetching phone from POST if you added it to checkout form
            phone = request.POST.get('phone')

            new_order = Order.objects.create(
                user=request.user,
                full_name=full_name,
                email=email,
                phone_number=phone,
                shipping_address=shipping_address,
                shipping_city=city,
                amount_paid=totals
            )

            for product in cart_products:
                item_id = str(product.id)
                quantity = int(cart.cart[item_id]['quantity'])
                
                if product.stock < quantity:
                    messages.error(request, f"Sorry, {product.name} just went out of stock.")
                    return redirect('cart_summary')

                OrderItem.objects.create(
                    order=new_order,
                    product=product,
                    quantity=quantity,
                    price=product.price
                )

                # Reduce stock level
                product.stock -= quantity
                product.save()

            cart.clear() 
            messages.success(request, f"Success! Order #{new_order.id} placed.")
            return redirect('dashboard') 

    if cart_products:
        for product in cart_products:
            item_id = str(product.id)
            if item_id in cart.cart:
                product.quantity = cart.cart[item_id]['quantity']
            
    return render(request, "checkout.html", {"cart_products": cart_products, "totals": totals})


# --- 5. SUPPORT ---

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_content = request.POST.get('message')
        ContactMessage.objects.create(name=name, email=email, message=message_content)
        messages.success(request, f"Thanks {name}! Your message has been sent.")
        return redirect('contact')
    return render(request, "contact.html")