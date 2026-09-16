from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email" # khai báo hằng số, ko tạo ra field trong database"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
    

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer_profile",)
    phone = models.CharField(max_length=30, blank=True)
    billing_address = models.TextField(blank=True)
    shipping_address = models.TextField(blank=True)

    def __str__(self):
        return f"Profile of {self.user.email}"