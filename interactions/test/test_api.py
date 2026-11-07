from rest_framework.test import APITestCase
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile

from photos.models import Photo
from accounts.models import AppUser
from interactions.models import Like

class TestToggleLIke(APITestCase):
    def setUp(self):
        self.user = AppUser.objects.create(username="user", password="password")
        self.other_user = AppUser.objects.create(username="other_user", password="password")

        self.photo = Photo.objects.create(user=self.user, caption="Photo")

    @staticmethod
    def get_url(photo_id : int) -> str:
        return f'/api/photos/{photo_id}/like/'

    def test_toggle_like_adds_like(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.post(self.get_url(self.photo.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.photo.likes.count(), 1)
        self.assertEqual(response.data['status'], 'liked')

    def test_toggle_like_removes_like(self):
        Like.objects.create(photo=self.photo, user=self.other_user)
        self.assertEqual(self.photo.likes.count(), 1)

        self.client.force_authenticate(user=self.other_user)

        response = self.client.post(self.get_url(self.photo.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.photo.likes.count(), 0)
        self.assertEqual(response.data['status'], 'unliked')

    def test_toggle_like_unauthenticated_bad_request(self):
        response = self.client.post(self.get_url(self.photo.pk))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.photo.likes.count(), 0)