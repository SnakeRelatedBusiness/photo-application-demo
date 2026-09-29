from rest_framework import serializers


class FeedItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    author = serializers.CharField(source='user.username')
    image_url = serializers.ImageField(source='image')
    caption = serializers.CharField()
    total_likes = serializers.IntegerField()
    uploaded_at = serializers.DateTimeField()
