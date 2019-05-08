from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    created_date = models.DateTimeField()

class Product(models.Model):
    name = models.CharField(max_length=100)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    description = models.CharField(max_length=1000)