import io
import logging
from abc import ABC, abstractmethod

from django.db import transaction
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image, UnidentifiedImageError

from .upload_context import PhotoUploadContext
from .services import TagService
from feed.services import PhotoFeedService
from .exceptions import PhotoProcessingError

logger = logging.getLogger(__name__)

class AbstractPhotoProcessor(ABC):
    @abstractmethod
    def process(self, context: PhotoUploadContext) -> PhotoUploadContext:
        pass


class SaveProcessor(AbstractPhotoProcessor):
    def process(self, context: PhotoUploadContext) -> PhotoUploadContext:
        context.photo = context.serializer.save(user=context.user)
        return context


class TagAssignProcessor(AbstractPhotoProcessor):
    def process(self, context):
        if context.tags and context.photo:
            TagService.assign_tags_to_photo(context.tags, context.photo)
        return context


class CacheInvalidationProcessor(AbstractPhotoProcessor):
    def process(self, context):
        PhotoFeedService.invalidate_feed_cache()
        return context


class PhotoUploadPipeline:
    def __init__(self):
        # Register the sequence of operations here.
        self.processors : list[AbstractPhotoProcessor] = [
            SaveProcessor(),
            ThumbnailGeneratorProcessor(),
            TagAssignProcessor(),
            CacheInvalidationProcessor()
        ]

    @transaction.atomic
    def execute(self, context: PhotoUploadContext) -> PhotoUploadContext:
        for processor in self.processors:
            context = processor.process(context)
        return context


class ThumbnailGeneratorProcessor(AbstractPhotoProcessor):
    THUMBNAIL_SIZE = (300, 300)

    def process(self, context):
        if not context.photo or not context.photo.image:
            return context

        try:
            context.photo.image.seek(0)
            image_bytes = context.photo.image.read()
            image_stream = io.BytesIO(image_bytes)

            with Image.open(image_stream) as img:
                # convert RGBA to RBG for JPEG saving
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

                img.thumbnail(self.THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
                thumbnail = io.BytesIO()
                img.save(thumbnail, format='JPEG', quality=85)
                thumbnail.seek(0)

        except (UnidentifiedImageError, OSError, IOError) as exc:
            logger.exception(f"Thumbnail generation failed")
            raise PhotoProcessingError("The uploaded file could not be processed as a valid image.")

        thumbnail_filename = f"thumb_{context.photo.image.name.split('/')[-1]}"

        thumb_file = InMemoryUploadedFile(
            file=thumbnail,
            field_name=None,
            name=thumbnail_filename,
            content_type='image/jpeg',
            size=thumbnail.tell(),
            charset=None
        )

        context.photo.thumbnail.save(thumbnail_filename, thumb_file, save=True)
        return context