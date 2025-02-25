from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required


# class CustomLogoutView(auth_views.LogoutView):
#     def dispatch(self, request, *args, **kwargs):
#         messages.success(request, "You have been logged out successfully.")
#         return super().dispatch(request, *args, **kwargs)

urlpatterns = [
    path('dregister/', views.dregister, name='dregister'),  # Ensure this matches the function name
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
    # path('logout/', CustomLogoutView.as_view(), name='logout'),
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
    path('dregister/', views.dregister, name='dregister'),
    path('dlogin/', views.dlogin_view, name='dlogin'),
    path('addnewproduct/', views.add_product, name='addnewproduct'),
    path('add_design/', views.add_design, name='add_design'),
    path('designp/', views.designp, name='designp'),
    path('decorella', views.decorella, name='decorella'),
    path('uphome', views.uphome, name='uphome'), 
    path('cart/', views.cart_view, name='cart'),
    # path('search/', views.search_products, name='search_products'),
    # path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('realhome', views.realhome, name='realhome'),  # Home Page
    path('designers/', views.designers_view, name='designers'),  # Designers Page
    path('design/<int:design_id>/', views.design_detail, name='design_detail'),
    path('designs/edit/<int:id>/', views.edit_design, name='edit_design'),
    path('designs/remove/<int:id>/', views.remove_design, name='remove_design'),
    path('dcart/', views.designer_cart_view, name='dcart'),
    path('dcart/update/<int:item_id>/', views.update_designer_cart, name='update_dcart'),
    path('dcart/remove/<int:item_id>/', views.remove_from_designer_cart, name='remove_from_dcart'),
    path('browse/', views.browse, name='browse'),  # URL for the browse page
    path('designer/<int:designer_id>/', views.designer_detail, name='designer_detail'),
    path('designers/remove/<int:designer_id>/', views.remove_designer, name='remove_designer'),
    path('designers/contact/<int:designer_id>/', views.contact_designer, name='contact_designer'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('kitchen-designs/', views.kitchen_designs, name='kitchen_designs'),
    path('living-room-designs/', views.living_room_designs, name='living_room_designs'),
    path('bedroom-designs/', views.bedroom_designs, name='bedroom_designs'),
    path('bathroom-designs/', views.bathroom_designs, name='bathroom_designs'),
    path('products/category1/', views.product_1, name='Lighting'),
    path('products/category2/', views.product_2, name='Decor_Items'),
    path('products/category3/', views.product_3, name='Curtains'),
    path('dining-room-designs/', views.dining_room_designs, name='dining_room_designs'),
    path('business-office-designs/', views.business_office_designs, name='business_office_designs'),
    path('hallway-entry-designs/', views.hallway_entry_designs, name='hallway_entry_designs'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('favorites/remove/<int:design_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('toggle-favorite/<int:design_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('search/', views.search_designs, name='search_designs'),
    path('get-favorites-count/', views.get_favorites_count, name='get_favorites_count'),
    path('products/', views.products_list, name='products'),
    path('products/category/<str:category>/', views.products_by_category, name='products_by_category'),
    path('products/filter/', views.filter_products, name='filter_products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('create-order/', views.create_order, name='create_order'),
    path('payment-success/<str:order_id>/', views.payment_success, name='payment_success'),
    path('payment-success-page/', views.payment_success_page, name='payment_success_page'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('get-cart-count/', views.get_cart_count, name='get_cart_count'),
    path('3d_modeling/', views.modeling_view, name='3d_modeling'),
    path('generate-3d-model/', views.generate_3d_model, name='generate_3d_model'),
    path('budget-planner/', views.budget_planner, name='budget_planner'),
    path('create-budget-plan/', views.create_budget_plan, name='create_budget_plan'),
    path('lighting-bulbs/', views.lighting_bulbs, name='lighting_bulbs'),
    path('decoration-items/', views.decoration_items, name='decoration_items'),  # Correct URL pattern
    path('carpets-and-rugs/', views.carpets_and_rugs, name='carpets_and_rugs'),  # New URL for carpets and rugs
    path('wallpapers/', views.wallpapers, name='wallpapers'),  # New URL for wallpapers
    path('indoor-plants/', views.indoor_plants, name='indoor_plants'),  # New URL for indoor plants
    path('storage-solutions/', views.storage_solutions, name='storage_solutions'),  # New URL for storage solutions
    path('furniture/', views.furniture, name='furniture'),
    path('curtains-and-drapes/', views.curtains_and_drapes, name='curtains_and_drapes'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('worker/register/', views.worker_register, name='worker_register'),
    path('worker/login/', views.worker_login, name='worker_login'),
    path('worker/dashboard/', views.worker_dashboard, name='worker_dashboard'),
    path('meet-workers/', views.meet_workers, name='meet_workers'),
    path('worker/profile/<int:worker_id>/', views.worker_profile, name='worker_profile'),
    path('filter-workers/', views.filter_workers, name='filter_workers'),
    path('view-designs/', views.view_designs, name='view_designs'),
    path('filter-designs/', views.filter_designs, name='filter_designs'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('admin/users/', views.admin_users, name='admin_users'),
    path('admin/filter-users/', views.filter_users, name='filter_users'),
    path('designers/', views.view_designers, name='view_designers'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
