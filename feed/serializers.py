from rest_framework import serializers


class FeedItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    author = serializers.CharField(source='user.username')
    image_url = serializers.ImageField(source='image')
    caption = serializers.CharField()
    total_likes = serializers.IntegerField()
    uploaded_at = serializers.DateTimeField()

    is_liked_by_user = serializers.SerializerMethodField()

    def get_is_liked_by_user(self, obj):
        request = self.context.get('request')

        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False
