from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Photo
from .serializers import PhotoSerializer

class PhotoUploadView(generics.CreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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
