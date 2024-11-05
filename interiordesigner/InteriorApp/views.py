from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .models import UserProfile, Portfolio
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

def dregister_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if username or email already exists
        if Designer.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        elif Designer.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
        else:
            # Create a new Designer with hashed password
            designer = Designer(
                full_name=full_name,
                email=email,
                phone=phone,
                username=username,
                password=password  # Hash the password before saving
            )
            designer.save()
            
            messages.success(request, 'Registration successful!')
            return redirect('dlogin')  # Redirect to login page after successful registration

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
        # Get data from the form
        design_name = request.POST['design_name']
        price = request.POST['price']
        # origin = request.POST['origin']
        description = request.POST.get('description', '')  # Optional field
        design_image = request.FILES.get('image')  # Image file

        # Create a new Design instance
        design = Design(
            design_name=design_name,
            price=price,
            # origin=origin,
            description=description,
            image=design_image
        )

        # Save the design to the database
        design.save()

        messages.success(request, 'Design added successfully!')
        return redirect('dhome')  # Redirect to a home or portfolio page after adding

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
    # Here you will add the product to the user's cart (this depends on your cart logic)
    product = get_object_or_404(Product, id=product_id)
    user = request.session['id']
    # Assuming you have a Cart model or session-based cart
    cart, created = Cart.objects.get_or_create(user=user)
    print(cart.id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        # If the cart item already exists, increment the quantity
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

# Cart view - display items in cart
#  def cart_view(request):
#      cart_product_ids = request.session.get('cart', [])
#      cart_products = Product.objects.filter(id__in=cart_product_ids)
#      return render(request, 'cart.html', {'cart_products': cart_products})

# # Favorites view
# def favorites_view(request):
#     # Assuming you are storing favorites in the session or in a database model
#     favorite_product_ids = request.session.get('favorites', [])
#     favorite_products = Product.objects.filter(id__in=favorite_product_ids)
#     return render(request, 'favorites.html', {'favorite_products': favorite_products})

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
    print(user)
    try:
        cart = Cart.objects.get(user=user)
        print(cart)
        cart_items = CartItem.objects.filter(cart=cart)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        context = {
            'cart_items': cart_items,
            'total_price': total_price,
            'delivery_charges': 50  # You can customize delivery charges or add logic based on cart total
        }
        return render(request, 'cart.html', context)
    except Cart.DoesNotExist:
        return render(request, 'cart.html')

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
    designs = Design.objects.all()  # Get all designs from the database
    return render(request, 'realhome.html', {'designs': designs})

# Designers Page View
def designers_page(request):
    # Logic for listing designers can go here (e.g., querying a Designer model)
    return render(request, 'dhome.html')

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