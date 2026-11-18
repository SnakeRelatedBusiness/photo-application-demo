from abc import ABC, abstractmethod

from django.db import transaction

from .upload_context import PhotoUploadContext
from .services import TagService
from feed.services import PhotoFeedService


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
            TagAssignProcessor(),
            CacheInvalidationProcessor()
        ]

    @transaction.atomic
    def execute(self, context: PhotoUploadContext) -> PhotoUploadContext:
        for processor in self.processors:
            context = processor.process(context)
        return context
