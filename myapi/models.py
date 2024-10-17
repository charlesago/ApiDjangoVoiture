# myapi/models.py
import hashlib
import secrets

from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
class CustomUser(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    enabled = models.IntegerField(default=1)

    def __str__(self):
        return self.username
class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='marques')

    def __str__(self):
        return f"{self.name} (Groupe: {self.group.name})"


class Model(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='models')
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.brand.name} {self.name} ({self.year})"

class GlobalApiKey(models.Model):
    key = models.CharField(max_length=256, unique=True, editable=False)
    name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @staticmethod
    def generate_raw_key():

        return secrets.token_urlsafe(50)

    @staticmethod
    def hash_key(raw_key):

        return hashlib.sha256(raw_key.encode('utf-8')).hexdigest()

    def check_key(self, raw_key):
        return self.key == self.hash_key(raw_key)

class Client(models.Model):
    client_id = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255)
    api_key = models.CharField(max_length=256, unique=True)
    count = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    uuid = models.CharField(max_length=36, blank=True, null=True, unique=True)
    def __str__(self):
        return f"{self.email} ({self.client_id})"