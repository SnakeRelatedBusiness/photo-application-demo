from rest_framework.test import APITestCase
from rest_framework import status

from photos.models import Photo
from ..test.test_data import TestDataMixin


class PhotoUploadTests(APITestCase, TestDataMixin):
    def setUp(self):
        self.user = self.create_user()
        self.other_user = self.create_user(username="other_user")

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

        new_photo = Photo.objects.latest('uploaded_at')
        self.assertTrue(bool(new_photo.thumbnail))
        self.assertEqual(new_photo.tags.count(), 2)


    def test_upload_when_unauthenticated_forbidden(self):
        response = self.client.post(self.get_url(), {})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Photo.objects.count(), 1)


class PhotoDeleteTests(APITestCase, TestDataMixin):
    def setUp(self):
        self.user = self.create_user()
        self.other_user = self.create_user(username="other_user")

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


class ProfileAPITests(APITestCase, TestDataMixin):
    def setUp(self):
        self.user = self.create_user()
        self.other_user = self.create_user(username="other_user")

        self.photo1 = Photo.objects.create(
            user=self.user,
            caption="User Photo 1",
            image=self.get_mock_image()
        )

        self.photo2 = Photo.objects.create(
            user=self.other_user,
            caption="Other Photo",
            image=self.get_mock_image()
        )

    @staticmethod
    def get_url() -> str:
        return '/api/profile/'

    def test_profile_view_returns_owned_photos(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.get_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.photo1.id)

    def test_profile_view_serializes_fields(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.get_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        photo_data = response.data[0]

        self.assertIn('thumbnail_url', photo_data)
        self.assertIn('total_likes', photo_data)
        self.assertEqual(photo_data['total_likes'], 0)

    def test_unauthenticated_user_forbidden(self):
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)