from django.db import models

from django.contrib.auth.models import User
from image_cropping import ImageRatioField



# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Category (models.Model):
    parent=models.ForeignKey('self',blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    name = models.CharField(max_length=30, unique=True)
    dept_name = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name


class Product(models.Model):
    BOOL_CHOICES = ((True, 'Published'), (False, 'Draft'))
    name = models.CharField(max_length=200, null=True,)
    category = models.CharField(max_length=200, default=None,)
    status = models.BooleanField(default=False,choices=BOOL_CHOICES)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.IntegerField( null=True, blank=True)
    strike_out_price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    #digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True,default="dummy/dummy_product.jpg", upload_to = 'products/')
    description = models.TextField(blank=True, null=True)
    dateadded = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.name
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

       

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    def __str__(self):
        return str(self.id)
 

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
       
        if orderitems is None:
            return 0
        total =sum([item.get_total for item in orderitems])
        return total

    


    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        if orderitems is None:
            return 0
        total =sum([item.quantity for item in orderitems])
        
        return total

  

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=False, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        if self.product is None:
            return 0
        
        total = self.product.price * self.quantity


        return total



class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class SiteName (models.Model):
    primry_name = models.CharField(max_length=200, null=True)
    
    

class SiteImage (models.Model):
    
    logoImage = models.ImageField(upload_to='logo/site_logo/',null=True, blank=True)



class FrontEndSettings(models.Model):
    navbarcolor = models.CharField(max_length=10, blank=True, null=True)


 

    


