from django.db import models
from django.contrib.auth.models import AbstractUser

class AppUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    
    def __str__(self):
        return self.username
