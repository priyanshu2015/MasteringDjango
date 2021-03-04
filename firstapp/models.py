from django.db import models

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone
# Create your models here.
from multiselectfield import MultiSelectField


from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager

from django.contrib.auth.models import PermissionsMixin

from django.db.models import Q
from datetime import timedelta


# class UserType(models.Model):
#     CUSTOMER = 1
#     SELLER = 2
#     TYPE_CHOICES = (
#         (SELLER, 'Seller'),
#         (CUSTOMER, 'Customer')
#     )

#     id = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, primary_key=True)

#     def __str__(self):
#         return self.get_id_display()

class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """
    def to_python(self, value):
        """
        Convert email to lowercase.
        """
        value = super(LowercaseEmailField, self).to_python(value)
        # Value can be None so check that it's a string before lowercasing.
        if isinstance(value, str):
            return value.lower()
        return value

class CustomUser(AbstractBaseUser, PermissionsMixin):
    # username = None
    email = LowercaseEmailField(_('email address'), unique=True)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # if you require phone number field in your project
    phone_regex = RegexValidator( regex = r'^\d{10}$',message = "phone number should exactly be in 10 digits")
    phone = models.CharField(max_length=255, validators=[phone_regex], blank = True, null=True)  # you can set it unique = True

    # is_customer = models.BooleanField(default=True)
    # is_seller = models.BooleanField(default = False)

    # type = (
    #     (1, 'Seller'),
    #     (2, 'Customer')
    # )
    # user_type = models.IntegerField(choices = type, default=1)

    #usertype = models.ManyToManyField(UserType)

    class Types(models.TextChoices):
        SELLER = "Seller", "SELLER"
        CUSTOMER = "Customer", "CUSTOMER"
    
    # Types = (
    #     (1, 'SELLER'),
    #     (2, 'CUSTOMER')
    # )
    # type = models.IntegerField(choices=Types, default=2)

    default_type = Types.CUSTOMER

    #type = models.CharField(_('Type'), max_length=255, choices=Types.choices, default=default_type)
    type = MultiSelectField(choices=Types.choices, default=[], null=True, blank=True)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    #place here
        # if not the code below then taking default value in User model not in proxy models
    def save(self, *args, **kwargs):
        if not self.id:
            #self.type = self.default_type
            self.type.append(self.default_type)
        return super().save(*args, **kwargs)

class CustomerAdditional(models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    address = models.CharField(max_length=1000)


class SellerAdditional(models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    gst = models.CharField(max_length=10)
    warehouse_location = models.CharField(max_length=1000)

# Model Managers for proxy models
class SellerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        #return super().get_queryset(*args, **kwargs).filter(type = CustomUser.Types.SELLER)
        return super().get_queryset(*args, **kwargs).filter(Q(type__contains = CustomUser.Types.SELLER))

class CustomerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        #return super().get_queryset(*args, **kwargs).filter(type = CustomUser.Types.CUSTOMER)
        return super().get_queryset(*args, **kwargs).filter(Q(type__contains = CustomUser.Types.CUSTOMER))


# Proxy Models. They do not create a seperate table
class Seller(CustomUser):
    default_type = CustomUser.Types.SELLER
    objects = SellerManager()
    class Meta:
        proxy = True
    
    def sell(self):
        print("I can sell")

    @property
    def showAdditional(self):
        return self.selleradditional

class Customer(CustomUser):
    default_type = CustomUser.Types.CUSTOMER
    objects = CustomerManager()
    class Meta:
        proxy = True 

    def buy(self):
        print("I can buy")

    @property
    def showAdditional(self):
        return self.customeradditional


class Contact(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=5)
    phone_regex = RegexValidator( regex = r'^\d{10}$',message = "phone number should exactly be in 10 digits")
    phone = models.CharField(max_length=255, validators=[phone_regex])
    query = models.TextField()





class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=15)
    image = models.ImageField(upload_to = "firstapp/productimages", default = None, null = True, blank = True)
    price = models.FloatField()
    brand = models.CharField(max_length=1000)
    date_added = models.DateTimeField(default=timezone.now)

    #class Meta:
        #ordering = ['-price']      # default ordering whenever you query to database    retrieval in order as stored in DB ---> ordering ---> returned as a queryset where called

    @classmethod
    def updateprice(cls,product_id, price):
        product = cls.objects.filter(product_id = product_id)
        product = product.first()
        product.price = price
        product.save()
        return product

    @classmethod
    def create(cls, product_name, price):
        product = Product(product_name = product_name, price = price)
        product.save()
        return product
    

    # @staticmethod
    # def a_static_method():
    #     """A static method has no information about instances or classes
    #     unless explicitly given. It just lives in the class (and thus its 
    #     instances') namespace.
    #     """
    #     return some_function_h()

    def __str__(self):
        return self.product_name



class CartManager(models.Manager):
    def create_cart(self, user):
        cart = self.create(user = user)
        # you can perform more operations 
        return cart

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)

    objects = CartManager()

class ProductInCart(models.Model):
    class Meta:
        unique_together = (('cart', 'product'),)
    product_in_cart_id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField()


class Order(models.Model):
    status_choices = (
        (1, 'Not Packed'),
        (2, 'Ready For Shipment'),
        (3, 'Shipped'),
        (4, 'Delivered')
    )
    payment_status_choices = (
        (1, 'SUCCESS'),
        (2, 'FAILURE' ),
        (3, 'PENDING'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.IntegerField(choices = status_choices, default=1)

    total_amount = models.FloatField()
    payment_status = models.IntegerField(choices = payment_status_choices, default=3)
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True, default=None) 
    datetime_of_payment = models.DateTimeField(default=timezone.now)
    # related to razorpay
    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)
    

    def save(self, *args, **kwargs):
        if self.order_id is None and self.datetime_of_payment and self.id:
            self.order_id = self.datetime_of_payment.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.user.email + " " + str(self.id)
    

class ProductInOrder(models.Model):
    class Meta:
        unique_together = (('order', 'product'),)
    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()




class Deal(models.Model):
    user = models.ManyToManyField(CustomUser)
    deal_name = models.CharField(max_length=255)



class OtpModel(models.Model):
    otp_regex = RegexValidator( regex = r'^\d{6}$',message = "otp should be in six digits")
    otp = models.CharField(max_length=6, validators=[otp_regex])
    phone_regex = RegexValidator( regex = r'^\d{10}$',message = "phone number should exactly be in 10 digits")
    phone = models.CharField(max_length=255, validators=[phone_regex])
    expiry = models.DateTimeField(default = (timezone.now() + timedelta(minutes = 5)))
    is_verified = models.BooleanField(default=False)
    
    # expiry_after_verified



# class Category(models.Model):
#     category_name = models.CharField(max_length=1000)

# class Subcategory(models.Model):
#     subcategory_name = models.CharField(max_length=1000)
#     category = models.ForeignKey(Category, on_delete = models.CASCADE)



class PremiumProduct(models.Model):
    product_name = models.CharField(max_length=15)
    image = models.ImageField(upload_to = "firstapp/premiumproductimages", default = None, null = True, blank = True)
    price = models.FloatField()
    brand = models.CharField(max_length=1000)
    date_added = models.DateTimeField(default=timezone.now)

    # # custom permissions dependent to a specific model
    class Meta:
        permissions = (
            ('can_avail_premium_delivery', 'can avail for premium delivery on premium products'),
            ('can_add_premium_discount', 'can avail more premium discount on premium products')
       )



class CustomPermissions(models.Model):

    class Meta:

        managed = False  # No database table creation or deletion  \
                         # operations will be performed for this model.

        default_permissions = () # disable "add", "change", "delete"
                                 # and "view" default permissions

        # All the custom permissions not related to models on Manufacturer
        permissions = (
            ('accept_order', 'can accept order'),
            ('reject_order', 'can reject order'),
            ('view_order', 'can view order'),
            ('change_order', 'can change order'),
            ('view_return', 'can view return'),
            ('accept_return', 'can accept return'),
            ('reject_return', 'can reject return'),
            ('change_return', 'can change return'),
            ('view_dashboard', 'can view dashboard'),
        )

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


















