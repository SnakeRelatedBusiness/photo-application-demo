from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import render

class LoginAPIView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({"status": "success", "message": "Logged in successfully"})

        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response({
                "is_authenticated": True,
                "id": request.user.id,
                "username": request.user.username
            })
        return Response({"is_authenticated": False})