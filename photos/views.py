from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Photo
from .serializers import PhotoSerializer
from .services import TagService
from feed.services import PhotoFeedService


class PhotoUploadView(generics.CreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        tags = self.request.data.getlist('tags', [])
        photo = serializer.save(user=self.request.user)
        TagService.assign_tags_to_photo(tags, photo)

        PhotoFeedService.invalidate_feed_cache()


class PhotoDetailView(generics.RetrieveAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]


class PhotoTemplateView(APIView):
    def get(self, request, photo_id):
        return render(request, 'photo/photo.html', {'current_user_id': request.user.id if request.user.is_authenticated else None})


class PhotoDeleteView(generics.DestroyAPIView):
    serializer_class = PhotoSerializer

    def get_queryset(self):
        return Photo.objects.filter(user=self.request.user)
