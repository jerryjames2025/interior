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

def home(request):
    return render(request, 'home.html')

def print_hello(request):
    return HttpResponse("Hello")

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            messages.error(request, 'Both username and password are required.')
            return render(request, 'loginn.html')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('userhome') 
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'loginn.html')

def registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, 'Registration successful. You can now log in.')
        return redirect('login')

    return render(request, 'registration.html')

def portfolio(request):
    return render(request, 'portfolio.html')

def userhome(request):
    return render(request, 'user_home.html')

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