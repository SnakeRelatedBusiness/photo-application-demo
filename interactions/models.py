from django.db import models
from django.conf import settings
from photos.models import Photo

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'photo')
        
    def __str__(self):
        return f"{self.user.username} likes {self.photo.id}"