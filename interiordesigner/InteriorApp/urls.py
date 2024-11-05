
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.conf import settings
from django.conf.urls.static import static

class CustomLogoutView(auth_views.LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have been logged out successfully.")
        return super().dispatch(request, *args, **kwargs)

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    # path('reg/', views.registration, name='registration'),
    path('port/', views.portfolio, name='portfolio'),
    path('register/', views.registration, name='register'),
    path('userhome/', views.userhome, name='userhome'),
    path('forgotpas/', views.forgotpass, name='forgotpassword'),
    path('resetpas/<uidb64>/<token>/',views.resetpass, name='resetpassword'),
    path('register/', views.registration, name='register'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('logout/', views.logout_view, name='logout'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('about/', views.about, name='about'),
    path('service/', views.service, name='service'),
    path('project/', views.project, name='project'),
    path('blog/', views.blog_grid, name='blog_grid'),
    path('dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('slogin/', views.seller_login, name='slogin'),
    path('shome/', views.shome, name='shome'),
    path('sregister/', views.sregister, name='sregister'),
    path('dhome/', views.dportfolio_view, name='dhome'),
    path('dregister/', views.dregister_view, name='dregister'),
    path('dlogin/', views.dlogin_view, name='dlogin'),
    path('addnewproduct/', views.add_product, name='addnewproduct'),
    path('add_design/', views.add_design, name='add_design'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
