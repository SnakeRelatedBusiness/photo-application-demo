from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from photos.models import Photo
from .models import Like

class ToggleLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, photo_id):
        photo = get_object_or_404(Photo, id=photo_id)
        like, created = Like.objects.get_or_create(user=request.user, photo=photo)

        if not created:
            like.delete()
            return Response({"status": "unliked"})

        return Response({"status": "liked"})
