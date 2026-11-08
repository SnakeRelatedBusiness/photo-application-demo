from rest_framework.test import APITestCase
from rest_framework import status

from photos.models import Photo
from accounts.models import AppUser
from ..test.test_data import TestDataMixin


class PhotoUploadTests(APITestCase, TestDataMixin):
    def setUp(self):
        self.user = AppUser.objects.create(username="user", password="password")
        self.other_user = AppUser.objects.create(username="other_user", password="password")

        self.photo = Photo.objects.create(user=self.user, caption="Photo")
        self.mock_image = self.get_mock_image()

    @staticmethod
    def get_url() -> str:
        return '/api/photos/upload/'

    def test_upload_successful(self):
        self.client.force_authenticate(user=self.user)

        payload = {
            "caption": "Test",
            "image": self.mock_image,
            "tags": ["tag1", "tag2"]
        }
        response = self.client.post(self.get_url(), payload, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Photo.objects.count(), 2)


    def test_upload_when_unauthenticated_forbidden(self):
        response = self.client.post(self.get_url(), {})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Photo.objects.count(), 1)


class PhotoDeleteTests(APITestCase, TestDataMixin):
    def setUp(self):
        self.user = AppUser.objects.create(username="user", password="password")
        self.other_user = AppUser.objects.create(username="other_user", password="password")

        self.photo = Photo.objects.create(user=self.user, caption="Photo")
        self.mock_image = self.get_mock_image()

    @staticmethod
    def get_url(photo_id) -> str:
        return f'/api/photos/{photo_id}/delete/'

    def test_delete_photo_owner_success(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(self.get_url(self.photo.pk))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Photo.objects.count(), 0)

    def test_delete_photo_not_owner_forbidden(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(self.get_url(self.photo.pk))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Photo.objects.count(), 1)
