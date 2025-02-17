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

# Add a new product (without form)
def add_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        category = request.POST.get('category')
        image = request.FILES.get('image')
        seller_id = request.session['id']
        seller = Seller.objects.get(id = seller_id)

        if product_name and price and stock:  # Simple validation
            product = Product(
                seller=seller,
                product_name=product_name,
                description=description,
                price=price,
                stock=stock,
                image=image,
            )
            product.save()
            messages.success(request, 'Product added successfully.')
            return redirect('shome')
        else:
            messages.error(request, 'All fields are required.')
    
    return render(request, 'addnewproduct.html')

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
        full_name = request.POST['full_name']
        email = request.POST['email']
        phone = request.POST['phone']
        username = request.POST['username']
        password = request.POST['password']

        # Validate first name
        if not full_name[0].isupper():
            return render(request, 'dregister.html', {'error': 'First name must start with a capital letter.'})

        # Validate phone number
        if len(phone) != 10 or not phone.isdigit():
            return render(request, 'dregister.html', {'error': 'Phone number must be 10 digits.'})

        # Check if profile_picture is in request.FILES
        if 'profile_picture' in request.FILES:
            profile_picture = request.FILES['profile_picture']  # Get the uploaded file
        else:
            return render(request, 'dregister.html', {'error': 'Profile picture is required.'})

        # Create User instance
        user = Designer.objects.create(username=username, email=email, password=password)
        first_name, last_name = full_name.split(' ', 1) if ' ' in full_name else (full_name, '')
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Create UserProfile instance and set is_designer to True
        user_profile = UserProfile.objects.create(user=user, phone=phone, is_designer=True)
        user_profile.profile_picture = profile_picture  # Save the profile picture
        user_profile.save()

        return redirect('dlogin')  # Redirect to login or another page after registration

    return render(request, 'dregister.html')


def dlogin_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            # Check if designer exists in the custom Designer table
            designer = Designer.objects.get(username=username)
            
            # Validate the password directly (note: this is not secure)
            if designer.password == password:  # Direct comparison
                # Log the user in (manual login)
                request.session['designer_id'] = designer.id  # Save designer's ID in session
                messages.success(request, 'Login successful!')
                return redirect('dhome')  # Redirect to designer's home/dashboard page
            else:
                messages.error(request, 'Invalid username or password')
        except Designer.DoesNotExist:
            messages.error(request, 'Invalid username or password')

    return render(request, 'dlogin.html')

def add_design(request):
    if request.method == 'POST':
        try:
            # Get the designer from the session
            designer_id = request.session.get('designer_id')
            if not designer_id:
                messages.error(request, 'Please login as a designer first')
                return redirect('dlogin')
            
            designer = Designer.objects.get(id=designer_id)

            # Create the design
            design = Design(
                designer=designer,
                design_name=request.POST.get('design_name'),
                description=request.POST.get('description'),
                category=request.POST.get('category'),
                image=request.FILES.get('image')
            )
            design.save()

            messages.success(request, 'Design added successfully!')
            return redirect('dhome')  # Redirect to designs page

        except Designer.DoesNotExist:
            messages.error(request, 'Designer not found')
            return redirect('dlogin')
        except Exception as e:
            messages.error(request, f'Error adding design: {str(e)}')
            return render(request, 'add_design.html')

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
def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return JsonResponse({
            'success': False,
            'message': "Please login to add items to cart"
        })

    try:
        product = get_object_or_404(Product, id=product_id)
        cart, _ = Cart.objects.get_or_create(user_id=request.user.id)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 1}
        )
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        cart_count = CartItem.objects.filter(cart=cart).aggregate(
            total_items=Sum('quantity'))['total_items'] or 0

        return JsonResponse({
            'success': True,
            'message': f"{product.product_name} has been added to your cart",
            'cartCount': cart_count
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })

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

def cart_view(request):
    user = request.session['id']
    try:
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        context = {
            'cart_items': cart_items,
            'total_price': total_price,
            'delivery_charges': 50,
            'razorpay_key': settings.RAZORPAY_API_KEY
        }
        return render(request, 'cart.html', context)
    except Cart.DoesNotExist:
        return render(request, 'cart.html', {'razorpay_key': settings.RAZORPAY_API_KEY})

# View to remove product from cart
@login_required
def remove_from_cart(request, item_id):
    user = request.session['id']
    cart_item = get_object_or_404(CartItem, id=item_id, user=user)
    cart_item.delete()
    messages.success(request, "Product removed from cart.")
    return redirect('cart')

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
    kitchen_designs = Design.objects.filter(category='Kitchen')
    print(f"Number of kitchen designs fetched: {kitchen_designs.count()}")  # Debugging line
    return render(request, 'kitchen_designs.html', {'kitchen_designs': kitchen_designs})

def living_room_designs(request):
    living_room_designs = Design.objects.filter(category='Living Room')
    return render(request, 'living_room_designs.html', {'living_room_designs': living_room_designs})

def bedroom_designs(request):
    bedroom_designs = Design.objects.filter(category='Bedroom')
    return render(request, 'bedroom_designs.html', {'bedroom_designs': bedroom_designs})

def bathroom_designs(request):
    bathroom_designs = Design.objects.filter(category='Bathroom')
    return render(request, 'bathroom_designs.html', {'bathroom_designs': bathroom_designs})

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
    dining_room_designs = Design.objects.filter(category='Dining Room')
    return render(request, 'dining_room_designs.html', {'dining_room_designs': dining_room_designs})

def business_office_designs(request):
    business_office_designs = Design.objects.filter(category='Business Office')
    return render(request, 'business_office_designs.html', {'business_office_designs': business_office_designs})

def hallway_entry_designs(request):
    hallway_entry_designs = Design.objects.filter(category='Hallway/Entry')
    return render(request, 'hallway_entry_designs.html', {'hallway_entry_designs': hallway_entry_designs})

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
                    Q(category__icontains=query)
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
                    'category': design.category,
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
                }, status=500)
    
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
    
    if category:
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
    } for product in products[:12]]  # Limit to 12 products for performance
    
    return JsonResponse({
        'products': products_data,
        'total_count': products.count()
    })

def create_order(request):
    if request.method == "POST":
        try:
            # Initialize Razorpay client
            client = razorpay.Client(
                auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET)
            )

            # Get cart total
            user = request.session.get('id')
            cart = Cart.objects.get(user=user)
            cart_items = CartItem.objects.filter(cart=cart)
            total_amount = sum(item.product.price * item.quantity for item in cart_items)
            total_amount += 50  # Add delivery charges
            
            try:
                # Create Razorpay Order
                payment = client.order.create({
                    "amount": int(total_amount * 100),  # Amount in paise
                    "currency": "INR",
                    "payment_capture": "1"
                })
                
                return JsonResponse({
                    "success": True,
                    "order_id": payment['id'],
                    "amount": payment['amount']
                })
            except requests.exceptions.ConnectionError as e:
                print(f"Connection Error: {str(e)}")
                return JsonResponse({
                    "success": False,
                    "error": "Unable to connect to payment service. Please check your internet connection."
                })
            except razorpay.errors.BadRequestError as e:
                print(f"Razorpay Error: {str(e)}")
                return JsonResponse({
                    "success": False,
                    "error": "Invalid payment request. Please try again."
                })
            except Exception as e:
                print(f"Order Creation Error: {str(e)}")
                return JsonResponse({
                    "success": False,
                    "error": "Error creating order. Please try again later."
                })
                
        except Exception as e:
            print(f"General Error: {str(e)}")
            return JsonResponse({
                "success": False,
                "error": str(e)
            })
    
    return JsonResponse({
        "success": False,
        "error": "Invalid request method"
    })

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        try:
            # Get the payment data
            payment_data = json.loads(request.body)
            print("Payment Data:", payment_data)  # Debug print
            
            # Verify payment signature
            params_dict = {
                'razorpay_payment_id': payment_data.get('razorpay_payment_id'),
                'razorpay_order_id': payment_data.get('razorpay_order_id'),
                'razorpay_signature': payment_data.get('razorpay_signature')
            }
            
            try:
                # Verify the payment signature
                razorpay_client.utility.verify_payment_signature(params_dict)
            except Exception as e:
                print("Signature verification failed:", str(e))  # Debug print
                return JsonResponse({
                    "success": False,
                    "error": "Payment signature verification failed"
                })
            
            # Get user and cart
            user_id = request.session.get('id')
            if not user_id:
                return JsonResponse({"success": False, "error": "User not logged in"})
            
            cart = Cart.objects.get(user_id=user_id)
            cart_items = CartItem.objects.filter(cart=cart)
            
            if not cart_items.exists():
                return JsonResponse({"success": False, "error": "Cart is empty"})
            
            # Calculate total amount
            total_amount = sum(item.quantity * item.product.price for item in cart_items)
            total_amount += 50  # Add delivery charges
            
            try:
                # Create order
                order = Order.objects.create(
                    user_id=user_id,
                    payment_id=payment_data['razorpay_payment_id'],
                    razorpay_order_id=payment_data['razorpay_order_id'],
                    amount=total_amount,
                    status='Completed'
                )
                
                # Create order items
                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        price=cart_item.product.price
                    )
                
                # Clear the cart
                cart_items.delete()
                
                return JsonResponse({
                    "success": True,
                    "message": "Payment successful and order created",
                    "order_id": order.id
                })
                
            except Exception as e:
                print("Error creating order:", str(e))  # Debug print
                return JsonResponse({
                    "success": False,
                    "error": "Error creating order: " + str(e)
                })
            
        except Exception as e:
            print("Payment processing error:", str(e))  # Debug print
            return JsonResponse({
                "success": False,
                "error": str(e)
            })
    
    return JsonResponse({"success": False, "error": "Invalid request method"})

@login_required
def payment_success_page(request):
    try:
        # Get user ID from session
        user_id = request.session.get('id')
        if not user_id:
            messages.error(request, 'Please log in to view your orders')
            return redirect('login')

        # Get all orders for the current user
        orders = Order.objects.filter(user_id=user_id).order_by('-created_at')
        
        # Debug print to help diagnose issues
        print(f"User ID: {user_id}, Found orders: {orders.count()}")
        
        # Get order items for each order
        orders_with_items = []
        for order in orders:
            try:
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
                print(f"Order {order.id}: {order_items.count()} items, total: {order.amount}")
            except Exception as e:
                print(f"Error processing order {order.id}: {str(e)}")
                continue

        return render(request, 'payment_success.html', {
            'orders_with_items': orders_with_items,
            'user_id': user_id
        })
        
    except Exception as e:
        print(f"Error in payment_success_page: {str(e)}")
        messages.error(request, f'Error fetching orders: {str(e)}')
        return redirect('products')

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