from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .services import get_global_feed
from .serializers import FeedItemSerializer

class GlobalFeedView(APIView):
    def get(self, request):
        feed_data = get_global_feed()
        serializer = FeedItemSerializer(feed_data, many=True, context={'request': request})
        return Response(serializer.data)

class FeedTemplateView(APIView):
    def get(self, request):
        return render(request, 'feed/index.html')