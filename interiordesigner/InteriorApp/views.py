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
from django.db.models import Sum, Avg
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
from django.contrib.auth import update_session_auth_hash

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
            image = request.FILES.get('image')
            seller_id = request.session['id']
            seller = Seller.objects.get(id=seller_id)

            if product_name and price and stock:  # Simple validation
                product = Product(
                    product_name=product_name,
                    description=description,
                    price=price,
                    stock=stock,
                    image=image,
                    seller=seller
                )
                product.save()
                messages.success(request, 'Product added successfully!')
                
                # Redirect based on category
                category_redirects = {
                    'furniture': 'furniture',
                    'lighting': 'lighting',
                    'decor': 'decor',
                    'carpets': 'carpets',
                    'wallpaper': 'wallpaper',
                    'plants': 'plants',
                    'storage': 'storage'
                }
                return redirect(category_redirects.get(product.category, 'products'))
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


def designer_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            designer = Designer.objects.get(username=username)
            if designer.check_password(password):
                login(request, designer)
                request.session['designer_id'] = designer.id
                messages.success(request, 'Login successful!')
                return redirect('dhome')
            else:
                messages.error(request, 'Invalid username or password')
        except Designer.DoesNotExist:
            messages.error(request, 'Invalid username or password')

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

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        try:
            product = get_object_or_404(Product, id=product_id)
            quantity = int(request.POST.get('quantity', 1))
            
            # Validate quantity
            if quantity <= 0:
                return JsonResponse({
                    'success': False,
                    'error': 'Quantity must be greater than 0'
                })
            
            # Get or create cart
            cart, created = Cart.objects.get_or_create(user=request.user)
            
            # Add item to cart
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            return JsonResponse({
                'success': True,
                'cart_count': cart.get_total_items()
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    })

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

@login_required
def dhome(request):
    try:
        # Check if user has a designer profile
        if not hasattr(request.user, 'designer'):
            messages.error(request, "You don't have a designer profile. Please register as a designer first.")
            return redirect('dregister')  # Redirect to designer registration
            
        designer = request.user.designer
        designs = Design.objects.filter(designer=designer)
        
        # Get statistics for the dashboard
        total_views = 0
        total_likes = 0
        total_comments = 0
        
        # If you have these fields in your Design model, calculate them
        # total_views = designs.aggregate(Sum('views'))['views__sum'] or 0
        # total_likes = designs.aggregate(Sum('likes'))['likes__sum'] or 0
        # total_comments = designs.aggregate(Sum('comments'))['comments__sum'] or 0
        
        context = {
            'designer': designer,
            'designs': designs,
            'total_views': total_views,
            'total_likes': total_likes,
            'total_comments': total_comments,
        }
        return render(request, 'dhome.html', context)
    except Exception as e:
        print(f"Error in dhome: {str(e)}")
        messages.error(request, f"Error loading dashboard: {str(e)}")
        return redirect('home')  # Redirect to main home page on error

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

@login_required
def modeling_view(request):
    return render(request, '3D_Modeling.html')

@login_required
def generate_3d_model(request):
    if request.method == 'POST' and request.FILES.get('room_image'):
        try:
            image = Image.open(request.FILES['room_image'])
            image_np = np.array(image)
            
            if image_np.shape[-1] == 4:
                image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2RGB)

            # Resize for better processing
            target_size = (512, 512)
            image_np = cv2.resize(image_np, target_size)
            gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

            # Enhanced edge detection
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            edges = cv2.Canny(blurred, 50, 150)
            kernel = np.ones((3,3), np.uint8)
            edges = cv2.dilate(edges, kernel, iterations=1)

            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if not contours:
                return JsonResponse({'error': 'No object detected'}, status=400)
            
            # Get the largest contour
            main_contour = max(contours, key=cv2.contourArea)
            
            # Approximate the contour
            epsilon = 0.02 * cv2.arcLength(main_contour, True)
            approx_contour = cv2.approxPolyDP(main_contour, epsilon, True)

            # Create 3D vertices from contour
            vertices = []
            for point in approx_contour:
                x = (point[0][0] / target_size[0]) * 2 - 1
                y = -(point[0][1] / target_size[1]) * 2 + 1  # Flip Y coordinate
                
                # Add front and back vertices
                vertices.append([x, y, 0.2])  # Front
                vertices.append([x, y, -0.2])  # Back

            # Create faces
            faces = []
            num_points = len(approx_contour)
            for i in range(num_points):
                i2 = (i + 1) % num_points
                v0 = i * 2  # Front vertex of current point
                v1 = i2 * 2  # Front vertex of next point
                v2 = v0 + 1  # Back vertex of current point
                v3 = v1 + 1  # Back vertex of next point
                
                # Add two triangles for each quad face
                faces.append([v0, v1, v2])
                faces.append([v1, v3, v2])

            # Create model data
            model_data = {
                'vertices': vertices,
                'faces': faces,
                'dimensions': {
                    'width': 2.0,
                    'height': 2.0,
                    'depth': 0.4
                }
            }

            return JsonResponse({
                'success': True,
                'model_data': model_data
            })

        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)

    return JsonResponse({
        'success': False,
        'error': 'Please upload an image'
    }, status=400)

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

@login_required
def worker_register(request):
    if request.method == 'POST':
        # Get form data
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        specialization = request.POST.get('specialization')
        
        try:
            # Create user
            user = User.objects.create_user(username=username, email=email, password=password)
            
            # Create worker profile without a designer
            worker = Worker.objects.create(
                user=user,
                full_name=full_name,
                email=email,
                phone=phone,
                specialization=specialization,
                # No designer assigned initially
            )
            
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('worker_login')
        
        except Exception as e:
            # Delete the user if worker creation fails
            if 'user' in locals():
                user.delete()
            messages.error(request, f'Registration failed: {str(e)}')
    
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
        assignments = WorkerAssignment.objects.filter(worker=worker)
        
        # Get construction companies instead of designers
        construction_companies = ConstructionCompany.objects.all()
        
        context = {
            'worker': worker,
            'assignments': assignments,
            'completed_projects': assignments.filter(status='completed').count(),
            'pending_projects': assignments.filter(status='pending').count(),
            'total_earnings': sum(a.project.budget for a in assignments.filter(status='completed')) if assignments.exists() else 0,
            'construction_companies': construction_companies,
        }
        
        return render(request, 'worker_dashboard.html', context)
        
    except Exception as e:
        messages.error(request, f'Error loading dashboard: {str(e)}')
        return redirect('worker_login')

@login_required
def apply_to_company(request, designer_id):
    if request.method == 'POST':
        try:
            designer = Designer.objects.get(id=designer_id)
            worker = request.user.worker
            
            # Create a team request
            TeamRequest.objects.create(
                worker=worker,
                designer=designer,
                status='pending'
            )
            
            messages.success(request, f'Application sent to {designer.full_name}')
        except Exception as e:
            messages.error(request, f'Error sending application: {str(e)}')
    
    return redirect('worker_dashboard')

@login_required
def meet_workers(request):
    try:
        # Get all workers ordered by rating
        workers = Worker.objects.all().order_by('-rating')
        
        # Get filter parameters
        specialization = request.GET.get('specialization')
        experience = request.GET.get('experience')
        rating = request.GET.get('rating')
        
        # Apply filters if provided
        if specialization:
            workers = workers.filter(specialization=specialization)
        if experience:
            workers = workers.filter(experience_years__gte=int(experience))
        if rating:
            workers = workers.filter(rating__gte=float(rating))
            
        context = {
            'workers': workers,
            'specializations': Worker.SPECIALIZATION_CHOICES
        }
        
        return render(request, 'meet_workers.html', context)
    except Exception as e:
        messages.error(request, f'Error loading workers: {str(e)}')
        return redirect('home')

def worker_profile(request, worker_id):
    worker = get_object_or_404(Worker, id=worker_id)
    completed_projects = WorkerAssignment.objects.filter(
        worker=worker, 
        status='completed'
    ).select_related('project')
    
    context = {
        'worker': worker,
        'completed_projects': completed_projects,
    }
    return render(request, 'worker_profile.html', context)

def filter_workers(request):
    workers = Worker.objects.all()
    
    specialization = request.GET.get('specialization')
    experience = request.GET.get('experience')
    rating = request.GET.get('rating')
    
    if specialization:
        workers = workers.filter(specialization=specialization)
    if experience:
        workers = workers.filter(experience_years__gte=int(experience))
    if rating:
        workers = workers.filter(rating__gte=float(rating))
    
    workers_data = [{
        'id': w.id,
        'full_name': w.full_name,
        'specialization': w.specialization,
        'rating': w.rating,
        'experience_years': w.experience_years,
        'completed_projects': w.completed_projects,
        'hourly_rate': w.hourly_rate,
        'skills': w.skills,
        'profile_picture': w.profile_picture.url if w.profile_picture else None
    } for w in workers]
    
    return JsonResponse({'workers': workers_data})

@login_required
def view_designs(request):
    try:
        designs = Design.objects.all().order_by('-created_at')
        print(f"Number of designs found: {designs.count()}")
        
        for design in designs:
            print(f"Design: {design.design_name}, Image: {design.image if design.image else 'No image'}")
        
        context = {
            'designs': designs,
            'room_types': Design.ROOM_TYPE_CHOICES,
            'styles': Design.STYLE_CHOICES
        }
        
        return render(request, 'view_designs.html', context)
    except Exception as e:
        print(f"Error in view_designs: {str(e)}")
        messages.error(request, f'Error loading designs: {str(e)}')
        return redirect('home')

@login_required
def filter_designs(request):
    designs = Design.objects.all()
    
    room_type = request.GET.get('room_type')
    style = request.GET.get('style')
    price_range = request.GET.get('price')
    
    if room_type:
        designs = designs.filter(room_type=room_type)
    if style:
        designs = designs.filter(style=style)
    if price_range:
        if price_range == 'budget':
            designs = designs.filter(price__lte=50000)
        elif price_range == 'mid':
            designs = designs.filter(price__gt=50000, price__lte=150000)
        elif price_range == 'luxury':
            designs = designs.filter(price__gt=150000)
    
    designs_data = [{
        'id': d.id,
        'design_name': d.design_name,
        'room_type': d.room_type,
        'style': d.style,
        'price': str(d.price),
        'description': d.description,
        'image_url': d.image.url if d.image else None
    } for d in designs]
    
    return JsonResponse({'designs': designs_data})

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check for predefined admin credentials
        if username == 'jerry' and password == 'jerry@123':
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid credentials')
        else:
            messages.error(request, 'Invalid admin credentials')
    
    return render(request, 'admin_login.html')

@login_required
def admin_dashboard(request):
    # Get statistics and recent activities
    context = {
        'total_users': User.objects.count(),
        'total_workers': Worker.objects.count(),
        'total_designs': Design.objects.count(),
        'completed_projects': Project.objects.filter(status='completed').count(),
        'recent_activities': get_recent_activities()
    }
    return render(request, 'admin_dashboard.html', context)

def admin_logout(request):
    logout(request)
    return redirect('admin_login')

def get_recent_activities():
    # Implement logic to get recent activities
    # This could include user registrations, new designs, favorites, etc.
    return []

@login_required
def admin_users(request):
    users = []
    
    # Get regular users (customers)
    regular_users = User.objects.filter(is_staff=False, is_superuser=False)
    for user in regular_users:
        if not hasattr(user, 'seller') and not hasattr(user, 'designer') and not hasattr(user, 'worker'):
            users.append({
                'full_name': f"{user.first_name} {user.last_name}",
                'username': user.username,
                'email': user.email,
                'role': 'Customer',
                'is_active': user.is_active,
                'date_joined': user.date_joined,
                'profile_picture': None
            })
    
    # Get sellers
    sellers = Seller.objects.all()
    for seller in sellers:
        try:
            users.append({
                'full_name': seller.name,
                'username': seller.username,
                'email': seller.email,
                'role': 'Seller',
                'is_active': seller.is_active,
                'date_joined': timezone.now(),
                'profile_picture': seller.profile_picture.url if hasattr(seller, 'profile_picture') and seller.profile_picture else None
            })
        except Exception as e:
            print(f"Error processing seller {seller.id}: {str(e)}")
            continue
    
    # Get designers
    designers = Designer.objects.all()
    for designer in designers:
        try:
            users.append({
                'full_name': designer.full_name,
                'username': designer.username,
                'email': designer.email,
                'role': 'Designer',
                'is_active': True,
                'date_joined': timezone.now(),
                'profile_picture': designer.profile_picture if designer.profile_picture else None
            })
        except Exception as e:
            print(f"Error processing designer {designer.id}: {str(e)}")
            continue
    
    context = {
        'users': users
    }
    return render(request, 'admin_users.html', context)

@login_required
def filter_users(request):
    role = request.GET.get('role', 'all')
    # Implement filtering logic similar to the above but only for the specified role
    filtered_users = []  # Add filtering logic here
    return JsonResponse({'users': filtered_users})

def view_designers(request):
    try:
        designers = Designer.objects.all()
        print(f"Number of designers found: {designers.count()}")  # Debug line
        
        designers_data = []
        for designer in designers:
            print(f"Processing designer: {designer.full_name}")  # Debug line
            
            # Get number of workers under this designer (if the relationship exists)
            workers_count = Worker.objects.filter(designer=designer).count() if hasattr(Worker, 'designer') else 0
            
            # Get designs by this designer
            designs = Design.objects.filter(designer=designer)
            
            # Calculate average rating (if rating field exists)
            avg_rating = 0
            if hasattr(Design, 'rating'):
                avg_rating = designs.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
            
            # Get total completed projects
            completed_projects = designs.count()
            
            # Get recent designs
            recent_designs = designs.order_by('-created_at')[:3]
            
            # Get specializations as list
            specializations = []
            if designer.specializations:
                specializations = [s.strip() for s in designer.specializations.split(',') if s.strip()]
            
            designer_data = {
                'designer': designer,
                'workers_count': workers_count,
                'avg_rating': round(float(avg_rating), 1),
                'completed_projects': completed_projects,
                'years_experience': getattr(designer, 'experience_years', 0),
                'specializations': specializations,
                'recent_designs': recent_designs,
                'full_name': designer.full_name,
                'email': designer.email,
                'description': designer.description or "An experienced interior designer passionate about creating beautiful spaces.",
                'profile_picture': designer.profile_picture if designer.profile_picture else None
            }
            
            print(f"Designer data prepared: {designer_data}")  # Debug line
            designers_data.append(designer_data)
        
        context = {
            'designers_data': designers_data
        }
        return render(request, 'designers.html', context)
    except Exception as e:
        print(f"Error in view_designers: {str(e)}")
        messages.error(request, f'Error loading designers: {str(e)}')
        return redirect('home')

@login_required
def find_workers(request):
    try:
        workers = Worker.objects.all()  # Fetch all workers
        specializations = Worker.objects.values_list('specialization', flat=True).distinct()  # Get unique specializations
        
        context = {
            'workers': workers,
            'specializations': specializations,
        }
        return render(request, 'find_workers.html', context)  # Render the find_workers template
    except Exception as e:
        messages.error(request, f'Error loading workers: {str(e)}')
        return redirect('dhome')  # Redirect to the designer home page on error

@login_required
def send_worker_request(request, worker_id):
    if request.method == 'POST':
        try:
            worker = Worker.objects.get(id=worker_id)
            designer = request.user.designer
            
            # Check if request already exists
            if not TeamRequest.objects.filter(
                worker=worker,
                designer=designer,
                status='pending'
            ).exists():
                # Create new request
                team_request = TeamRequest.objects.create(
                    worker=worker,
                    designer=designer,
                    status='pending'
                )
                
                # Create notification for worker
                Notification.objects.create(
                    worker=worker,
                    message=f"Designer {designer.full_name} wants to add you to their team",
                    type='team_request',
                    related_id=team_request.id
                )
                
                return JsonResponse({'success': True})
            
            return JsonResponse({'success': False, 'message': 'Request already sent'})
        except Worker.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Worker not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

@login_required
def view_team_requests(request):
    try:
        # Get all team requests for the logged-in designer
        team_requests = TeamRequest.objects.filter(designer=request.user.designer).select_related('worker')
        
        # Organize requests by status
        pending_requests = team_requests.filter(status='pending')
        accepted_requests = team_requests.filter(status='accepted')
        declined_requests = team_requests.filter(status='declined')
        
        context = {
            'pending_requests': pending_requests,
            'accepted_requests': accepted_requests,
            'declined_requests': declined_requests
        }
        
        return render(request, 'team_requests.html', context)  # Render the team_requests template
    except Exception as e:
        messages.error(request, f'Error loading team requests: {str(e)}')
        return redirect('dhome')  # Redirect to the designer home page on error

@login_required
def accept_request(request, request_id):
    if request.method == 'POST':
        try:
            team_request = TeamRequest.objects.get(id=request_id, worker=request.user.worker)
            team_request.status = 'accepted'
            team_request.save()
            
            # Create notification for designer
            Notification.objects.create(
                designer=team_request.designer,
                message=f"{team_request.worker.full_name} has accepted your team request",
                type='request_accepted'
            )
            
            return JsonResponse({'success': True})
        except TeamRequest.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Request not found or you do not have permission'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

@login_required
def decline_request(request, request_id):
    if request.method == 'POST':
        try:
            # Get the team request for the logged-in worker
            team_request = TeamRequest.objects.get(id=request_id, worker=request.user.worker)
            team_request.status = 'declined'
            team_request.save()
            
            # Create notification for designer
            Notification.objects.create(
                designer=team_request.designer,
                message=f"{team_request.worker.full_name} has declined your team request",
                type='request_declined'
            )
            
            return JsonResponse({'success': True})
        except TeamRequest.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Request not found or you do not have permission'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

@login_required
def designer_dashboard(request):
    try:
        # Check if user has a designer profile
        if not hasattr(request.user, 'designer'):
            messages.error(request, "You don't have a designer profile. Please register as a designer first.")
            return redirect('dregister')
            
        designer = request.user.designer
        designs = Design.objects.filter(designer=designer)
        
        # Add more context data for the dashboard
        total_designs = designs.count()
        
        # You can add more statistics if your models support them
        # For example, if Design model has a views field:
        # total_views = designs.aggregate(Sum('views'))['views__sum'] or 0
        
        context = {
            'designer': designer,
            'designs': designs,
            'total_designs': total_designs,
            # Add more context variables as needed
        }
        
        # Print debug information
        print(f"Designer Dashboard - Designer: {designer.full_name}, Designs: {total_designs}")
        
        return render(request, 'designer_dashboard.html', context)
    except Exception as e:
        print(f"Error in designer_dashboard: {str(e)}")
        messages.error(request, f"Error loading dashboard: {str(e)}")
        return redirect('dhome')

@login_required
def edit_profile(request):
    designer = request.user.designer
    if request.method == 'POST':
        # Handle form submission
        designer.full_name = request.POST.get('full_name')
        designer.phone = request.POST.get('phone')
        if 'profile_picture' in request.FILES:
            designer.profile_picture = request.FILES['profile_picture']
        designer.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('dhome')
    
    context = {
        'designer': designer
    }
    return render(request, 'edit_profile.html', context)

@login_required
def apply_for_company(request, designer_id):
    try:
        designer = Designer.objects.get(id=designer_id)
        context = {
            'designer': designer
        }
        print(f"Rendering apply_for_company.html for designer: {designer.full_name}")  # Debug print
        return render(request, 'apply_for_company.html', context)
    except Designer.DoesNotExist:
        messages.error(request, "Designer not found.")
        return redirect('worker_dashboard')

@login_required
def submit_company_application(request, designer_id):
    if request.method == 'POST':
        try:
            designer = Designer.objects.get(id=designer_id)
            worker = request.user.worker

            # Update worker profile with new information
            worker.full_name = request.POST.get('full_name')
            worker.email = request.POST.get('email')
            worker.phone = request.POST.get('phone')
            worker.specialization = request.POST.get('profession')
            worker.experience_years = int(request.POST.get('experience'))
            worker.hourly_rate = float(request.POST.get('salary'))
            
            if 'resume' in request.FILES:
                worker.resume = request.FILES['resume']
            
            worker.save()

            # Create team request
            TeamRequest.objects.create(
                worker=worker,
                designer=designer,
                status='pending'
            )

            messages.success(request, f"Application submitted successfully to {designer.full_name}'s company!")
            return redirect('worker_dashboard')

        except Exception as e:
            messages.error(request, f"Error submitting application: {str(e)}")
            return redirect('apply_for_company', designer_id=designer_id)

    return redirect('worker_dashboard')

@login_required
def company_register(request):
    if request.method == 'POST':
        try:
            # Get passwords and verify they match
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            
            if not password:
                messages.error(request, 'Password is required!')
                return render(request, 'company_register.html')
                
            if password != confirm_password:
                messages.error(request, 'Passwords do not match!')
                return render(request, 'company_register.html')
            
            # Validate password strength
            if len(password) < 8:
                messages.error(request, 'Password must be at least 8 characters long!')
                return render(request, 'company_register.html')
            
            # Create user account with email as username
            email = request.POST.get('email')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered!')
                return render(request, 'company_register.html')
                
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )
            
            # Create construction company profile
            company = ConstructionCompany.objects.create(
                user=user,
                company_name=request.POST.get('company_name'),
                email=email,
                phone=request.POST.get('phone'),
                address=request.POST.get('address'),
                registration_number=request.POST.get('registration_number'),
                established_year=request.POST.get('established_year'),
                company_size=request.POST.get('company_size'),
                description=request.POST.get('description')
            )
            
            if 'logo' in request.FILES:
                company.logo = request.FILES['logo']
                company.save()
            
            messages.success(request, 'Company registered successfully! Please login.')
            return redirect('company_login')
            
        except Exception as e:
            if 'user' in locals():
                user.delete()
            messages.error(request, f'Registration failed: {str(e)}')
            
    return render(request, 'company_register.html')

def company_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            # Since we used email as username during registration
            user = authenticate(username=email, password=password)
            
            if user is not None and hasattr(user, 'constructioncompany'):
                login(request, user)
                messages.success(request, f'Welcome back, {user.constructioncompany.company_name}!')
                return redirect('company_dashboard')
            else:
                messages.error(request, 'Invalid email or password')
        except Exception as e:
            messages.error(request, 'Invalid email or password')
        
    return render(request, 'company_login.html')

@login_required
def company_change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if not request.user.check_password(old_password):
            messages.error(request, 'Current password is incorrect!')
            return redirect('company_change_password')
            
        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match!')
            return redirect('company_change_password')
            
        if len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters long!')
            return redirect('company_change_password')
            
        # Change password
        request.user.set_password(new_password)
        request.user.save()
        
        # Update session auth hash to prevent logout
        update_session_auth_hash(request, request.user)
        
        messages.success(request, 'Password changed successfully!')
        return redirect('company_dashboard')
        
    return render(request, 'company_change_password.html')

@login_required
def company_dashboard(request):
    try:
        company = request.user.constructioncompany
        # Get workers who have applied to this company
        worker_applications = TeamRequest.objects.filter(company=company).select_related('worker')
        
        context = {
            'company': company,
            'worker_applications': worker_applications,
            'total_applications': worker_applications.count(),
            'pending_applications': worker_applications.filter(status='pending').count(),
            'accepted_applications': worker_applications.filter(status='accepted').count(),
        }
        return render(request, 'company_dashboard.html', context)
    except Exception as e:
        messages.error(request, f'Error loading dashboard: {str(e)}')
        return redirect('company_login')

@login_required
def apply_to_company(request, company_id):
    try:
        company = ConstructionCompany.objects.get(id=company_id)
        worker = request.user.worker

        # Check if already applied
        if TeamRequest.objects.filter(worker=worker, company=company).exists():
            messages.warning(request, 'You have already applied to this company')
            return redirect('worker_dashboard')

        # Create new application
        TeamRequest.objects.create(
            worker=worker,
            company=company,
            status='pending'
        )
        
        messages.success(request, f'Successfully applied to {company.company_name}')
        return redirect('worker_dashboard')

    except ConstructionCompany.DoesNotExist:
        messages.error(request, 'Company not found')
    except Exception as e:
        messages.error(request, f'Error applying to company: {str(e)}')
    
    return redirect('worker_dashboard')

@login_required
def handle_application(request, application_id, action):
    try:
        application = TeamRequest.objects.get(id=application_id, company=request.user.constructioncompany)
        
        if action == 'accept':
            application.status = 'accepted'
            messages.success(request, f'Application from {application.worker.full_name} accepted')
        elif action == 'reject':
            application.status = 'rejected'
            messages.success(request, f'Application from {application.worker.full_name} rejected')
            
        application.save()
        
    except TeamRequest.DoesNotExist:
        messages.error(request, 'Application not found')
    except Exception as e:
        messages.error(request, f'Error handling application: {str(e)}')
    
    return redirect('company_dashboard')