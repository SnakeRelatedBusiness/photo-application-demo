from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Photo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='photos/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
            return f"Photo {self.id} by {self.user.username}"