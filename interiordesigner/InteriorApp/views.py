from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str  # Ensure force_str is used
from django.conf import settings
from django.urls import reverse
from .tokens import account_activation_token
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.utils import IntegrityError
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render
from .models import *
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
import re
from .forms import FeedbackForm
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.db.models import Sum
import razorpay
from django.views.decorators.csrf import csrf_exempt
import json
import requests.exceptions
import numpy as np
from PIL import Image
import cv2
from scipy.spatial import Delaunay
import base64
from functools import wraps
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.utils import timezone

# Initialize Razorpay client
razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

def home(request):
    return render(request, 'home.html')

def print_hello(request):
    return HttpResponse("Hello")

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            request.session['id']=user.id
            return redirect('realhome')
        else:
            # Check if username exists
            if not User.objects.filter(username=username).exists():
                messages.error(request, 'Invalid Username')
            else:
                messages.error(request, 'Invalid Password')
    return render(request, 'loginn.html')

def registration(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password1']
        phone = request.POST['phone']
        country_code = request.POST.get('country_code', '+1')  # Default to +1 if not provided

        # Input validation
        if not first_name.isalpha() or not first_name[0].isupper():
            messages.error(request, 'First name must only contain letters and start with an uppercase letter.')
            return redirect('register')

        if not last_name.isalpha() or not last_name[0].isupper():
            messages.error(request, 'Last name must only contain letters and start with an uppercase letter.')
            return redirect('register')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Please enter a valid email address.')
            return redirect('register')

        if len(phone) != 10 or not phone.isdigit():
            messages.error(request, 'Phone Number must be exactly 10 digits.')
            return redirect('register')

        if len(password) < 6 or not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password) or not any(char in '@$!%*?&' for char in password):
            messages.error(request, 'Password must be at least 6 characters long and contain letters, numbers, and symbols.')
            return redirect('register')

        try:
            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            user.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')  # Redirect to the login page after successful registration
        except IntegrityError:
            messages.error(request, 'Username is already taken. Please choose another username.')
            return redirect('register')

    return render(request, 'registration.html')

def portfolio(request):
    return render(request, 'portfolio.html')

def userhome(request):
    featured_products = Product.objects.all()  # Fetch top 6 products as featured
    return render(request, 'user_home.html', {'featured_products': featured_products})

def forgotpass(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'No user is registered with this email address.')
            return redirect('forgotpassword')

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        reset_link = request.build_absolute_uri(
            reverse('resetpassword', kwargs={'uidb64': uid, 'token': token})
        )
        subject = 'Password Reset Request'
        message = (
            f"Hello {user.username},\n\n"
            f"Please click the link below to reset your password:\n\n"
            f"{reset_link}\n\n"
            "If you did not request this, please ignore this email."
        )
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
        messages.success(request, 'A password reset link has been sent to your email.')
        return redirect('forgotpassword')
    
    return render(request, 'forgotpassword.html')

def resetpass(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            password_confirm = request.POST.get('password_confirm')
            if password != password_confirm:
                messages.error(request, 'Passwords do not match.')
                return redirect('resetpassword', uidb64=uidb64, token=token)
            
            user.set_password(password)  # Use set_password for hashing
            user.save()
            messages.success(request, 'Your password has been reset successfully.')
            return redirect('login')
        
        return render(request, 'resetpassword.html')
    else:
        messages.error(request, 'The password reset link is invalid or has expired.')
        return redirect('forgotpassword')

def logout_view(request):
    logout(request)
    return redirect('home')

def about(request):
    return render(request, 'about.html')

def service(request):
    return render(request, 'service.html')

def project(request):
    return render(request, 'project.html')

def blog_grid(request):
    # Fetch all blog posts from the database (modify to fit your database structure)
    posts = BlogPost.objects.all()  # Assuming BlogPost is your blog model
    context = {
        'posts': posts,
        }
    return render(request, 'blog_grid.html', context)

def seller_dashboard(request):
    products = Product.objects.filter(seller=request.user)  # Assuming a user is associated with seller
    return render(request, 'seller.html', {'products': products})

# Custom decorator for seller login required
def seller_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'id' not in request.session:
            messages.error(request, 'Please login as a seller first')
            return redirect('slogin')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@login_required
def add_product(request):
    if request.method == 'POST':
        try:
            product_name = request.POST.get('product_name')
            description = request.POST.get('description')
            price = request.POST.get('price')
            stock = request.POST.get('stock')
            category = request.POST.get('category')
            image = request.FILES.get('image')
            seller_id = request.session['id']
            seller = Seller.objects.get(id=seller_id)

            if product_name and price and stock:  # Simple validation
                product = Product(
                    seller=seller,
                    product_name=product_name,
                    description=description,
                    price=price,
                    stock=stock,
                    category=category,
                    image=image
                )
                product.save()
                messages.success(request, 'Product added successfully.')
                
                # Redirect based on category
                category_redirects = {
                    'Furniture': 'furniture',
                    'Lighting': 'lighting_bulbs',
                    'Decor_Items': 'decoration_items',
                    'Carpets': 'carpets_and_rugs',
                    'Curtains': 'curtains_and_drapes',
                    'Wallpaper': 'wallpapers',
                    'Plants': 'indoor_plants',
                    'Storage': 'storage_solutions'
                }
                
                redirect_url = category_redirects.get(category)
                if redirect_url:
                    return redirect(redirect_url)
                
                return redirect('products')  # Fallback to main products page
            else:
                messages.error(request, 'All fields are required.')
        except Exception as e:
            messages.error(request, f'Error adding product: {str(e)}')
            return redirect('add_product')
    
    return render(request, 'add_product.html')

# Edit an existing product (without form)
def edit_product(request, product_id):
    seller_id = request.session['id']
    seller = Seller.objects.get(id = seller_id)
    product = get_object_or_404(Product, id=product_id, seller=seller)
    
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        image = request.FILES.get('image', product.image)  # If no new image is uploaded, keep the current one

        if product_name and price and stock:
            product.product_name = product_name
            product.description = description
            product.price = price
            product.stock = stock
            if image:  # If a new image is provided
                product.image = image
            product.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('shome')
        else:
            messages.error(request, 'All fields are required.')
    
    return render(request, 'edit_product.html', {'product': product})

# Delete a product
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('seller_dashboard')
    
    return render(request, 'delete_product.html', {'product': product})

def seller_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            seller = Seller.objects.get(username=username, password=password)
        except Seller.DoesNotExist:
            messages.error(request, 'Invalid username or password')
            return redirect('slogin')

        if seller is not None:
            # Ensure you're storing the correct seller ID in the session
            request.session['seller'] = seller.username  # Store seller's username
            request.session['id'] = seller.id  # Store seller's ID (which should be an integer)
            return redirect('shome')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'slogin.html')

def shome(request):
    seller_id = request.session.get('id')
    print(seller_id)
    if seller_id:
        try:
            # Ensure you are passing an integer ID to this query
            seller = Seller.objects.get(id=seller_id)
            products = Product.objects.filter(seller=seller)
            print(seller_id)
        except Seller.DoesNotExist:
            print("ii")
            messages.error(request, 'Seller not found.')
            return redirect('slogin')
    else:
        print("jj")
        messages.error(request, 'You need to login first.')
        return redirect('slogin')
    print(products)
    print("")
    return render(request, 'shome.html', {'products': products})



def sregister(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        company = request.POST.get('company')
        password = request.POST.get('password')

        # Check if the username or email already exists
        if Seller.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('sregister')  # Redirect back to the registration form

        if Seller.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('sregister')

        # Create a new seller instance
        seller = Seller.objects.create(
            name=name,
            username=username,
            email=email,
            phone=phone,
            company=company,
            password=password  # Storing password as plain text (Note: This is not recommended in production)
        )

        # Optionally, add a success message
        messages.success(request, 'Your account has been created successfully!')

        # Redirect to another page, like login or dashboard
        return redirect('slogin')  # Update this with your actual login URL name

    # If it's a GET request, just render the registration form
    return render(request, 'sregister.html')

designs = [
    {
        'name': 'Elegant Living Room',
        'price': 2500,
        'origin': 'California',
        'image': 'elr.jpeg',
    },
    {
        'name': 'Modern Kitchen',
        'price': 3000,
        'origin': 'New York',
        'image': 'mk.jpeg',
    },
    # Add more designs here
]
def dportfolio_view(request):
    designs = Design.objects.all()  # Fetch all designs from the database
    context = {'designs': designs}
    return render(request, 'dhome.html', context)

def dregister(request):
    if request.method == 'POST':
        try:
            # First create the User instance
            user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password'],
                email=request.POST['email'],
                first_name=request.POST['full_name']
            )

            # Then create the Designer instance
            designer = Designer.objects.create(
                user=user,
                full_name=request.POST['full_name'],
                email=request.POST['email'],
                phone=request.POST['phone'],
                username=request.POST['username']
            )

            # Finally create the UserProfile and mark as designer
            user_profile = UserProfile.objects.create(
                user=user,  # Link to User instance, not Designer
                phone=request.POST['phone'],
                is_designer=True
            )

            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')

        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
            return redirect('dregister')

    return render(request, 'dregister.html')


def dlogin_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            designer = Designer.objects.get(username=username)
            if designer.password == password:  # Note: Use proper password hashing in production
                # Set the designer session
                request.session['designer_id'] = designer.id
                messages.success(request, 'Login successful!')
                return redirect('dhome')
            else:
                messages.error(request, 'Invalid password')
        except Designer.DoesNotExist:
            messages.error(request, 'Designer not found')
        
    return render(request, 'dlogin.html')

# Create a custom decorator for designer login
def designer_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('designer_id'):
            messages.error(request, 'Please login as a designer first')
            return redirect('dlogin')  # Redirect to designer login
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@designer_login_required  # Change from @login_required
def add_design(request):
    if request.method == 'POST':
        try:
            # Get the currently logged-in designer using session
            designer = Designer.objects.get(id=request.session['designer_id'])
            
            # Create new design
            design = Design.objects.create(
                designer=designer,
                design_name=request.POST['design_name'],
                description=request.POST['description'],
                price=request.POST['price'],
                area_size=request.POST['area_size'],
                room_type=request.POST['room_type'],
                style=request.POST['style']
            )

            # Handle image upload
            if 'image' in request.FILES:
                design.image = request.FILES['image']
                design.save()

            messages.success(request, 'Design added successfully!')
            return redirect('dhome')

        except Designer.DoesNotExist:
            messages.error(request, 'You must be registered as a designer to add designs.')
            return redirect('dregister')
        except Exception as e:
            messages.error(request, f'Error adding design: {str(e)}')
            return redirect('add_design')

    return render(request, 'add_design.html')

def designp(request):
    # Fetch all designs from the database
    designs = Design.objects.all()

    # Group designs by their category
    categorized_designs = {}
    for design in designs:
        category = design.category  # Assuming category is a field in the Design model
        if category not in categorized_designs:
            categorized_designs[category] = []
        categorized_designs[category].append(design)

    # Context to pass to the template
    context = {
        'categorized_designs': categorized_designs
    }

    return render(request, 'designp.html', context)

def decorella(request):
    return render(request, 'decorella.html')

def uphome(request):
    featured_products = Product.objects.all()[:6]  # Fetch top 6 products as featured
    return render(request, 'uphome.html', {'featured_products': featured_products})

# # Product detail view - individual product details
# def product_detail(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     return render(request, 'product_detail.html', {'product': product})

#  Add to cart view
@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        try:
            product = get_object_or_404(Product, id=product_id)
            cart, created = Cart.objects.get_or_create(user=request.user)
            
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': 1}
            )
            
            if not created:
                cart_item.quantity += 1
                cart_item.save()

            # Get updated cart count
            cart_count = CartItem.objects.filter(cart=cart).aggregate(
                total_items=Sum('quantity'))['total_items'] or 0
            
            
            
            return JsonResponse({
                'success': True,
                'message': f"{product.product_name} added to cart",
                'cartCount': cart_count
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    }, status=400)

# Cart view - display items in cart
#  def cart_view(request):
#      cart_product_ids = request.session.get('cart', [])
#      cart_products = Product.objects.filter(id__in=cart_product_ids)
#      return render(request, 'cart.html', {'cart_products': cart_products})


# # Add to favorites
# def add_to_favorites(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     favorites = request.session.get('favorites', [])
#     if product.id not in favorites:
#         favorites.append(product.id)
#     request.session['favorites'] = favorites
#     return redirect('favorites')

# # Search functionality
# def search(request):
#     query = request.GET.get('q')
#     products = Product.objects.filter(product_name__icontains=query)
#     return render(request, 'search_results.html', {'products': products, 'query': query})


# def cart_view(request):
#     cart_items = Cart.objects.filter(user=request.user.id)
#     return render(request, 'cart.html', {'cart_items': cart_items})

# def search_products(request):
#     query = request.GET.get('query')
#     products = Product.objects.filter(product_name__icontains=query)
#     return render(request, 'search_results.html', {'products': products})

# def remove_from_cart(request, item_id):
#     item = get_object_or_404(Cart, id=item_id, user=request.user)
#     item.delete()
#     return redirect('cart')

@login_required
def cart_view(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart).select_related('product')
        
        # Calculate subtotal
        subtotal = sum(item.product.price * item.quantity for item in cart_items)
        delivery_charges = 50 if subtotal > 0 else 0
        total = subtotal + delivery_charges
        
        context = {
            'cart_items': cart_items,
            'subtotal': subtotal,
            'delivery_charges': delivery_charges,
            'total': total,
            'razorpay_key': settings.RAZORPAY_API_KEY,
        }
        return render(request, 'cart.html', context)
    except Cart.DoesNotExist:
        context = {
            'cart_items': [],
            'subtotal': 0,
            'delivery_charges': 0,
            'total': 0,
            'razorpay_key': settings.RAZORPAY_API_KEY,
        }
        return render(request, 'cart.html', context)
    except Exception as e:
        messages.error(request, f"Error loading cart: {str(e)}")
        return redirect('home')

@login_required
def remove_from_cart(request, product_id):
    if request.method == 'POST':
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.delete()
            
            # Recalculate cart count
            cart_count = CartItem.objects.filter(cart=cart).aggregate(
                total_items=Sum('quantity'))['total_items'] or 0
            
            
            return JsonResponse({
                'success': True,
                'message': 'Item removed from cart',
                'cartCount': cart_count
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)
    return JsonResponse({
        'success': False,
        'message': 'Invalid request'
    }, status=400)

# Update the cart (increase/decrease quantity)
@login_required
def update_cart(request, item_id):
    if 'id' in request.session:
        user = request.session['id']
        cart_item = get_object_or_404(CartItem, id=item_id)

        action = request.POST.get('action')
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease' and cart_item.quantity > 1:
            cart_item.quantity -= 1

        cart_item.save()
        return redirect('cart')
    else:
        return redirect('login')
    
    
    
def realhome(request):
    designs = Design.objects.all()
    user_favorites = []
    
    if 'id' in request.session:
        user_favorites = Favorite.objects.filter(
            user_id=request.session['id']
        ).values_list('design_id', flat=True)
    
    context = {
        'designs': designs,
        'user_favorites': user_favorites
    }
    
    return render(request, 'realhome.html', context)

# Designers Page View
def designers_view(request):
    designers = UserProfile.objects.filter(is_designer=True).select_related('user')  # Fetch designers
    return render(request, 'designers.html', {'designers': designers})

# Designer Detail View
def designer_detail(request, designer_id):
    designer = get_object_or_404(User, id=designer_id)  # Fetch the designer by ID
    return render(request, 'designer_detail.html', {'designer': designer})  # Create this template

# # Design Details View
# def design_details(request, design_id):
#     design = get_object_or_404(Design, id=design_id)  # Fetch the design by ID
#     return render(request, 'design_details.html', {'design': design})

# Search View
# def search(request):
#     query = request.GET.get('q')
#     if query:
#         designs = Design.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
#     else:
#         designs = Design.objects.none()
#     return render(request, 'search_results.html', {'designs': designs})



def edit_design(request, id):
    design = get_object_or_404(Design, id=id)

    if request.method == 'POST':
        design_name = request.POST.get('design_name')
        price = request.POST.get('price')
        # origin = request.POST.get('origin')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        # Validation for design_name - letters only
        if not re.match("^[A-Za-z ]+$", design_name):
            messages.error(request, "Design name should contain letters only.")
            return render(request, 'edit_design.html', {'design': design})

        # Validation for description - letters only
        if not re.match("^[A-Za-z ]+$", description):
            messages.error(request, "Description should contain letters only.")
            return render(request, 'edit_design.html', {'design': design})

        # Validation for image - only allow specific types
        if image:
            if not image.name.endswith(('.png', '.jpg', '.jpeg')):
                messages.error(request, "Only image files (PNG, JPG, JPEG) are allowed.")
                return render(request, 'edit_design.html', {'design': design})

            design.image = image

        # Update other fields
        design.design_name = design_name
        design.price = price
        # design.origin = origin
        design.description = description
        design.save()
        return redirect('dhome')

    return render(request, 'edit_design.html', {'design': design})



def remove_design(request, id):
    design = get_object_or_404(Design, id=id)
    if request.method == 'POST':
        design.delete()
        return redirect('dhome')
    return HttpResponseForbidden("Only POST requests allowed for delete.")

@login_required
def designer_cart_view(request):
    # Fetch designer's cart items
    designer_cart_items = DesignerCartItem.objects.filter(user=request.user)
    
    # Calculate total price and service charges
    designer_total_price = sum(item.design.price * item.quantity for item in designer_cart_items)
    designer_service_charges = 100  # Set your service charge, or calculate as needed
    
    context = {
        'designer_cart_items': designer_cart_items,
        'designer_total_price': designer_total_price,
        'designer_service_charges': designer_service_charges,
    }
    return render(request, 'dcart.html', context)

@login_required
def update_designer_cart(request, item_id):
    # Get the specific cart item
    item = get_object_or_404(DesignerCartItem, id=item_id, user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Increase or decrease item quantity based on action
        if action == 'increase':
            item.quantity = F('quantity') + 1
        elif action == 'decrease' and item.quantity > 1:
            item.quantity = F('quantity') - 1
        item.save()
        item.refresh_from_db()

    return redirect('dcart')

@login_required
def remove_from_designer_cart(request, item_id):
    # Get the specific cart item and delete it
    item = get_object_or_404(DesignerCartItem, id=item_id, user=request.user)
    
    if request.method == 'POST':
        item.delete()
    
    return redirect('dcart')

def browse(request):
    return render(request, 'browse.html')

def dhome(request):
    # Logic to get data for the designer dashboard
    return render(request, 'dhome.html')

def shome(request):
    # Logic to get data for the seller dashboard
    return render(request, 'shome.html')

# Remove Designer View
def remove_designer(request, designer_id):
    designer = get_object_or_404(User, id=designer_id)
    designer.delete()  # Remove the designer
    messages.success(request, 'Designer removed successfully.')
    return redirect('designers')  # Redirect back to the designers page

def contact_designer(request, designer_id):
    designer = get_object_or_404(UserProfile, id=designer_id)  # Fetch the designer's profile

    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        sender_email = request.POST.get('email')

        # Send email (you may want to customize this)
        send_mail(
            subject,
            message,
            sender_email,
            [designer.user.email],  # Send to the designer's email
        )
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('designers')  # Redirect back to the designers page

    return render(request, 'contact_designer.html', {'designer': designer})

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user  # Associate feedback with the logged-in user
            feedback.save()
            messages.success(request, 'Your feedback has been submitted successfully!')
            return redirect('feedback')  # Redirect to the feedback page or another page
    else:
        form = FeedbackForm()
    
    feedbacks = Feedback.objects.all()  # Fetch all feedbacks to display
    return render(request, 'feedback.html', {'form': form, 'feedbacks': feedbacks})

def design_detail(request, design_id):
    design = get_object_or_404(Design, id=design_id)
    return render(request, 'design_detail.html', {'design': design})

def kitchen_designs(request):
    try:
        # Change category filter to room_type
        designs = Design.objects.filter(room_type='Kitchen')
        
        context = {
            'designs': designs,
            'room_type': 'Kitchen'
        }
        return render(request, 'kitchen_designs.html', context)
    except Exception as e:
        messages.error(request, f'Error loading kitchen designs: {str(e)}')
        return redirect('home')

def living_room_designs(request):
    try:
        # Change category filter to room_type
        designs = Design.objects.filter(room_type='Living Room')
        
        context = {
            'designs': designs,
            'room_type': 'Living Room'
        }
        return render(request, 'living_room_designs.html', context)
    except Exception as e:
        messages.error(request, f'Error loading living room designs: {str(e)}')
        return redirect('home')

def bedroom_designs(request):
    try:
        # Change category filter to room_type
        designs = Design.objects.filter(room_type='Bedroom')
        
        context = {
            'designs': designs,
            'room_type': 'Bedroom'
        }
        return render(request, 'bedroom_designs.html', context)
    except Exception as e:
        messages.error(request, f'Error loading bedroom designs: {str(e)}')
        return redirect('home')

def bathroom_designs(request):
    try:
        # Change category filter to room_type
        designs = Design.objects.filter(room_type='Bathroom')
        
        context = {
            'designs': designs,
            'room_type': 'Bathroom'
        }
        return render(request, 'bathroom_designs.html', context)
    except Exception as e:
        messages.error(request, f'Error loading bathroom designs: {str(e)}')
        return redirect('home')

def product_1(request):
    products = Product.objects.filter(category='Lighting')
    return render(request, 'lighting.html', {'products': products})

def product_2(request):
    products = Product.objects.filter(category='Decor_Items')
    return render(request, 'decor_items.html', {'products': products})

def product_3(request):
    products = Product.objects.filter(category='Curtains')
    return render(request, 'curtains.html', {'products': products})

def dining_room_designs(request):
    try:
        # Change category filter to room_type
        designs = Design.objects.filter(room_type='Dining Room')
        
        context = {
            'designs': designs,
            'room_type': 'Dining Room'
        }
        return render(request, 'dining_room_designs.html', context)
    except Exception as e:
        messages.error(request, f'Error loading dining room designs: {str(e)}')
        return redirect('home')

def business_office_designs(request):
    try:
        # Change category filter to room_type
        designs = Design.objects.filter(room_type='Office')  # Using 'Office' from room_type choices
        
        context = {
            'designs': designs,
            'room_type': 'Office'
        }
        return render(request, 'business_office_designs.html', context)
    except Exception as e:
        messages.error(request, f'Error loading office designs: {str(e)}')
        return redirect('home')

def hallway_entry_designs(request):
    try:
        # Change category filter to room_type
        designs = Design.objects.filter(room_type='Hallway')  # Make sure this matches your room_type choices
        
        context = {
            'designs': designs,
            'room_type': 'Hallway'
        }
        return render(request, 'hallway_entry_designs.html', context)
    except Exception as e:
        messages.error(request, f'Error loading hallway designs: {str(e)}')
        return redirect('home')

@require_POST
def toggle_favorite(request, design_id):
    if 'id' not in request.session:
        return JsonResponse({'success': False, 'error': 'Please log in first'}, status=401)
    try:
        user_id = request.session['id']
        design = Design.objects.get(id=design_id)
        favorite, created = Favorite.objects.get_or_create(
            user_id=user_id,
            design=design
        )
        
        if not created:
            favorite.delete()
            is_favorite = False
        else:
            is_favorite = True

        return JsonResponse({
            'success': True,
            'is_favorite': is_favorite
        })
    except Design.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Design not found'}, status=404)
    
def fav(request):
    return render(request, 'favourite.html')

@login_required
@require_POST
def remove_from_favorites(request, design_id):
    if 'id' not in request.session:
        return JsonResponse({
            'success': False,
            'error': 'Please log in first'
        }, status=401)
    
    user_id = request.session['id']
    try:
        favorite = Favorite.objects.get(
            user_id=user_id,
            design_id=design_id
        )
        favorite.delete()
        
        # Get updated favorite count
        favorite_count = Favorite.objects.filter(user_id=user_id).count()
        
        return JsonResponse({
            'success': True,
            'message': 'Design removed from favorites',
            'favorite_count': favorite_count
        })
    except Favorite.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Design was not in your favorites'
        }, status=404)

@login_required
def favorites_view(request):
    if 'id' not in request.session:
        messages.error(request, "Please log in to view favorites")
        return redirect('login')
    
    user_id = request.session['id']
    favorites = Favorite.objects.filter(user_id=user_id).select_related('design')
    
    return render(request, 'favourites.html', {
        'favorites': favorites,
        'favorite_count': favorites.count()
    })

def search_designs(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        query = request.GET.get('q', '').strip()
        if len(query) >= 2:
            try:
                designs = Design.objects.filter(
                    Q(design_name__icontains=query) |
                    Q(description__icontains=query) |
                    Q(room_type__icontains=query)  # Changed from category to room_type
                ).distinct()[:10]
                
                # Get user favorites if logged in
                user_favorites = []
                if 'id' in request.session:
                    user_favorites = Favorite.objects.filter(
                        user_id=request.session['id']
                    ).values_list('design_id', flat=True)
                
                results = [{
                    'id': design.id,
                    'name': design.design_name,
                    'category': design.room_type,  # Changed from category to room_type
                    'description': design.description[:100] + '...' if design.description else '',
                    'image': design.image.url if design.image else None,
                    'is_favorite': design.id in user_favorites
                } for design in designs]
                
                return JsonResponse({
                    'success': True,
                    'results': results
                })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                })
    
    return JsonResponse({
        'success': False,
        'results': []
    })

def get_favorites_count(request):
    if not request.user.is_authenticated:
        return JsonResponse({'count': 0})
    
    count = Favorite.objects.filter(user_id=request.session.get('id', 0)).count()
    return JsonResponse({'count': count})

def products_list(request):
    # Get all filters from request
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort = request.GET.get('sort', 'newest')
    
    # Base queryset
    products = Product.objects.all()
    
    # Apply filters
    if category:
        products = products.filter(category=category)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Apply sorting
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'popular':
        products = products.order_by('-views')
    else:  # newest
        products = products.order_by('-created_at')
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 12)  # Show 12 products per page
    products = paginator.get_page(page)
    
    # Get distinct categories and price range for filters
    categories = Product.objects.values_list('category', flat=True).distinct()
    # price_range = Product.objects.aggregate(
    #     min_price=Min('price'),
    #     max_price=Max('price')
    # )
    
    context = {
        'products': products,
        'categories': categories,
        # 'price_range': price_range,
        'selected_category': category,
        'selected_sort': sort,
        'min_price_filter': min_price,
        'max_price_filter': max_price,
        'cart_count': CartItem.objects.filter(cart__user_id=request.session.get('id', 0)).count()
    }
    
    return render(request, 'products.html', context)

def products_by_category(request, category):
    products = Product.objects.filter(category=category)
    return render(request, 'products.html', {
        'products': products,
        'selected_category': category
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Increment view count
    product.views = product.views + 1 if hasattr(product, 'views') else 1
    product.save()
    
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]
    
    return render(request, 'product_detail.html', {
        'product': product,
        'related_products': related_products
    })

def filter_products(request):
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort = request.GET.get('sort')
    
    products = Product.objects.all()
    
    if category and category != 'all':
        products = products.filter(category=category)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'popular':
        products = products.order_by('-views')
    else:
        products = products.order_by('-created_at')
    
    products_data = [{
        'id': product.id,
        'name': product.product_name,
        'price': str(product.price),
        'image': product.image.url if product.image else None,
        'description': product.description[:100] + '...' if product.description else '',
        'category': product.category
    } for product in products[:12]]
    
    return JsonResponse({
        'products': products_data,
        'total_count': products.count()
    })

@login_required
def create_order(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        
        if not cart_items.exists():
            return JsonResponse({
                'success': False,
                'message': 'Cart is empty'
            })
        
        # Calculate total amount including delivery charges
        subtotal = sum(item.product.price * item.quantity for item in cart_items)
        delivery_charges = 50 if subtotal > 0 else 0
        total_amount = subtotal + delivery_charges
        
        # Create Razorpay order
        order_amount = int(total_amount * 100)  # Convert to paise
        order_currency = 'INR'
        
        razorpay_order = razorpay_client.order.create({
            'amount': order_amount,
            'currency': order_currency,
        })
        
        # Create order in database
        order = Order.objects.create(
            user=request.user,
            razorpay_order_id=razorpay_order['id'],
            amount=total_amount,
            status='Pending'
        )
        
        return JsonResponse({
            'success': True,
            'order_id': razorpay_order['id'],
            'amount': order_amount,
            'currency': order_currency
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)

@login_required
def payment_success(request, order_id):
    try:
        # Get the order
        order = Order.objects.get(razorpay_order_id=order_id)
        
        if order.status != 'Completed':
            # Get the user's cart
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
            
            # Create OrderItems
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            
            # Update order status
            order.status = 'Completed'
            order.save()
            
            # Clear the cart
            cart_items.delete()
            
            messages.success(request, "Payment successful! Your order has been placed.")
        
        return render(request, 'payment_success.html', {'order': order})
        
    except Exception as e:
        messages.error(request, f"Error processing payment: {str(e)}")
        return redirect('cart')

@login_required
def get_cart_count(request):
    try:
        cart = Cart.objects.get(user_id=request.session.get('id'))
        cart_count = CartItem.objects.filter(cart=cart).count()
    except Cart.DoesNotExist:
        cart_count = 0
    return JsonResponse({'cart_count': cart_count})

@login_required
def view_orders(request):
    try:
        # Get user ID from session
        user_id = request.session.get('id')
        if not user_id:
            messages.error(request, 'Please log in to view your orders')
            return redirect('login')

        # Get all orders for the current user
        orders = Order.objects.filter(user_id=user_id).order_by('-created_at')
        
        # Get order items for each order
        orders_with_items = []
        for order in orders:
            order_items = OrderItem.objects.filter(order=order)
            subtotal = sum(item.price * item.quantity for item in order_items)
            
            order_data = {
                'order': order,
                'items': order_items,
                'subtotal': subtotal,
                'delivery_charge': 50,  # Fixed delivery charge
                'total': order.amount
            }
            orders_with_items.append(order_data)

        context = {
            'orders_with_items': orders_with_items
        }
        
        return render(request, 'payment_success.html', context)
        
    except Exception as e:
        print(f"Error in view_orders: {str(e)}")  # Debug print
        messages.error(request, f'Error fetching orders: {str(e)}')
        return redirect('products')

def modeling_view(request):
    return render(request, '3D_Modeling.html')

@csrf_exempt
def generate_3d_model(request):
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            image = request.FILES['image']
            print(f"Processing image: {image.name}")
            
            # Read and decode image
            image_data = image.read()
            nparr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                raise ValueError("Failed to decode image")
            
            # Convert to RGB and get dimensions
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            height, width = img_rgb.shape[:2]
            
            # Enhanced depth estimation pipeline
            gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
            
            # Stronger noise reduction
            filtered = cv2.bilateralFilter(gray, 15, 80, 80)
            
            # Enhance contrast
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
            enhanced = clahe.apply(filtered)
            
            # Smoother edge detection
            edges = cv2.Canny(enhanced, 30, 90)
            kernel = np.ones((3,3), np.uint8)
            edges = cv2.dilate(edges, kernel, iterations=1)
            edges = cv2.GaussianBlur(edges, (5,5), 0)
            
            # Create smoother depth map
            depth_map = cv2.distanceTransform(~edges, cv2.DIST_L2, 5)
            depth_map = cv2.GaussianBlur(depth_map, (7,7), 0)
            depth_map = cv2.normalize(depth_map, None, 0, 1, cv2.NORM_MINMAX)
            
            # Lower resolution for smoother mesh
            segments = min(100, min(width, height) // 4)
            rows = segments + 1
            cols = segments + 1
            
            vertices = []
            uvs = []
            
            # Create smoother vertex distribution
            for i in range(rows):
                for j in range(cols):
                    u = j / (cols - 1)
                    v = 1 - (i / (rows - 1))
                    
                    # Smoother position calculation
                    x = (u * 2 - 1)
                    y = (v * 2 - 1)
                    
                    # Bilinear interpolation for depth
                    img_y = int(v * (height - 1))
                    img_x = int(u * (width - 1))
                    
                    # Get smoother depth value
                    z = depth_map[img_y, img_x]
                    
                    # Reduce depth intensity
                    z = np.power(z, 1.2) * 0.3  # Reduced depth scaling
                    
                    vertices.append([x, y, z])
                    uvs.append([u, v])
            
            # Generate faces with proper orientation
            faces = []
            for i in range(rows - 1):
                for j in range(cols - 1):
                    v0 = i * cols + j
                    v1 = v0 + 1
                    v2 = (i + 1) * cols + j
                    v3 = v2 + 1
                    
                    faces.append([v0, v1, v2])
                    faces.append([v1, v3, v2])
            
            # Convert to numpy arrays
            vertices = np.array(vertices, dtype=np.float32)
            faces = np.array(faces, dtype=np.uint32)
            uvs = np.array(uvs, dtype=np.float32)
            
            # Smooth the mesh
            vertices = smooth_mesh(vertices, faces, iterations=2)
            
            # Convert image to base64 for texture
            _, buffer = cv2.imencode('.png', img_rgb)
            texture_data = base64.b64encode(buffer).decode('utf-8')
            
            return JsonResponse({
                'success': True,
                'model_data': {
                    'vertices': vertices.tolist(),
                    'faces': faces.tolist(),
                    'uvs': uvs.tolist(),
                    'texture': f'data:image/png;base64,{texture_data}'
                }
            })
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

def smooth_mesh(vertices, faces, iterations=2):
    """Smooth the mesh using Laplacian smoothing"""
    for _ in range(iterations):
        new_vertices = vertices.copy()
        
        # Create vertex neighbors dictionary
        neighbors = {}
        for face in faces:
            for i in range(3):
                v1, v2 = face[i], face[(i+1)%3]
                if v1 not in neighbors:
                    neighbors[v1] = []
                if v2 not in neighbors[v1]:
                    neighbors[v1].append(v2)
        
        # Apply smoothing
        for i in range(len(vertices)):
            if i in neighbors:
                neighbor_vertices = vertices[neighbors[i]]
                if len(neighbor_vertices) > 0:
                    # Weight center vertex more heavily
                    new_vertices[i] = 0.8 * vertices[i] + 0.2 * np.mean(neighbor_vertices, axis=0)
        
        vertices = new_vertices
    
    return vertices

@login_required
def budget_planner(request):
    if request.method == 'POST':
        try:
            min_budget = float(request.POST.get('min_budget'))
            max_budget = float(request.POST.get('max_budget'))
            room_type = request.POST.get('room_type')
            design_style = request.POST.get('style')
            area_size = float(request.POST.get('area_size'))
            
            # Create budget plan
            budget_plan = BudgetPlan.objects.create(
                user=request.user,
                min_budget=min_budget,
                max_budget=max_budget,
                room_type=room_type,
                design_style=design_style,
                area_size=area_size,
                priority_features=request.POST.getlist('priorities')
            )
            
            # Get products within budget range
            products = Product.objects.filter(
                price__gte=min_budget,
                price__lte=max_budget,
                category__icontains=room_type
            )
            
            if design_style:
                products = products.filter(style__icontains=design_style)
            
            context = {
                'budget_plan': budget_plan,
                'products': products,
                'room_types': ['Living Room', 'Bedroom', 'Dining Room', 'Kitchen'],
                'design_styles': ['Modern', 'Traditional', 'Contemporary', 'Minimalist']
            }
            
            return render(request, 'budget_planner.html', context)
            
        except Exception as e:
            messages.error(request, f'Error creating budget plan: {str(e)}')
            return redirect('budget_planner')
    
    # For GET request
    context = {
        'room_types': ['Living Room', 'Bedroom', 'Dining Room', 'Kitchen'],
        'design_styles': ['Modern', 'Traditional', 'Contemporary', 'Minimalist']
    }
    return render(request, 'budget_planner.html', context)

def get_recommended_products(room_type, style, budget):
    """Get product recommendations based on room type, style and budget"""
    
    # Get all products
    products = Product.objects.all()
    products_list = list(products)  # Convert QuerySet to list
    
    # Create feature text for each product
    product_features = []
    for product in products:
        features = f"{product.category} {product.style} {room_type}"
        product_features.append(features.lower())
    
    # Create TF-IDF vectors
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(product_features)
    
    # Create query vector based on room type and style
    query = f"{room_type} {style}".lower()
    query_vector = vectorizer.transform([query])
    
    # Calculate similarity scores
    similarity_scores = cosine_similarity(query_vector, tfidf_matrix)
    
    # Get product indices sorted by similarity
    product_indices = similarity_scores[0].argsort()[::-1]
    
    # Filter by budget and get recommended products
    recommended_products = []
    total_cost = 0
    
    for idx in product_indices:
        product = products_list[int(idx)]  # Convert numpy.int64 to Python int
        if total_cost + float(product.price) <= float(budget):
            recommended_products.append(product)
            total_cost += float(product.price)
    
    return recommended_products

@login_required
def create_budget_plan(request):
    if request.method == 'POST':
        try:
            min_budget = float(request.POST.get('min_budget'))
            max_budget = float(request.POST.get('max_budget'))
            room_type = request.POST.get('room_type')
            style = request.POST.get('style')
            area_size = float(request.POST.get('area_size'))
            
            # Get matching designs
            designs = Design.objects.filter(
                room_type=room_type,
                style=style,
                price__range=(min_budget, max_budget)
            )
            
            # Get recommended products for each design
            design_recommendations = []
            for design in designs:
                recommended_products = get_recommended_products(
                    room_type=design.room_type,
                    style=design.style,
                    budget=max_budget - float(design.price)  # Remaining budget after design
                )
                
                design_recommendations.append({
                    'design': design,
                    'recommended_products': recommended_products
                })
            
            return JsonResponse({
                'success': True,
                'recommendations': [{
                    'design': {
                        'id': rec['design'].id,
                        'name': rec['design'].design_name,
                        'image_url': rec['design'].image.url if rec['design'].image else None,
                        'price': float(rec['design'].price),
                        'description': rec['design'].description,
                        'style': rec['design'].style,
                    },
                    'products': [{
                        'id': p.id,
                        'name': p.product_name,
                        'image_url': p.image.url if p.image else None,
                        'price': float(p.price),
                        'category': p.category,
                        'style': p.style,
                    } for p in rec['recommended_products']]
                } for rec in design_recommendations]
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return render(request, 'budget_planner.html')

def lighting_bulbs(request):
    # Fetch products that belong to the 'Lighting' category
    products = Product.objects.filter(category='Lighting')
    
    context = {
        'products': products,
    }
    
    return render(request, 'lighting_bulbs.html', context)

def decoration_items(request):
    # Fetch products that belong to the 'Decor_Items' category
    products = Product.objects.filter(category='Decor_Items')
    
    context = {
        'products': products,
    }
    
    return render(request, 'Decoration_items.html', context)

def carpets_and_rugs(request):
    # Fetch products that belong to the 'Carpets' category
    products = Product.objects.filter(category='Carpets')
    
    context = {
        'products': products,
    }
    
    return render(request, 'Carpets_and_Rugs.html', context)

def wallpapers(request):
    # Fetch products that belong to the 'Wallpapers' category
    products = Product.objects.filter(category='Wallpapers')
    
    context = {
        'products': products,
    }
    
    return render(request, 'Walpapers.html', context)

def indoor_plants(request):
    # Fetch products that belong to the 'Indoor Plants' category
    products = Product.objects.filter(category='Indoor Plants')
    
    context = {
        'products': products,
    }
    
    return render(request, 'Indoor_plants.html', context)

def storage_solutions(request):
    # Fetch products that belong to the 'Storage Solutions' category
    products = Product.objects.filter(category='Storage Solutions')
    
    context = {
        'products': products,
    }
    
    return render(request, 'Storage_solution.html', context)

def furniture(request):
    # Fetch products that belong to the 'Furniture' category
    products = Product.objects.filter(category='Furniture')
    
    context = {
        'products': products,
    }
    
    return render(request, 'furniture.html', context)

def curtains_and_drapes(request):
    # Fetch products that belong to the 'Curtains' category
    products = Product.objects.filter(category='Curtains')
    
    context = {
        'products': products,
    }
    
    return render(request, 'Curtains_and_Drapes.html', context)

@login_required
def payment_success_page(request):
    try:
        # Get all orders for the current user
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        
        # Get order items for each order
        orders_with_items = []
        for order in orders:
            order_items = OrderItem.objects.filter(order=order)
            subtotal = sum(item.price * item.quantity for item in order_items)
            
            order_data = {
                'order': order,
                'items': order_items,
                'subtotal': subtotal,
                'delivery_charge': 50,  # Fixed delivery charge
                'total': order.amount
            }
            orders_with_items.append(order_data)

        return render(request, 'payment_success.html', {
            'orders_with_items': orders_with_items
        })
        
    except Exception as e:
        messages.error(request, f'Error fetching orders: {str(e)}')
        return redirect('cart')

def worker_register(request):
    if request.method == 'POST':
        try:
            # Create User instance
            user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password'],
                email=request.POST['email'],
                first_name=request.POST['full_name']
            )

            # Create Worker instance
            skills = request.POST.getlist('skills[]')  # Get skills as list
            worker = Worker.objects.create(
                user=user,
                full_name=request.POST['full_name'],
                phone=request.POST['phone'],
                email=request.POST['email'],
                experience_years=request.POST['experience'],
                skills=skills,
                hourly_rate=request.POST['hourly_rate'],
                specialization=request.POST['specialization']
            )

            # Handle profile picture
            if 'profile_picture' in request.FILES:
                worker.profile_picture = request.FILES['profile_picture']
                worker.save()

            messages.success(request, 'Registration successful! Please login.')
            return redirect('worker_login')

        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
            return redirect('worker_register')

    return render(request, 'worker_register.html')

def worker_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is not None and hasattr(user, 'worker'):
            auth_login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('worker_dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'worker_login.html')

@login_required
def worker_dashboard(request):
    try:
        worker = request.user.worker
        assignments = WorkerAssignment.objects.filter(worker=worker).select_related('project', 'project__designer')
        
        context = {
            'worker': worker,
            'assignments': assignments,
            'completed_projects': assignments.filter(status='completed').count(),
            'pending_projects': assignments.filter(status='pending').count(),
            'total_earnings': sum(a.project.budget for a in assignments.filter(status='completed')),
            'current_month_earnings': sum(
                a.project.budget for a in assignments.filter(
                    status='completed',
                    completion_date__month=timezone.now().month
                )
            ),
        }
        return render(request, 'worker_dashboard.html', context)
    except Worker.DoesNotExist:
        messages.error(request, 'Worker profile not found')
        return redirect('worker_login')