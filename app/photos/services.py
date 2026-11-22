from django.utils.text import slugify
from .models import Tag, Photo

class TagService():
    @staticmethod
    def assign_tags_to_photo(tags : list[str], photo : Photo):

        if not photo.pk:
            raise ValueError("Photo must be saved to the database before assigning tags.")

        processed_tags = set(tag.strip().lower() for tag in tags if tag.strip())

        if not processed_tags:
            return

        tag_instances = []

        for name in processed_tags:
            if name.strip():
                tag, created = Tag.objects.get_or_create(
                    name=name.strip().lower(),
                    defaults={'slug': slugify(name)}
                )
                tag_instances.append(tag)

        photo.tags.add(*tag_instances)