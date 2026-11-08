from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import PhotoFeedService
from .serializers import FeedItemSerializer

class GlobalFeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tag_slug = request.query_params.get('tag')
        feed_data = PhotoFeedService.get_feed(tag_slug)

        serializer = FeedItemSerializer(feed_data, many=True, context={'request': request})
        return Response(serializer.data)

class FeedTemplateView(APIView):
    def get(self, request):
        return render(request, 'feed/index.html')