from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import  get_object_or_404
from .models import MenuItem
from .forms import MenuItemForm 
from django.http import JsonResponse
from .models import Product, Cart, Order, OrderItem
from django.views.decorators.http import require_POST
from django.db.models import Sum
from decimal import Decimal



# Create your views here.
def home(request):
    items = MenuItem.objects.all()
    return render(request, 'home.html', {
        'items': items,
        'user': request.user
    }) 

def add_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MenuItemForm()
    return render(request, 'add_item.html', {'form': form})

def update_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MenuItemForm(instance=item)
    return render(request, 'update_item.html', {'form': form})

def delete_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('home')
    return render(request, 'delete_item.html', {'item': item})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                # Save the user without authenticating
                user = form.save()
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                
                # Verify the user was created in the database
                if User.objects.filter(username=username).exists():
                    messages.success(request, f'Account created successfully for {username}. Please login to continue.')
                    # Redirect to login page with username
                    return redirect(f'/login/?username={username}')
                else:
                    messages.error(request, 'Error creating account. Please try again.')
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('menu')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = AuthenticationForm()
        # Pre-fill username if provided in URL
        if 'username' in request.GET:
            form.fields['username'].initial = request.GET['username']
    return render(request, 'login.html', {'form': form})






@login_required(login_url='login')
def menu_view(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to access the menu.')
        return redirect('login')
        
    products = Product.objects.all().order_by('category', 'name')
    return render(request, 'menu.html', {
        'products': products,
        'user': request.user
    }) 


def about_us(request):
    return render(request, 'about.html') 

def register_view(request):
    return render(request, 'register.html')





@login_required
def add_to_cart(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        
        # Check if the product is already in the user's cart
        existing_item = Cart.objects.filter(user=request.user, product=product).first()
        
        if existing_item:
            # If item already exists, increase quantity
            existing_item.quantity += 1
            existing_item.save()
        else:
            # Otherwise, create a new cart item
            Cart.objects.create(user=request.user, product=product, quantity=1)
        
        return JsonResponse({
            "message": "Item added to cart successfully",
            "cart_count": Cart.objects.filter(user=request.user).count()
        }, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required
def view_cart(request):
    try:
        cart_items = Cart.objects.filter(user=request.user).select_related('product')
        total = sum(item.total_price() for item in cart_items)
        
        # Convert cart items to JSON format
        cart_items_data = [{
            'id': item.id,
            'product': {
                'id': item.product.id,
                'name': item.product.name,
                'price': float(item.product.price),
                'image': item.product.image.url if item.product.image else None
            },
            'quantity': item.quantity,
            'total_price': float(item.total_price())
        } for item in cart_items]
        
        return JsonResponse({
            'cart_items': cart_items_data,
            'total': float(total),
            'cart_count': len(cart_items)
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required
@require_POST
def remove_from_cart(request, item_id):
    try:
        cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
        cart_item.delete()
        return JsonResponse({
            "message": "Item removed from cart successfully",
            "cart_count": Cart.objects.filter(user=request.user).count()
        }, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required
@require_POST
def update_cart_quantity(request, item_id):
    try:
        cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity < 1:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save()
            
        return JsonResponse({
            "message": "Cart updated successfully",
            "cart_count": Cart.objects.filter(user=request.user).count()
        }, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required
def get_cart_count(request):
    try:
        count = Cart.objects.filter(user=request.user).count()
        return JsonResponse({"cart_count": count})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def product_management(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Staff privileges required.')
        return redirect('menu')
    
    products = Product.objects.all().order_by('category', 'name')
    return render(request, 'product_management.html', {'products': products})

@login_required
@require_POST
def add_product(request):
    if not request.user.is_staff:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        name = request.POST.get('name')
        price = request.POST.get('price')
        category = request.POST.get('category')
        image = request.FILES.get('image')
        
        if not all([name, price, category, image]):
            return JsonResponse({'error': 'All fields are required'}, status=400)
        
        product = Product.objects.create(
            name=name,
            price=price,
            category=category,
            image=image
        )
        
        return JsonResponse({
            'message': 'Product added successfully',
            'product': {
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'category': product.category,
                'image_url': product.image.url
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def get_product(request, product_id):
    if not request.user.is_staff:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        product = get_object_or_404(Product, id=product_id)
        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'category': product.category
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_POST
def update_product(request, product_id):
    if not request.user.is_staff:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        product = get_object_or_404(Product, id=product_id)
        
        product.name = request.POST.get('name', product.name)
        product.price = request.POST.get('price', product.price)
        product.category = request.POST.get('category', product.category)
        
        if 'image' in request.FILES:
            product.image = request.FILES['image']
        
        product.save()
        
        return JsonResponse({
            'message': 'Product updated successfully',
            'product': {
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'category': product.category,
                'image_url': product.image.url
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_POST
def delete_product(request, product_id):
    if not request.user.is_staff:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        return JsonResponse({'message': 'Product deleted successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def place_order(request):
    try:
        # Get cart items
        cart_items = Cart.objects.filter(user=request.user).select_related('product')
        if not cart_items.exists():
            return JsonResponse({'error': 'Your cart is empty'}, status=400)
        
        # Calculate total amount
        total_amount = sum(item.total_price() for item in cart_items)
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount
        )
        
        # Create order items and clear cart
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            cart_item.delete()
        
        return JsonResponse({
            'message': 'Order placed successfully',
            'order_id': order.id
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})

@login_required
def order_details(request, order_id):
    try:
        order = get_object_or_404(Order, id=order_id, user=request.user)
        return render(request, 'order_details.html', {'order': order})
    except Order.DoesNotExist:
        messages.error(request, 'Order not found')
        return redirect('order_history')

@login_required
@require_POST
def update_order_status(request, order_id):
    if not request.user.is_staff:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        
        if new_status not in dict(Order.STATUS_CHOICES):
            return JsonResponse({'error': 'Invalid status'}, status=400)
        
        order.status = new_status
        order.save()
        
        return JsonResponse({
            'message': 'Order status updated successfully',
            'status': order.get_status_display()
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_POST
def cancel_order(request, order_id):
    try:
        order = get_object_or_404(Order, id=order_id, user=request.user)
        
        if not order.can_cancel():
            return JsonResponse({
                'error': 'Order cannot be cancelled. Only pending orders within 30 minutes can be cancelled.'
            }, status=400)
        
        order.status = 'cancelled'
        order.save()
        
        return JsonResponse({'message': 'Order cancelled successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)








