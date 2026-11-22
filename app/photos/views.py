
from django.db.models import Count
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from .models import Photo
from .serializers import PhotoSerializer, ProfileGridSerializer
from .upload_context import PhotoUploadContext
from .processors import PhotoUploadPipeline
from .exceptions import PhotoProcessingError
from feed.services import PhotoFeedService

class PhotoUploadView(generics.CreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        context = PhotoUploadContext(
            user=self.request.user,
            tags=self.request.data.getlist('tags', []),
            serializer=serializer,
        )

        pipeline = PhotoUploadPipeline()

        try:
            pipeline.execute(context)
        except PhotoProcessingError as exc:
            if context.photo and context.photo.image:
                context.photo.image.delete(save=False)

            raise ValidationError({"image": str(e)})


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

    def perform_destroy(self, instance):
        PhotoFeedService.invalidate_feed_cache()
        return super().perform_destroy(instance)


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Photo.objects.filter(user=request.user)\
            .annotate(total_likes=Count('likes'))\
            .order_by('-uploaded_at')

        serializer = ProfileGridSerializer(qs, many=True)
        return Response(serializer.data)


class ProfileTemplateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return render(request, 'photo/profile.html')