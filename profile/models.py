from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=70, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    street = models.CharField(max_length=60)
    house_number = models.CharField(max_length=10)
    flat_number = models.CharField(max_length=10, null=True)
    zip_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=12)
    city = models.CharField(max_length=100, null=True)