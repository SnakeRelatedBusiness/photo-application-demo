from dataclasses import dataclass
from typing import List, Optional

from django.contrib.auth.models import User
from rest_framework.serializers import Serializer

from .models import Photo

@dataclass
class PhotoUploadContext:
    """Carries the state of a photo upload through the processing pipeline."""
    user: User
    tags: List[str]
    serializer: Serializer
    photo: Optional[Photo] = None