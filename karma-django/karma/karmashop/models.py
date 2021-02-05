from django.db import models
from django.contrib.auth import models as dj_models

# Create your models here.

class Address(models.Model):
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    country = models.CharField(max_length=100)



class Profile(models.Model):
    user_id = models.ForeignKey(dj_models.User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=13)
    alternate_mobile_number = models.CharField(max_length=13,null=True, blank=True)
    address = models.ManyToManyField(Address,blank=True)



class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0, null=True,blank=True)
    discription = models.TextField()
    quantity = models.IntegerField(default=0, null=True,blank=True)
    category = models.CharField(max_length=255)
    img = models.ImageField(upload_to='product/')

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(dj_models.User,on_delete=models.CASCADE)
    transection_id = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False,null=True,blank=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        order_items = OrderItem.objects.filter(order=self.id)
        subtotal = sum([item.get_total for item in order_items])

        #order_items = self.orderitem_set.all()
        total_items = sum([item.quantity for item in order_items])

        gst = subtotal * 0.18
        total = subtotal + gst

        return {'subtotal' : subtotal,
                'gst' : gst,
                'total' : total,
                'total_items':total_items}


class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0, null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        return self.quantity * self.product.price



class ShippingInfo(models.Model):
    user = models.ForeignKey(dj_models.User,on_delete=models.SET_NULL,null=True,blank=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
    address = models.ForeignKey(Address,on_delete=models.SET_NULL,null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
