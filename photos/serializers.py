from rest_framework import serializers
from .models import Photo
from django.db.models import Count

class PhotoSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='user.username')
    total_likes = serializers.IntegerField(source='likes.count', read_only=True)

    class Meta:
        model = Photo
        fields = ('id', 'user_id', 'author', 'image', 'caption', 'uploaded_at', 'total_likes')
        read_only_fields = ['user_id', 'author', 'uploaded_at']
