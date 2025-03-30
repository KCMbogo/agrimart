from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User

def user_directory_path(instance, filename):
    # return f'user_{instance.user.id}/{filename}'
    return "user_{0}/{1}".format(instance.user.id, filename)

STATUS_CHOICES = (
    ("processing", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)

STATUS = (
    ("draf", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
)

RATING = (
    (1, "⭐✩✩✩✩"),
    (2, "⭐⭐✩✩✩"),
    (3, "⭐⭐⭐✩✩"),
    (4, "⭐⭐⭐⭐✩"),
    (5, "⭐⭐⭐⭐⭐"),
)

class Category(models.Model):
    cid = ShortUUIDField(primary_key=True, editable=False, length=10, max_length=30, prefix="cat_", alphabet="0123456789abcdefghijklmn")
    title = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to="category")
    
    class Meta:
        verbose_name_plural = "Categories"
        
    def category_image(self):
        return mark_safe(f'<img src="{self.image.url}" width=50 height=50 />')
        
    def __str__(self):
        return self.title
    

class Vendor(models.Model):
    vid = ShortUUIDField(primary_key=True, editable=False, length=10, max_length=30, prefix="ven_", alphabet="0123456789abcdefghijklmn")
    title = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to=user_directory_path)
    description = models.TextField(blank=True, null=True)
    
    address = models.CharField(max_length=100, default="123 Main Street")
    contact = models.CharField(max_length=15, default="1+255 34567890")   
    chat_resp_time = models.CharField(max_length=100, default=100)
    shipping_on_time = models.CharField(max_length=100, default=100)
    authentic_rating = models.CharField(max_length=100, default=100)
    days_return = models.CharField(max_length=100, default=100)
    warranty_period = models.CharField(max_length=100, default=100)
     
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name_plural = "Vendors"
        
    def vendor_image(self):
        return mark_safe(f'<img src="{self.image.url}" width=50 height=50 />')
        
    def __str__(self):
        return self.title
    
    
class Tags(models.Model):
    pass
    
class Product(models.Model):
    pid = ShortUUIDField(primary_key=True, editable=False, length=10, max_length=30, prefix="pro_", alphabet="0123456789abcdefghijklmn")
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=user_directory_path)
    description = models.TextField(blank=True, null=True)
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    specifications = models.TextField(blank=True, null=True)
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    
    tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, blank=True, null=True)
    
    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")
    
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=True)
    digital = models.BooleanField(default=True)
    
    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix="sku_", alphabet="1234567890")
    
    date = models.DateField(auto_now_add=True)
    updated = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Products"
        
    def product_image(self):
        return mark_safe(f'<img src="{self.image.url}" width=50 height=50 />')
        
    def __str__(self):
        return self.title
    
    def get_percentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price
    

class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    images = models.ImageField(upload_to="product-images", default="product.jpg")
    date = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Product Images"
        
    
class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=999999999999999999, decimal_places=2, default="1.99")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICES, max_length=10, default="processing")
    
    class Meta:
        verbose_name_plural = "Cart Order"
        
        
class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=9999999999999999, decimal_places=2, default="1.99")
    total = models.DecimalField(max_digits=9999999999999999, decimal_places=2, default="1.99")
    
    class Meta:
        verbose_name_plural = "Cart Order Items"
        
    def order_img(self):
        return mark_safe(f'<img src="/media/{self.image}" width="50" />')
    
    
class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Product Reviews"
        
    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating
    
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Wishlists"
        
    def __str__(self):
        return self.product.title
    
 
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)

    


