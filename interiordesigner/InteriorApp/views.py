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
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError, FieldError
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
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
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
    # Get recent designs
    recent_designs = Design.objects.order_by('-created_at')[:4]
    
    # Get recent designers
    top_designers = Designer.objects.order_by('-id')[:3]
    
    # Get latest products
    latest_products = Product.objects.order_by('-created_at')[:6]
    
    context = {
        'recent_designs': recent_designs,
        'top_designers': top_designers,
        'latest_products': latest_products,
        'user': request.user,
        'is_designer': hasattr(request.user, 'designer') if request.user.is_authenticated else False,
        'is_customer': not hasattr(request.user, 'designer') if request.user.is_authenticated else False,
    }
    return render(request, 'home.html', context)

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
        if 'seller_id' not in request.session:
            messages.error(request, 'Please login as a seller first')
            return redirect('slogin')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@seller_login_required
def add_product(request):
    if request.method == 'POST':
        try:
            product_name = request.POST.get('product_name')
            description = request.POST.get('description')
            price = request.POST.get('price')
            stock = request.POST.get('stock')
            image = request.FILES.get('image')
            category = request.POST.get('category')
            style = request.POST.get('style')
            
            # Get seller from session using seller_id instead of id
            seller_id = request.session.get('seller_id')
            if not seller_id:
                raise ValueError("Please login as a seller")
                
            seller = Seller.objects.get(id=seller_id)

            if not all([product_name, price, stock, style]):
                raise ValueError("All required fields must be filled")

            product = Product(
                seller=seller,
                product_name=product_name,
                description=description,
                price=price,
                stock=stock,
                image=image,
                category=category,
                style=style
            )
            product.save()
            messages.success(request, 'Product added successfully!')
            
            # Redirect based on category
            category_redirects = {
                'Furniture': 'furniture',
                'Lighting': 'lighting_bulbs',
                'Decor': 'decor_items',
                'Carpets': 'carpets_and_rugs',
                'Curtains': 'curtains_and_drapes',
                'Wallpaper': 'wallpapers',
                'Plants': 'indoor_plants',
                'Storage': 'storage_solutions'
            }
            return redirect(category_redirects.get(product.category, 'products'))
            
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('add_product')
        except Exception as e:
            messages.error(request, f'Error adding product: {str(e)}')
            return redirect('add_product')
    
    return render(request, 'add_product.html')

# Edit an existing product (without form)
def edit_product(request, product_id):
    seller_id = request.session['seller_id']
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

def sregister(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        # Check if username or email exists in Seller table only
        if Seller.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('sregister')

        if Seller.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('sregister')

        # Create seller without User instance
        seller = Seller.objects.create(
            name=request.POST.get('name'),
            username=username,
            email=email,
            phone=request.POST.get('phone'),
            company=request.POST.get('company'),
            password=make_password(request.POST.get('password'))  # Hash the password
        )

        messages.success(request, 'Your account has been created successfully!')
        return redirect('slogin')

    return render(request, 'sregister.html')

def seller_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            seller = Seller.objects.get(username=username)
            if seller.check_password(password):
                # Store seller info in session
                request.session['seller_id'] = seller.id
                request.session['role'] = 'seller'
                messages.success(request, 'Login successful!')
                return redirect('shome')
            else:
                messages.error(request, 'Invalid password')
        except Seller.DoesNotExist:
            messages.error(request, 'Invalid username')
        
        return redirect('slogin')
    return render(request, 'slogin.html')

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
            # Check if username or email already exists in Designer table
            if Designer.objects.filter(username=request.POST['username']).exists():
                messages.error(request, 'Username already taken')
                return redirect('dregister')
            
            if Designer.objects.filter(email=request.POST['email']).exists():
                messages.error(request, 'Email already registered')
                return redirect('dregister')

            # Create Designer instance directly without User
            designer = Designer.objects.create(
                username=request.POST['username'],
                password=make_password(request.POST['password']),  # Hash the password
                email=request.POST['email'],
                full_name=request.POST['full_name'],
                phone=request.POST['phone']
            )

            messages.success(request, 'Registration successful! Please login.')
            return redirect('dlogin')

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
            if check_password(password, designer.password):
                # Store designer info in session
                request.session['designer_id'] = designer.id
                request.session['role'] = 'designer'
                messages.success(request, 'Login successful!')
                return redirect('dhome')  # Changed from dhome to designer_dashboard
            else:
                messages.error(request, 'Invalid password')
        except Designer.DoesNotExist:
            messages.error(request, 'Invalid username')
        
        return redirect('dlogin')

    return render(request, 'dlogin.html')

# Add the decorator to protect designer routes
def designer_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        designer_id = request.session.get('designer_id')
        if not designer_id:
            messages.error(request, 'Please login as a designer first')
            return redirect('dlogin')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@designer_login_required
def designer_dashboard(request):
    try:
        # Get the designer ID from the session
        designer_id = request.session.get('designer_id')
        if not designer_id:
            messages.error(request, 'Designer session not found.')
            return redirect('dlogin')
            
        designer = Designer.objects.get(id=designer_id)
        
        # Get designs by this designer
        designs = Design.objects.filter(designer=designer)
        
        # Get consultation requests by this designer
        consultation_requests = DesignerConsultationRequest.objects.filter(designer=designer).order_by('-created_at')
        
        # Get pending consultations as a queryset, not just a count
        pending_consultations = consultation_requests.filter(status='pending')
        
        # Get all companies - don't filter by status to see if any exist
        companies = Company.objects.all()
        
        # Get all regular users (not staff, not companies)
        # This ensures we only get actual clients
        company_user_ids = Company.objects.values_list('user_id', flat=True)
        clients = User.objects.filter(is_staff=False).exclude(id__in=company_user_ids)
        
        # Calculate total likes safely
        total_likes = 0
        if hasattr(Design, 'favorited_by'):
            for design in designs:
                total_likes += design.favorited_by.count()
        
        context = {
            'designer': designer,
            'designs': designs,
            'consultation_requests': consultation_requests,
            'pending_consultations': pending_consultations,  # Now this is a queryset, not a count
            'companies': companies,
            'clients': clients,
            'total_designs': designs.count(),
            'pending_consultations_count': pending_consultations.count(),  # Add this for stats
            'completed_consultations': consultation_requests.filter(status='completed').count(),
            'total_views': designs.aggregate(Sum('views'))['views__sum'] or 0,
            'total_likes': total_likes,
            'total_consultations': consultation_requests.count(),
        }
        
        return render(request, 'designer_dashboard.html', context)
        
    except Designer.DoesNotExist:
        messages.error(request, 'Designer not found.')
        return redirect('dlogin')

@designer_login_required
def handle_consultation(request, consultation_id, action):
    if request.method == 'POST':
        try:
            consultation = Consultation.objects.get(id=consultation_id)
            
            if action == 'approve':
                consultation.status = 'approved'
                message = 'Consultation request approved successfully!'
            elif action == 'decline':
                consultation.status = 'declined'
                message = 'Consultation request declined.'
            else:
                return JsonResponse({'success': False, 'error': 'Invalid action'})
            
            consultation.save()
            
            # Create notification for user
            Notification.objects.create(
                user=consultation.user,
                title=f'Consultation {consultation.status}',
                message=f'Your consultation request for {consultation.design.design_name} has been {consultation.status}.',
                notification_type='consultation_update'
            )
            
            return JsonResponse({
                'success': True,
                'message': message,
                'consultation_id': consultation_id,
                'new_status': consultation.status
            })
            
        except Consultation.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Consultation not found'
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    })

@login_required
def get_notifications(request):
    notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).order_by('-created_at')
    
    return JsonResponse({
        'notifications': list(notifications.values(
            'id', 'title', 'message', 'created_at'
        ))
    })

@login_required
def mark_notification_read(request, notification_id):
    if request.method == 'POST':
        notification = get_object_or_404(Notification, id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

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
                category=request.POST['room_type'],  # Use room_type as category
                room_type=request.POST['room_type'],
                style=request.POST['style']
            )

            # Handle image upload
            if 'image' in request.FILES:
                design.image = request.FILES['image']
                design.save()

            messages.success(request, 'Design added successfully!')
            return redirect('designer_dashboard')

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


def add_to_cart(request, product_id):
    if request.method == 'POST':
        try:
            # Check if user is authenticated
            if not request.user.is_authenticated:
                return JsonResponse({
                    'success': False,
                    'message': 'Please log in to add items to your cart',
                    'redirect': '/login/'  # URL to redirect to login page
                })
            
            product = get_object_or_404(Product, id=product_id)
            quantity = int(request.POST.get('quantity', 1))
            
            # Validate quantity
            if quantity <= 0:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid quantity'
                })
            
            # Get or create cart
            cart, created = Cart.objects.get_or_create(user=request.user)
            
            # Get or create cart item
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            
            # If cart item already exists, update quantity
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            # Calculate cart count directly
            cart_count = CartItem.objects.filter(cart=cart).aggregate(
                total_items=Sum('quantity'))['total_items'] or 0
            
            return JsonResponse({
                'success': True,
                'cartCount': cart_count
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })


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


def cart_view(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        # For anonymous users, either redirect to login or show empty cart
        messages.warning(request, "Please log in to view your cart.")
        return redirect('login')  # Redirect to your login page
    
    try:
        # Get or create cart for authenticated user
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        
        # Calculate totals
        subtotal = sum(item.product.price * item.quantity for item in cart_items)
        delivery_charges = 50 if subtotal > 0 else 0
        total = subtotal + delivery_charges
        
        context = {
            'cart_items': cart_items,
            'subtotal': subtotal,
            'delivery_charges': delivery_charges,
            'total': total,
            'razorpay_key': settings.RAZORPAY_API_KEY
        }
        
        return render(request, 'cart.html', context)
        
    except Exception as e:
        messages.error(request, f"Error loading cart: {str(e)}")
        return redirect('products')


def update_cart(request, item_id):
    if 'seller_id' in request.session:
        user = request.session['seller_id']
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
    # Get all designs
    designs = Design.objects.all()
    
    # Get user favorites
    user_favorites = []
    if request.user.is_authenticated:
        user_favorites = Favorite.objects.filter(
            user=request.user
        ).values_list('design_id', flat=True)
    
    context = {
        'designs': designs,
        'user_favorites': list(user_favorites),  # Convert to list for template
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


def remove_from_designer_cart(request, item_id):
    # Get the specific cart item and delete it
    item = get_object_or_404(DesignerCartItem, id=item_id, user=request.user)
    
    if request.method == 'POST':
        item.delete()
    
    return redirect('dcart')

def browse(request):
    return render(request, 'browse.html')

@login_required
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
    if 'seller_id' not in request.session:
        return JsonResponse({'success': False, 'error': 'Please log in first'}, status=401)
    try:
        user_id = request.session['seller_id']
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


@require_POST
def remove_from_favorites(request, design_id):
    if 'seller_id' not in request.session:
        return JsonResponse({
            'success': False,
            'error': 'Please log in first'
        }, status=401)
    
    user_id = request.session['seller_id']
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
    if 'seller_id' not in request.session:
        messages.error(request, "Please log in to view favorites")
        return redirect('login')
    
    user_id = request.session['seller_id']
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
                if 'seller_id' in request.session:
                    user_favorites = Favorite.objects.filter(
                        user_id=request.session['seller_id']
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
    
    count = Favorite.objects.filter(user_id=request.session.get('seller_id', 0)).count()
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
        'cart_count': CartItem.objects.filter(cart__user_id=request.session.get('seller_id', 0)).count()
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

def get_cart_count(request):
    try:
        cart = Cart.objects.get(user_id=request.session.get('seller_id'))
        cart_count = CartItem.objects.filter(cart=cart).count()
    except Cart.DoesNotExist:
        cart_count = 0
    return JsonResponse({'cart_count': cart_count})


def view_orders(request):
    try:
        # Get user ID from session
        user_id = request.session.get('seller_id')
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

# def company_register(request):
#     if request.method == 'POST':
#         try:
#             # Get passwords and verify they match
#             password = request.POST.get('password')
#             confirm_password = request.POST.get('confirm_password')
            
#             if not password:
#                 messages.error(request, 'Password is required!')
#                 return render(request, 'company_register.html')
                
#             if password != confirm_password:
#                 messages.error(request, 'Passwords do not match!')
#                 return render(request, 'company_register.html')
            
#             # Validate password strength
#             if len(password) < 8:
#                 messages.error(request, 'Password must be at least 8 characters long!')
#                 return render(request, 'company_register.html')
            
#             # Create user account with email as username
#             email = request.POST.get('email')
#             if User.objects.filter(email=email).exists():
#                 messages.error(request, 'Email already registered!')
#                 return render(request, 'company_register.html')
                
#             user = User.objects.create_user(
#                 username=email,
#                 email=email,
#                 password=password
#             )
            
#             # Create construction company profile
#             company = ConstructionCompany.objects.create(
#                 user=user,
#                 company_name=request.POST.get('company_name'),
#                 email=email,
#                 phone=request.POST.get('phone'),
#                 address=request.POST.get('address'),
#                 registration_number=request.POST.get('registration_number'),
#                 established_year=request.POST.get('established_year'),
#                 company_size=request.POST.get('company_size'),
#                 description=request.POST.get('description')
#             )
            
#             if 'logo' in request.FILES:
#                 company.logo = request.FILES['logo']
#                 company.save()
            
#             messages.success(request, 'Company registered successfully! Please login.')
#             return redirect('company_login')
            
#         except Exception as e:
#             if 'user' in locals():
#                 user.delete()
#             messages.error(request, f'Registration failed: {str(e)}')
            
#     return render(request, 'company_register.html')

# @login_required
# def company_login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
        
#         try:
#             company = ConstructionCompany.objects.get(email=email)
#             user = authenticate(username=company.user.username, password=password)
            
#             if user is not None:
#                 login(request, user)
#                 return redirect('company_dashboard')
#             else:
#                 messages.error(request, 'Invalid credentials')
#         except ConstructionCompany.DoesNotExist:
#             messages.error(request, 'Company not found')
        
#     return render(request, 'company_login.html')

# @login_required
# def company_change_password(request):
#     if request.method == 'POST':
#         old_password = request.POST.get('old_password')
#         new_password = request.POST.get('new_password')
#         confirm_password = request.POST.get('confirm_password')
        
#         if not request.user.check_password(old_password):
#             messages.error(request, 'Current password is incorrect!')
#             return redirect('company_change_password')
            
#         if new_password != confirm_password:
#             messages.error(request, 'New passwords do not match!')
#             return redirect('company_change_password')
            
#         if len(new_password) < 8:
#             messages.error(request, 'Password must be at least 8 characters long!')
#             return redirect('company_change_password')
            
#         # Change password
#         request.user.set_password(new_password)
#         request.user.save()
        
#         # Update session auth hash to prevent logout
#         update_session_auth_hash(request, request.user)
        
#         messages.success(request, 'Password changed successfully!')
#         return redirect('company_dashboard')
        
#     return render(request, 'company_change_password.html')

# @login_required
# def company_dashboard(request):
#     try:
#         company = ConstructionCompany.objects.get(user=request.user)
#         applications = TeamRequest.objects.filter(company=company).select_related('worker')
        
#         context = {
#             'company': company,
#             'applications': applications,
#             'pending_applications': applications.filter(status='pending').count(),
#             'accepted_applications': applications.filter(status='accepted').count(),
#             'total_applications': applications.count(),
#         }
#         return render(request, 'company_dashboard.html', context)
#     except ConstructionCompany.DoesNotExist:
#         messages.error(request, "Company profile not found")
#         return redirect('company_login')

# @login_required
# def handle_application(request, application_id, action):
#     try:
#         application = TeamRequest.objects.get(id=application_id)
        
#         if action == 'accept':
#             application.status = 'accepted'
#             # Update worker's company
#             application.worker.company = application.company
#             application.worker.save()
#             messages.success(request, f'Accepted {application.worker.full_name} to your team')
#         elif action == 'reject':
#             application.status = 'rejected'
#             messages.info(request, f'Rejected {application.worker.full_name}\'s application')
            
#         application.save()
        
#     except TeamRequest.DoesNotExist:
#         messages.error(request, 'Application not found')
#     except Exception as e:
#         messages.error(request, f'Error handling application: {str(e)}')
    
#     return redirect('company_dashboard')

@login_required
def submit_company_application(request, designer_id):
    if request.method == 'POST':
        try:
            designer = Designer.objects.get(id=designer_id)
            # Add your application submission logic here
            messages.success(request, 'Application submitted successfully!')
            return redirect('designer_dashboard')
        except Exception as e:
            messages.error(request, f'Error submitting application: {str(e)}')
            return redirect('designer_dashboard')
    return redirect('designer_dashboard')

@login_required
def view_designers(request):
    # Get all designers with their profiles
    designers = Designer.objects.select_related('user').all()
    
    # Get filter parameters
    specialization = request.GET.get('specialization')
    experience = request.GET.get('experience')
    rating = request.GET.get('rating')
    
    # Apply filters if they exist
    if specialization:
        designers = designers.filter(specialization=specialization)
    if experience:
        designers = designers.filter(experience_years__gte=experience)
    if rating:
        designers = designers.filter(rating__gte=rating)
    
    context = {
        'designers': designers,
        'specializations': Designer.objects.values_list('specialization', flat=True).distinct(),
        'experience_ranges': [
            {'label': '0-2 years', 'value': 0},
            {'label': '2-5 years', 'value': 2},
            {'label': '5+ years', 'value': 5}
        ],
        'rating_ranges': [
            {'label': '4+ stars', 'value': 4},
            {'label': '3+ stars', 'value': 3},
            {'label': 'All ratings', 'value': 0}
        ]
    }
    return render(request, 'designers.html', context)

@login_required
def view_designs(request):
    # Get all designs with their designers
    designs = Design.objects.select_related('designer').all()
    
    # Get filter parameters
    style = request.GET.get('style')
    room_type = request.GET.get('room_type')
    
    # Apply filters if they exist
    if style:
        designs = designs.filter(style=style)
    if room_type:
        designs = designs.filter(room_type=room_type)
    
    context = {
        'designs': designs,
        'room_types': Design.ROOM_TYPE_CHOICES,
        'styles': Design.STYLE_CHOICES
    }
    
    return render(request, 'view_designs.html', context)

@login_required
def filter_designs(request):
    designs = Design.objects.all()
    
    # Get filter parameters from request
    filters = {}
    if request.GET.get('style'):
        filters['style'] = request.GET.get('style')
    if request.GET.get('room_type'):
        filters['room_type'] = request.GET.get('room_type')
    if request.GET.get('min_price'):
        filters['price__gte'] = request.GET.get('min_price')
    if request.GET.get('max_price'):
        filters['price__lte'] = request.GET.get('max_price')
    
    # Apply filters
    designs = designs.filter(**filters)
    
    # Return filtered designs as JSON
    designs_data = [{
        'id': design.id,
        'title': design.title,
        'description': design.description,
        'price': str(design.price),
        'image_url': design.image.url if design.image else None,
        'designer_name': design.designer.full_name,
        'style': design.style,
        'room_type': design.room_type,
    } for design in designs]
    
    return JsonResponse({'designs': designs_data})

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check against predefined credentials
        if username == 'jerry' and password == 'jerry@123':
            # Store admin session
            request.session['is_admin'] = True
            messages.success(request, 'Welcome Admin!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('admin_login')
    
    return render(request, 'admin_login.html')

# Add admin_required decorator
def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.session.get('is_admin'):
            return view_func(request, *args, **kwargs)
        return redirect('admin_login')
    return _wrapped_view

@admin_required
def admin_dashboard(request):
    # Check if user is admin
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    # Get all companies for the admin dashboard
    companies = Company.objects.all().order_by('-created_at')
    
    # Add companies to the context
    context = {
        'total_users': User.objects.count(),
        'total_workers': Worker.objects.count(),
        'total_designs': Design.objects.count(),
        'completed_projects': CompanyAssignment.objects.filter(status='completed').count(),
        'companies': companies,
    }
    
    return render(request, 'admin_dashboard.html', context)

@login_required
def admin_logout(request):
    if request.user.is_superuser:
        logout(request)
        messages.success(request, 'Successfully logged out from admin panel')
    return redirect('admin_login')

@login_required
def admin_users(request):
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    users = User.objects.all().order_by('-date_joined')
    context = {
        'users': users
    }
    return render(request, 'admin_users.html', context)

@login_required
def filter_users(request):
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    role = request.GET.get('role', '')
    users = User.objects.all()
    
    if role:
        if role == 'designer':
            users = users.filter(designer__isnull=False)
        elif role == 'customer':
            users = users.filter(designer__isnull=True, is_staff=False)
    
    users_data = [{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'date_joined': user.date_joined.strftime('%Y-%m-%d'),
        'is_active': user.is_active,
        'role': 'Designer' if hasattr(user, 'designer') else 'Customer'
    } for user in users]
    
    return JsonResponse({'users': users_data})

@login_required
def edit_profile(request):
    try:
        designer = Designer.objects.get(user=request.user)
        
        if request.method == 'POST':
            # Update designer profile
            designer.full_name = request.POST.get('full_name')
            designer.phone = request.POST.get('phone')
            designer.specialization = request.POST.get('specialization')
            designer.experience_years = request.POST.get('experience_years')
            designer.bio = request.POST.get('bio')
            
            # Handle profile picture upload
            if 'profile_picture' in request.FILES:
                designer.profile_picture = request.FILES['profile_picture']
            
            # Handle portfolio images
            if 'portfolio_images' in request.FILES:
                for image in request.FILES.getlist('portfolio_images'):
                    PortfolioImage.objects.create(
                        designer=designer,
                        image=image
                    )
            
            designer.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('designer_dashboard')
            
        context = {
            'designer': designer,
            'portfolio_images': designer.portfolioimages.all() if hasattr(designer, 'portfolioimages') else None,
            'specializations': [
                'Interior Design',
                'Residential Design',
                'Commercial Design',
                'Sustainable Design',
                'Modern Design',
                'Traditional Design',
                'Industrial Design',
                'Minimalist Design'
            ]
        }
        return render(request, 'edit_profile.html', context)
        
    except Designer.DoesNotExist:
        messages.error(request, 'Designer profile not found')
        return redirect('home')
    except Exception as e:
        messages.error(request, f'Error updating profile: {str(e)}')
        return redirect('designer_dashboard')

@admin_required
def admin_add_company(request):
    if request.method == 'POST':
        try:
            # Create company
            company = Company.objects.create(
                name=request.POST.get('company_name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                address=request.POST.get('address'),
                established_year=request.POST.get('established_year'),
                description=request.POST.get('description')
            )
            
            # Handle logo upload
            if 'logo' in request.FILES:
                company.logo = request.FILES['logo']
                company.save()
            
            # Handle workers
            worker_names = request.POST.getlist('worker_names[]')
            worker_skills = request.POST.getlist('worker_skills[]')
            worker_experience = request.POST.getlist('worker_experience[]')
            
            for i in range(len(worker_names)):
                Worker.objects.create(
                    company=company,
                    name=worker_names[i],
                    skill=worker_skills[i],
                    experience_years=worker_experience[i]
                )
            
            messages.success(request, 'Company added successfully!')
            return redirect('admin_dashboard')
            
        except Exception as e:
            messages.error(request, f'Error adding company: {str(e)}')
            return redirect('admin_add_company')
    
    return render(request, 'admin_add_company.html')

def shome(request):
    seller_id = request.session.get('seller_id')
    if not seller_id:
        messages.error(request, 'You need to login first.')
        return redirect('slogin')
        
    try:
        seller = Seller.objects.get(id=seller_id)
        products = Product.objects.filter(seller=seller)
        context = {
            'seller': seller,
            'products': products
        }
        return render(request, 'shome.html', context)
        
    except Seller.DoesNotExist:
        messages.error(request, 'Seller not found.')
        return redirect('slogin')

def designer_logout(request):
    # Clear designer-specific session data
    request.session.pop('designer_id', None)
    request.session.pop('role', None)
    request.session.pop('is_designer', None)
    messages.success(request, 'Logged out successfully')
    return redirect('dlogin')

@login_required
def user_dashboard(request):
    # Get user's consultations, favorites, and orders
    consultations = Consultation.objects.filter(user=request.user).order_by('-created_at')
    favorite_designs = Design.objects.filter(favorited_by=request.user)
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'consultations': consultations,
        'favorite_designs': favorite_designs,
        'orders': orders,
        'pending_consultations': consultations.filter(status='pending').count(),
        'approved_consultations': consultations.filter(status='approved').count(),
        'total_orders': orders.count()
    }
    return render(request, 'user_dashboard.html', context)

def book_consultation(request, design_id):
    if request.method == 'POST':
        try:
            design = Design.objects.get(id=design_id)
            consultation = Consultation.objects.create(
                user=request.user,
                designer=design.designer,
                design=design,
                preferred_date=request.POST.get('preferred_date'),
                preferred_time=request.POST.get('preferred_time'),
                consultation_method=request.POST.get('consultation_method'),
                notes=request.POST.get('notes')
            )
            return JsonResponse({
                'success': True,
                'message': 'Consultation request submitted successfully!'
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


def view_consultations(request):
    consultations = Consultation.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user_consultations.html', {'consultations': consultations})


def assign_company_work(request):
    # Get all companies
    companies = Company.objects.all()
    
    if request.method == 'POST':
        # Process form submission
        company_id = request.POST.get('company')
        company = Company.objects.get(id=company_id)
        
        # Create a new company assignment
        assignment = CompanyAssignment(
            designer=request.user,
            company=company,
            client_name=request.POST.get('full_name'),
            client_email=request.POST.get('email'),
            client_phone=request.POST.get('phone'),
            room_type=request.POST.get('room_type'),
            design_name=request.POST.get('design_name'),
            design_style=request.POST.get('design_style'),
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            milestones=request.POST.get('milestones'),
            update_frequency=request.POST.get('update_frequency'),
            communication_method=','.join(request.POST.getlist('communication_method')),
            meeting_times=request.POST.get('meeting_times'),
            additional_notes=request.POST.get('additional_notes')
        )
        assignment.save()
        
        messages.success(request, 'Work assignment submitted successfully!')
        return redirect('designer_dashboard')
    
    context = {
        'companies': companies
    }
    return render(request, 'assign_company_work.html', context)

# Company views
def company_register(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        description = request.POST.get('description')
        license_number = request.POST.get('license_number')
        logo = request.FILES.get('logo')
        
        # Validate form data
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('company_register')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('company_register')
        
        # Create user account
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )
        
        # Create company profile
        company = Company.objects.create(
            user=user,
            company_name=company_name,
            email=email,
            phone=phone,
            address=address,
            description=description,
            license_number=license_number,
            logo=logo,
            status='pending'  # Pending admin approval
        )
        
        messages.success(request, 'Registration successful! Your account is pending approval.')
        return redirect('company_login')
    
    return render(request, 'company_register.html')

def company_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        
        # Authenticate user
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            # Check if user has a company profile
            try:
                company = Company.objects.get(user=user)
                
                # Log in the user
                login(request, user)
                
                # Set session expiry if remember me is checked
                if not remember:
                    request.session.set_expiry(0)
                
                return redirect('company_dashboard')
            except Company.DoesNotExist:
                messages.error(request, 'No company profile found for this account.')
                return redirect('company_login')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('company_login')
    
    return render(request, 'company_login.html')


@login_required
def company_dashboard(request):
    try:
        company = Company.objects.get(user=request.user)
    except Company.DoesNotExist:
        messages.error(request, 'No company profile found for this account.')
        return redirect('home')
    
    # Get company assignments
    assignments = CompanyAssignment.objects.filter(company=company)
    
    # Get consultation requests
    consultation_requests = DesignerConsultationRequest.objects.filter(company=company).order_by('-created_at')
    
    # Count assignments by status
    pending_assignments = assignments.filter(status='pending').count()
    in_progress_assignments = assignments.filter(status='in_progress').count()
    completed_assignments = assignments.filter(status='completed').count()
    
    # Get recent assignments
    recent_assignments = assignments.order_by('-created_at')[:5]
    
    context = {
        'company': company,
        'total_assignments': assignments.count(),
        'pending_assignments': pending_assignments,
        'in_progress_assignments': in_progress_assignments,
        'completed_assignments': completed_assignments,
        'recent_assignments': recent_assignments,
        'consultation_requests': consultation_requests
    }
    
    return render(request, 'company_dashboard.html', context)

@login_required
def company_projects(request):
    try:
        company = Company.objects.get(user=request.user)
    except Company.DoesNotExist:
        messages.error(request, 'No company profile found for this account.')
        return redirect('home')
    
    # Get all company assignments
    assignments = CompanyAssignment.objects.filter(company=company).order_by('-created_at')
    
    context = {
        'company': company,
        'assignments': assignments
    }
    
    return render(request, 'company_projects.html', context)

@login_required
def company_project_detail(request, assignment_id):
    try:
        company = Company.objects.get(user=request.user)
        assignment = CompanyAssignment.objects.get(id=assignment_id, company=company)
    except (Company.DoesNotExist, CompanyAssignment.DoesNotExist):
        messages.error(request, 'Project not found.')
        return redirect('company_dashboard')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'accept':
            assignment.status = 'in_progress'
            assignment.save()
            messages.success(request, 'Project accepted successfully.')
        elif action == 'complete':
            assignment.status = 'completed'
            assignment.save()
            messages.success(request, 'Project marked as completed.')
        elif action == 'reject':
            assignment.status = 'rejected'
            assignment.save()
            messages.warning(request, 'Project rejected.')
    
    context = {
        'company': company,
        'assignment': assignment
    }
    
    return render(request, 'company_project_detail.html', context)

@login_required
def company_profile(request):
    try:
        company = Company.objects.get(user=request.user)
    except Company.DoesNotExist:
        messages.error(request, 'No company profile found for this account.')
        return redirect('home')
    
    if request.method == 'POST':
        company.company_name = request.POST.get('company_name')
        company.phone = request.POST.get('phone')
        company.address = request.POST.get('address')
        company.description = request.POST.get('description')
        
        if 'logo' in request.FILES:
            company.logo = request.FILES['logo']
        
        company.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('company_profile')
    
    context = {
        'company': company
    }
    
    return render(request, 'company_profile.html', context)

@login_required
def company_change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Check if current password is correct
        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('company_change_password')
        
        # Check if new passwords match
        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
            return redirect('company_change_password')
        
        # Update password
        request.user.set_password(new_password)
        request.user.save()
        
        # Update session to prevent logout
        update_session_auth_hash(request, request.user)
        
        messages.success(request, 'Password changed successfully.')
        return redirect('company_dashboard')
    
    return render(request, 'company_change_password.html')

@login_required
def admin_view_company(request, company_id):
    # Check if user is admin
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        messages.error(request, 'Company not found.')
        return redirect('admin_dashboard')
    
    # Get company assignments
    assignments = CompanyAssignment.objects.filter(company=company).order_by('-created_at')
    
    context = {
        'company': company,
        'assignments': assignments
    }
    
    return render(request, 'admin_view_company.html', context)

@login_required
def admin_delete_company(request, company_id):
    # Check if user is admin
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    try:
        company = Company.objects.get(id=company_id)
        user = company.user
        
        # Delete the company and associated user
        company.delete()
        user.delete()
        
        messages.success(request, f'Company "{company.company_name}" has been deleted successfully.')
    except Company.DoesNotExist:
        messages.error(request, 'Company not found.')
    
    return redirect('admin_dashboard')

def customer_dashboard(request):
    # Your customer dashboard logic here
    return render(request, 'customer_dashboard.html')

@login_required
def company_workers(request):
    try:
        company = Company.objects.get(user=request.user)
    except Company.DoesNotExist:
        messages.error(request, 'No company profile found for this account.')
        return redirect('home')
    
    # Get all workers for this company - updated to use company_workers
    workers = CompanyWorker.objects.filter(company=company).order_by('-created_at')
    
    context = {
        'company': company,
        'workers': workers
    }
    
    return render(request, 'company_workers.html', context)

@login_required
def add_worker(request):
    try:
        company = Company.objects.get(user=request.user)
    except Company.DoesNotExist:
        messages.error(request, 'No company profile found for this account.')
        return redirect('home')
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        age = request.POST.get('age')
        experience = request.POST.get('experience')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        specialization = request.POST.get('specialization')
        image = request.FILES.get('image')
        
        # Create new worker
        worker = CompanyWorker.objects.create(
            company=company,
            full_name=full_name,
            age=age,
            experience=experience,
            phone=phone,
            email=email,
            specialization=specialization,
            image=image
        )
        
        messages.success(request, 'Worker added successfully!')
        return redirect('company_workers')
    
    context = {
        'company': company,
        'specialization_choices': CompanyWorker.SPECIALIZATION_CHOICES
    }
    
    return render(request, 'add_worker.html', context)

@login_required
def edit_worker(request, worker_id):
    try:
        company = Company.objects.get(user=request.user)
        worker = CompanyWorker.objects.get(id=worker_id, company=company)
    except (Company.DoesNotExist, CompanyWorker.DoesNotExist):
        messages.error(request, 'Worker not found.')
        return redirect('company_workers')
    
    if request.method == 'POST':
        worker.full_name = request.POST.get('full_name')
        worker.age = request.POST.get('age')
        worker.experience = request.POST.get('experience')
        worker.phone = request.POST.get('phone')
        worker.email = request.POST.get('email')
        worker.specialization = request.POST.get('specialization')
        
        if 'image' in request.FILES:
            worker.image = request.FILES['image']
        
        worker.save()
        messages.success(request, 'Worker updated successfully!')
        return redirect('company_workers')
    
    context = {
        'company': company,
        'worker': worker,
        'specialization_choices': CompanyWorker.SPECIALIZATION_CHOICES
    }
    
    return render(request, 'edit_worker.html', context)

@login_required
def delete_worker(request, worker_id):
    try:
        company = Company.objects.get(user=request.user)
        worker = CompanyWorker.objects.get(id=worker_id, company=company)
    except (Company.DoesNotExist, CompanyWorker.DoesNotExist):
        messages.error(request, 'Worker not found.')
        return redirect('company_workers')
    
    worker.delete()
    messages.success(request, 'Worker deleted successfully!')
    return redirect('company_workers')

@designer_login_required  # Use designer_login_required instead of login_required
def designer_request_consultation(request):
    if request.method == 'POST':
        try:
            # Get designer from session instead of request.user
            designer_id = request.session.get('designer_id')
            if not designer_id:
                messages.error(request, 'Designer session not found.')
                return redirect('dlogin')
                
            designer = Designer.objects.get(id=designer_id)
            
            company_id = request.POST.get('company_id')
            user_id = request.POST.get('user_id')
            design_name = request.POST.get('design_name')
            # client_name is commented out in the form, so we'll use the user's name
            room_type = request.POST.get('room_type')
            budget = request.POST.get('budget')
            preferred_date = request.POST.get('preferred_date')
            preferred_time = request.POST.get('preferred_time')
            
            # Get company and user
            company = Company.objects.get(id=company_id)
            user = User.objects.get(id=user_id)
            
            # Create consultation request
            consultation = DesignerConsultationRequest.objects.create(
                designer=designer,
                company=company,
                user=user,
                design_name=design_name,
                client_name=user.get_full_name() or user.username,  # Use user's name
                room_type=room_type,
                budget=budget,
                preferred_date=preferred_date,
                preferred_time=preferred_time
            )
            
            # Create notification for company
            Notification.objects.create(
                user=company.user,
                title="New Consultation Request",
                message=f"Designer {designer.full_name} has requested a consultation for project '{design_name}'.",
                notification_type="consultation_request"
            )
            
            messages.success(request, "Consultation request sent successfully!")
            return redirect('designer_dashboard')
            
        except (Designer.DoesNotExist, Company.DoesNotExist, User.DoesNotExist) as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('designer_dashboard')
    
    return redirect('designer_dashboard')

@login_required
def company_respond_consultation(request, consultation_id, action):
    if request.method == 'POST':
        try:
            company = Company.objects.get(user=request.user)
            consultation = DesignerConsultationRequest.objects.get(id=consultation_id, company=company)
            
            if action == 'accept':
                consultation.status = 'accepted'
                status_text = 'accepted'
            elif action == 'decline':
                consultation.status = 'declined'
                status_text = 'declined'
            else:
                messages.error(request, "Invalid action.")
                return redirect('company_dashboard')
            
            consultation.save()
            
            # Create notification for designer - but don't try to access designer.user
            # Instead, store notifications in a different way or check if the attribute exists
            
            # For now, we'll skip the designer notification since Designer doesn't have user
            
            # Create notification for user (client) if user is not None
            if consultation.user:
                Notification.objects.create(
                    user=consultation.user,
                    title=f"Consultation Update",
                    message=f"Your consultation request for '{consultation.design_name}' has been {status_text} by {company.company_name}.",
                    notification_type="consultation_update"
                )
            
            messages.success(request, f"Consultation request {status_text} successfully.")
            
        except (Company.DoesNotExist, DesignerConsultationRequest.DoesNotExist) as e:
            messages.error(request, f"Error: {str(e)}")
    
    return redirect('company_dashboard')

@login_required
def company_view_consultation(request, consultation_id):
    try:
        company = Company.objects.get(user=request.user)
        consultation = DesignerConsultationRequest.objects.get(id=consultation_id, company=company)
        
        if request.method == 'POST':
            completion_percentage = request.POST.get('completion_percentage')
            if completion_percentage:
                consultation.completion_percentage = int(completion_percentage)
                if consultation.completion_percentage == 100:
                    consultation.status = 'completed'
                consultation.save()
                
                # Create notification for designer and user
                Notification.objects.create(
                    user=consultation.designer.user,
                    title="Project Progress Update",
                    message=f"Project '{consultation.design_name}' is now {consultation.completion_percentage}% complete.",
                    notification_type="project_update"
                )
                
                Notification.objects.create(
                    user=consultation.user,
                    title="Project Progress Update",
                    message=f"Your project '{consultation.design_name}' is now {consultation.completion_percentage}% complete.",
                    notification_type="project_update"
                )
                
                messages.success(request, "Progress updated successfully.")
                return redirect('company_view_consultation', consultation_id=consultation.id)
        
        context = {
            'company': company,
            'consultation': consultation
        }
        
        return render(request, 'company_view_consultation.html', context)
        
    except (Company.DoesNotExist, DesignerConsultationRequest.DoesNotExist) as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect('company_dashboard')

def designer_view_consultation(request, consultation_id):
    try:
        designer = Designer.objects.get(user=request.user)
        consultation = DesignerConsultationRequest.objects.get(id=consultation_id, designer=designer)
        
        context = {
            'designer': designer,
            'consultation': consultation
        }
        
        return render(request, 'designer_view_consultation.html', context)
        
    except (Designer.DoesNotExist, DesignerConsultationRequest.DoesNotExist) as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect('designer_dashboard')

@designer_login_required
def assign_company_work(request):
    if request.method == 'POST':
        try:
            # Get designer from session instead of request.user
            designer_id = request.session.get('designer_id')
            if not designer_id:
                messages.error(request, 'Designer session not found.')
                return redirect('dlogin')
                
            designer = Designer.objects.get(id=designer_id)
            
            company_id = request.POST.get('company_id')
            project_name = request.POST.get('project_name')
            description = request.POST.get('description')
            budget = request.POST.get('budget')
            deadline = request.POST.get('deadline')
            
            # Get company
            company = Company.objects.get(id=company_id)
            
            # Create assignment
            assignment = CompanyAssignment.objects.create(
                designer=designer,  # Use designer object, not request.user
                company=company,
                project_name=project_name,
                description=description,
                budget=budget,
                deadline=deadline
            )
            
            # Create notification for company
            Notification.objects.create(
                user=company.user,
                title="New Project Assignment",
                message=f"Designer {designer.full_name} has assigned a new project '{project_name}' to your company.",
                notification_type="project_assignment"
            )
            
            messages.success(request, "Project assigned successfully!")
            return redirect('designer_dashboard')
            
        except (Designer.DoesNotExist, Company.DoesNotExist) as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('designer_dashboard')
    
    # GET request - show form
    # Make sure we're getting ALL companies that are approved
    companies = Company.objects.filter(status='approved')
    
    # Add debug information to check if companies are being fetched
    print(f"Found {companies.count()} approved companies")
    
    # Pass companies to the template
    return render(request, 'assign_company_work.html', {'companies': companies})

# Try getting all companies without filtering by status
companies = Company.objects.all()
print(f"Found {companies.count()} total companies")