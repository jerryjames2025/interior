from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


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
    password = models.CharField(max_length=255)  # Changed from max_digits to max_length
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    category = models.CharField(
        max_length=50,
        choices=[
            ('Furniture', 'Furniture'),
            ('Lighting', 'Lighting'),
            ('Home Decor', 'Home Decor'),
            ('Kitchen & Dining', 'Kitchen & Dining'),
            ('Outdoor & Garden', 'Outdoor & Garden'),
            ('Storage Solutions', 'Storage Solutions'),
            ('Bathroom Accessories', 'Bathroom Accessories'),
            ('Other', 'Other')
        ]
    )
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
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)

    @property
    def name(self):
        return self.full_name

    def __str__(self):
        return self.full_name

# Then define Design model
class Design(models.Model):
    designer = models.ForeignKey(Designer, on_delete=models.CASCADE, related_name='designs')
    design_name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    area_size = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    room_type = models.CharField(
        max_length=50,
        choices=[
            ('Living Room', 'Living Room'),
            ('Bedroom', 'Bedroom'),
            ('Kitchen', 'Kitchen'),
            ('Bathroom', 'Bathroom'),
            ('Dining Room', 'Dining Room'),
            ('Office', 'Office'),
            ('Kids Room', 'Kids Room'),
            ('Master Bedroom', 'Master Bedroom'),
            ('Guest Room', 'Guest Room'),
            ('Study Room', 'Study Room'),
            ('Balcony', 'Balcony'),
            ('Outdoor Space', 'Outdoor Space')
        ]
    )
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
    features = models.JSONField(default=list)
    image = models.ImageField(upload_to='design_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    favorited_by = models.ManyToManyField(User, through='Favorite', related_name='favorite_designs_set')

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
