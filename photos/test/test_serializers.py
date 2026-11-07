from django.test import TestCase

from photos.serializers import PhotoSerializer
from ..test.test_data import TestDataMixin

class PhotoSerializerTests(TestCase, TestDataMixin):
    def test_missing_image_invalid(self):
        payload = {
            "caption" : "Image is missing"
        }

        serializer = PhotoSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn('image', serializer.errors)

    def test_valid_payload_accepted(self):
        payload = {
            "caption": "valid image request",
            "image": self.get_mock_image()
        }

        serializer = PhotoSerializer(data=payload)
        self.assertTrue(serializer.is_valid())
