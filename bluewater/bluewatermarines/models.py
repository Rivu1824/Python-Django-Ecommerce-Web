from django.contrib.auth.models import *
from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from .utils import *
from decimal import Decimal


class UserManager(BaseUserManager):

    def create_user(self, email, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Username must be set")

        if not email:
            raise ValueError("Email must be set")

        email = self.normalize_email(email)
        user = self.model(username=username,email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

        

    def create_superuser(self, email, username, password=None, **extra_fields):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            *extra_fields
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    username = models.CharField(max_length=30, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        ordering = ['-date_joined']
        verbose_name_plural = '01. User'



class Categorie(models.Model):
    image = models.ImageField(upload_to="Media/Categorie/Img", null=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '02. Categorie'

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Categorie.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

@receiver(pre_save, sender=Categorie)
def pre_save_categorie_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_categorie_receiver, Categorie)



class SubCategorie(models.Model):
    image = models.ImageField(upload_to="Media/SubCategorie/Img", null=False)
    title = models.CharField(max_length=255)
    parent_categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    description = models.TextField()
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = '03.SubCategories'

def create_subcategorie_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = SubCategorie.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_subcategorie_slug(instance, new_slug=new_slug)
    return slug

@receiver(pre_save, sender=SubCategorie)
def pre_save_subcategorie_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_subcategorie_slug(instance)

pre_save.connect(pre_save_subcategorie_receiver, SubCategorie)



class ThirdCategorie(models.Model):
    image = models.ImageField(upload_to="Media/ThirdCategorie/Img", null=False)
    title = models.CharField(max_length=255)
    parent_subcategorie = models.ForeignKey(SubCategorie, on_delete=models.CASCADE)
    description = models.TextField()
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '04. ThirdCategories'

def create_third_categorie_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = ThirdCategorie.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_third_categorie_slug(instance, new_slug=new_slug)
    return slug

@receiver(pre_save, sender=ThirdCategorie)
def pre_save_third_categorie_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_third_categorie_slug(instance)

pre_save.connect(pre_save_third_categorie_receiver, ThirdCategorie)





class Product(models.Model):
    LEVEL_CHOICES = (
          ('P', 'primary'),
          ('S', 'secondary'),
          ('D', 'danger')
    )

    STATUS_CHOICES = (
        ('PUBLISH', 'PUBLISH'),
        ('DRAFT', 'DRAFT'),
    )


    COLOR_CHOICES = (
          ('Red', 'Red'),
          ('Blue', 'Blue'),
          ('Green', 'Green'),
          ('Yellow', 'Yellow'),
          ('Orange', 'Orange'),
          ('Purple', 'Purple'),
          ('Pink', 'Pink'),
          ('Brown', 'Brown'),
          ('Gray', 'Gray'),
          ('White', 'White'),
          ('Black', 'Black'),
          ('Cyan', 'Cyan'),
          ('Maroon', 'Maroon'),
          ('Olive', 'Olive'),
          ('Gold', 'Gold'),

    )
    SIZE_CHOICES = (
          ('Small', 'Small'),
          ('Medium', 'Medium'),
          ('Large', 'Large'),
          ('Extra-Small', 'Extra-Small'),
          ('Extra-Large', 'Extra-Large'),
          ('Double-Extra-Large', 'Double-Extra-Large'),
          ('Triple-Extra-Large', 'Triple-Extra-Large'),
          ('Petite', 'Petite'),
          ('Regular', 'Regular'),
          ('Tall', 'Tall'),
          ('Short', 'Short'),
          ('Plus-Size', 'Plus-Size'),
          ('Oversize', 'Oversize'),
          ('Full-Length', 'Full-Length'),
          ('Half-Length', 'Half-Length'),

    )

    image = models.ImageField(upload_to="Media/Product/Img/", null=True)
    image_2nd = models.ImageField(upload_to="Media/Product/Img/", null=True,blank=True,default=None)
    image_3rd = models.ImageField(upload_to="Media/Product/Img/", null=True,blank=True,default=None)
    image_4th = models.ImageField(upload_to="Media/Product/Img/", null=True,blank=True,default=None)
    image_5th = models.ImageField(upload_to="Media/Product/Img/", null=True,blank=True,default=None)
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    sub_title = models.CharField(max_length=200)
    description = models.TextField()
    categories = models.ForeignKey(ThirdCategorie, on_delete=models.CASCADE)
    Size = models.CharField(choices=SIZE_CHOICES, max_length=100,null=True,blank=True,default=None)
    color = models.CharField(choices=COLOR_CHOICES, max_length=100,null=True,blank=True,default=None)
    level = models.CharField(choices=LEVEL_CHOICES, max_length=20, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=100, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    def calculate_discounted_price(self):
        discount_amount = (self.discount_percentage / 100) * self.price
        discounted_price = self.price - discount_amount
        return max(discounted_price, 0)

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_discounted_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    class Meta:
             verbose_name_plural = '05. Product'

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

@receiver(pre_save, sender=Product)
def pre_save_product_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_product_receiver, Product)

class Product_point(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    point = models.CharField(max_length=200)

    def __str__(self):
        return self.point


class Product_Specification(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    Dimensions = models.CharField(max_length=100,null=True,blank=True,default=None)
    Guarantee = models.CharField(max_length=100,null=True,blank=True,default=None)
    Brand = models.CharField(max_length=100,null=True,blank=True,default=None)
    Item_model_number = models.CharField(max_length=100,null=True,blank=True,default=None)
    Item_Type  = models.CharField(max_length=100,null=True,blank=True,default=None)
    Item_Height  = models.CharField(max_length=100,null=True,blank=True,default=None)
    Item_Width  = models.CharField(max_length=100,null=True,blank=True,default=None)
    Item_Weight  = models.CharField(max_length=100,null=True,blank=True,default=None)

    def __str__(self):
        return self.Guarantee



class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code

    class Meta:
             verbose_name_plural = '06. Coupon'



class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.CharField(max_length=100)  
    size = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_final_price(self):
        final_price = Decimal(self.quantity) * self.item.total_price
        if self.coupon:
            final_price -= Decimal(self.coupon.amount)
        return final_price

    class Meta:
        verbose_name_plural = '07. OrderItem'



class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(OrderItem)
    transaction_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    mobile = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    Street_Address = models.CharField(max_length=50)
    Postcode_Zip = models.CharField(max_length=50)
    Country  = models.CharField(max_length=50)
    State = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    payment_status = models.CharField(choices=STATUS_CHOICES, max_length=100, default='Pending')
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.mobile
    
    class Meta:
        verbose_name_plural = '08. Order'

    @classmethod
    def process_checkout(cls, user, product, first_name, last_name, mobile, address, city):
        transaction = Order.objects.create(
            user=user,
            product=product,
            transaction_id=generate_unique_transaction_id(),
            amount=product.calculate_discounted_price(),
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
            address=address,
            city=city,
            payment_status='Pending',
        )

        return {'transaction': transaction}

    


class OrderItemSuccess(models.Model): 
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    color = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.title}"

    def get_final_price(self):
        return self.quantity * self.product.total_price  

    class Meta:
        verbose_name_plural = 'Order Items Success'



class Logo(models.Model):
    Logo_file = models.ImageField(upload_to='logo_files/')
    background_image = models.ImageField(upload_to='Banner/background')
    nav_image = models.ImageField(upload_to='Banner/nav')
    email = models.EmailField(max_length=254, unique=True)
    address = models.CharField(max_length=200)
    mobile_number = models.BigIntegerField(unique=True)
    facebook_link = models.URLField(max_length=200, blank=True, null=True)
    linkedin_link = models.URLField(max_length=200, blank=True, null=True)
    instagram_link = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.Logo_file)
    class Meta:
             verbose_name_plural = '09. Logo'


class Banner(models.Model):
    title = models.CharField(max_length=255)
    sub_title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='home/banner_images/')

    def __str__(self):
        return self.title
    
    class Meta:
             verbose_name_plural = '10. Banner'


class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
            verbose_name_plural = '11. Contact'