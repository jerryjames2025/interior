from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    bio = models.TextField(blank=True)
    is_designer = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='portfolio_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


    
from django.db import models
from django.db import models

class Seller(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    company = models.CharField(max_length=255)
    password = models.CharField(max_length=128)  # For storing hashed password
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Furniture', 'Furniture'),
        ('Lighting', 'Lighting & Bulbs'),
        ('Decor', 'Decoration Items'),
        ('Carpets', 'Carpets & Rugs'),
        ('Curtains', 'Curtains & Drapes'),
        ('Wallpaper', 'Wallpapers'),
        ('Plants', 'Indoor Plants'),
        ('Storage', 'Storage Solutions'),
    ]
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    style = models.CharField(
        max_length=50,
        choices=[
            ('Modern', 'Modern'),
            ('Traditional', 'Traditional'),
            ('Contemporary', 'Contemporary'),
            ('Minimalist', 'Minimalist'),
            ('Industrial', 'Industrial'),
            ('Rustic', 'Rustic')
        ],
        default='Modern'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    
    from django.db import models
from django.contrib.auth.models import User

# Define Designer model first
class Designer(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    profile_picture = models.ImageField(upload_to='designer_profiles/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    experience_years = models.PositiveIntegerField(default=0)
    specializations = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.username

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

# Then define Design model
class Design(models.Model):
    ROOM_TYPE_CHOICES = [
        ('living', 'Living Room'),
        ('bedroom', 'Bedroom'),
        ('kitchen', 'Kitchen'),
        ('bathroom', 'Bathroom'),
        ('office', 'Office'),
    ]
    
    STYLE_CHOICES = [
        ('modern', 'Modern'),
        ('traditional', 'Traditional'),
        ('minimalist', 'Minimalist'),
        ('contemporary', 'Contemporary'),
    ]

    designer = models.ForeignKey(Designer, on_delete=models.CASCADE)
    design_name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='designs/')
    category = models.CharField(max_length=100)
    room_type = models.CharField(max_length=100)
    style = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    area_size = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    favorited_by = models.ManyToManyField(User, related_name='favorite_designs', blank=True)

    def __str__(self):
        return self.design_name

    class Meta:
        ordering = ['-created_at']

# Model to represent an entire shopping cart for a user
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_cart_total(self):
        # Calculate total price of the cart using the items directly
        return sum(item.quantity * item.product.price for item in self.items.all())

    def __str__(self):
        return f"Cart for {self.user.username}"

# Model to represent a single item within a cart
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f'{self.product.product_name} - {self.quantity}'

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link feedback to a user
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Feedback from {self.user.username} - {self.subject}'

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    design = models.ForeignKey(Design, on_delete=models.CASCADE, related_name='favorites')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'design')

    def __str__(self):
        return f"{self.user.username} - {self.design.design_name}"

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    shipping_address = models.TextField(null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name} in Order {self.order.id}"

class BudgetPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    min_budget = models.DecimalField(max_digits=10, decimal_places=2)
    max_budget = models.DecimalField(max_digits=10, decimal_places=2)
    room_type = models.CharField(max_length=50)
    design_style = models.CharField(max_length=50, blank=True, null=True)
    area_size = models.DecimalField(max_digits=8, decimal_places=2)
    priority_features = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='active')
    
    class Meta:
        ordering = ['-created_at']

class BundleDeal(models.Model):
    name = models.CharField(max_length=100)
    products = models.ManyToManyField('Product')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    valid_until = models.DateTimeField()

class BudgetAllocation(models.Model):
    budget_plan = models.ForeignKey(BudgetPlan, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)  # e.g., Furniture, Decor, Lighting
    allocation_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    allocated_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        self.allocated_amount = (self.allocation_percentage / 100) * self.budget_plan.total_budget
        super().save(*args, **kwargs)

class Project(models.Model):
    name = models.CharField(max_length=200)
    designer = models.ForeignKey(Designer, on_delete=models.CASCADE)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    room_type = models.CharField(max_length=50)
    area_size = models.DecimalField(max_digits=8, decimal_places=2)
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project_images/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.project.name}"

# class Notification(models.Model):
#     worker = models.ForeignKey(Worker, on_delete=models.CASCADE, null=True, blank=True)
#     designer = models.ForeignKey(Designer, on_delete=models.CASCADE, null=True, blank=True)
#     message = models.TextField()
#     type = models.CharField(max_length=50)  # team_invitation, team_acceptance, team_decline
#     related_id = models.IntegerField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Notification for {self.worker or self.designer}"

# First, define the ConstructionCompany model
class ConstructionCompany(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    company_size = models.CharField(max_length=20, choices=[
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large')
    ])
    logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)

    def __str__(self):
        return self.company_name

class Company(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    established_year = models.IntegerField()
    description = models.TextField()
    logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Worker(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='workers')
    name = models.CharField(max_length=200)
    skill = models.CharField(max_length=100)
    experience_years = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.skill}"

class Consultation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
        ('completed', 'Completed')
    ]
    
    METHOD_CHOICES = [
        ('video', 'Video Call'),
        ('voice', 'Voice Call'),
        ('in_person', 'In Person')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    designer = models.ForeignKey(Designer, on_delete=models.CASCADE)
    design = models.ForeignKey(Design, on_delete=models.CASCADE)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    consultation_method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Consultation with {self.designer.full_name} - {self.status}"

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('consultation_update', 'Consultation Update'),
        ('new_message', 'New Message'),
        ('system', 'System Notification')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"
