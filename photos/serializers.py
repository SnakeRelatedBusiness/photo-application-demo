from rest_framework import serializers
from .models import Photo
from django.db.models import Count

class PhotoSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='user.username')
    total_likes = serializers.IntegerField(source='likes.count', read_only=True)
    is_liked_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ('id', 'user_id', 'author', 'image', 'caption', 'uploaded_at', 'total_likes', 'is_liked_by_user')
        read_only_fields = ['user_id', 'author', 'uploaded_at']

    def get_is_liked_by_user(self, obj):
        request = self.context.get('request')

        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False