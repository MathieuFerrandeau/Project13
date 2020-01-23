from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    """Category table"""
    name = models.CharField(max_length=100)

class Outlay(models.Model):
    """Outlay table"""
    name = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="outlay")
    amount = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    payment_method = models.CharField(null=True, blank=True, max_length=15)
    payment_date = models.DateField(null=True, blank=True)
    creation_date = models.DateField(null=True, blank=True)

class UserOutlay(models.Model):
    """UserOutlay table"""
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    outlay = models.ForeignKey(Outlay, on_delete=models.CASCADE)