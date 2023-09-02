from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

class Recipient(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)

class Courier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)

class Package(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()

class CustomerLocation(models.Model):
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

class Delivery(models.Model):
    delivery_date = models.DateField()
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    customer_location = models.ForeignKey(CustomerLocation, on_delete=models.CASCADE)
    pack = models.ForeignKey(Package, on_delete=models.CASCADE)

