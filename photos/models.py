from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Photo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photos')
    caption = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='photos/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    tags = models.ManyToManyField(Tag, blank=True, related_name='photos')

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
            return f"Photo {self.id} by {self.user.username}"