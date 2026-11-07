from django.db.models import Count
from django.db.models import QuerySet

from photos.models import Photo

class PhotoFeedService():
    @staticmethod
    def get_feed(tag_slug : str | None = None, limit=50) -> QuerySet:
        query = Photo.objects.select_related(
            'user'
            ).prefetch_related(
                'tags'
                ).annotate(
                    total_likes=Count('likes')
                    )


        if tag_slug:
            query = query.filter(tags__slug=tag_slug.lower())

        photos = list(query.order_by('-uploaded_at')[:limit])

        return photos