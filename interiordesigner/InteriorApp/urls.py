
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('reg/', views.registration, name='registration'),
    path('port/', views.portfolio, name='portfolio'),
    path('register/', views.registration, name='register'),
    path('userhome/', views.userhome, name='userhome'),
    path('forgotpas/', views.forgotpass, name='forgotpassword'),
    path('resetpas/<uidb64>/<token>/',views.resetpass, name='resetpassword'),
]


