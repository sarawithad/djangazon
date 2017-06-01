import datetime

from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone
from sorl.thumbnail import ImageField

class ProductType(models.Model):                      
    """
    purpose: Instantiates a product type
    author: Aaron Barfoot
    args: Extends the models.Model Django class
    returns: (None): N/A
    """   
    product_type_name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.product_type_name

    def get_absolute_url(self):
        return "/product_type_products/{}".format(self.id)

class Product(models.Model):
    """
    purpose: Instantiates a product
    author: boilerplate code
    args: Extends the models.Model Django class
    returns: (None): N/A
    """   
    seller = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
    )
    product_type = models.ForeignKey(ProductType)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    quantity = models.IntegerField()
    quantity_sold = models.IntegerField(default=0)
    product_photo = models.ImageField(blank=True, null=True) 
    city = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/single_product/{}".format(self.id)


# this is unnecessary and we don't need it, we should just look to the profile class that already has a one to one connection with the django user
class Customer(models.Model):
    """
    purpose: Instantiates a customer
    author: Dara Thomas
    args: Extends the models.Model Django class
    returns: (None): N/A
    """   
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField()
    # first_name = models.CharField(max_length=30)
    # last_name = models.CharField(max_length=30)
    # email_address = models.EmailField(max_length=30)




class PaymentType(models.Model):
    """
    purpose: Instantiates a payment type
    author: Dara Thomas
    args: Extends the models.Model Django class
    returns: (None): N/A
    """   
    payment_type_name = models.CharField(max_length=15)
    account_number = models.IntegerField()
    customer = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
    )

    class Meta:
        ordering = ('payment_type_name',)

    def __str__(self):
        return self.payment_type_name

class Order(models.Model):
    """
    purpose: Instantiates an order
    author: Dara Thomas
    args: Extends the models.Model Django class
    returns: (None): N/A
    """
    order_date = models.DateTimeField('Order Date', null=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.PROTECT, null=True)
    products = models.ManyToManyField(Product, through="ProductOrder")
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ('order_date',)

class ProductOrder(models.Model):
    """
    purpose: Instantiates an instance of a product on an order
    author: Dara Thomas
    args: Extends the models.Model Django class
    returns: (None): N/A
    """   
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


    class Meta:
        ordering = ('product',)

    def __str__(self):
        return self.product.title



class ProductOpinion(models.Model):
    """
    purpose: Store product likes and dislikes
    author: Aaron Barfoot
    args: 
    returns: (None): N/A
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    opinion = models.IntegerField(default=0)






