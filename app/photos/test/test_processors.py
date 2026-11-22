from unittest.mock import patch
from django.test import TestCase
from PIL import Image

from photos.processors import ThumbnailGeneratorProcessor, SaveProcessor
from photos.models import Photo
from photos.upload_context import PhotoUploadContext
from ..test.test_data import TestDataMixin
from photos.exceptions import PhotoProcessingError

class ThumbnailGeneratorProcessorTests(TestCase, TestDataMixin):
    def test_thumbnail_generates_successfully(self):
        mock_image = self.get_mock_image()
        mock_image.name = "test_upload.jpg"

        user = self.create_user()
        photo = Photo(image=mock_image, user=user)

        context = PhotoUploadContext(
            user=user,
            tags=[],
            serializer=None,
            photo=photo
        )

        processor = ThumbnailGeneratorProcessor()
        post_process_context = processor.process(context)

        self.assertIsNotNone(post_process_context.photo.thumbnail)
        self.assertIn("thumb_test_upload", post_process_context.photo.thumbnail.name)

    def test_missing_image_skips_processor(self):
        photo = Photo()
        context = PhotoUploadContext(
            user=None,
            tags=[],
            serializer=None,
            photo=photo
        )

        processor = ThumbnailGeneratorProcessor()
        post_process_context = processor.process(context)
        self.assertFalse(post_process_context.photo.thumbnail)

    def test_exception_raises_photo_processing_error(self):
        with patch.object(Image, "open") as mock_save:
            with self.assertRaises(PhotoProcessingError):
                mock_save.side_effect = IOError

                mock_image = self.get_mock_image()
                mock_image.name = "test_upload.jpg"

                user = self.create_user()
                photo = Photo(image=mock_image, user=user)

                context = PhotoUploadContext(
                    user=user,
                    tags=[],
                    serializer=None,
                    photo=photo
                )

                processor = ThumbnailGeneratorProcessor()
                processor.process(context)
