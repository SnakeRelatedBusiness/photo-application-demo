from django.db.models import Count
from django.db.models import QuerySet
from django.core.cache import cache

from photos.models import Photo

FEED_CACHE_TTL = 60 * 15  # Cache expires after 15 minutes

class PhotoFeedService():
    @staticmethod
    def get_feed(tag_slug : str | None = None, limit=50) -> QuerySet:
        cache_key = f"feed_cache_tag_{tag_slug}" if tag_slug else "feed_cache_global"

        cached_feed = cache.get(cache_key)
        if cached_feed is not None:
            return cached_feed

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

        cache.set(cache_key, photos, FEED_CACHE_TTL)
        return photos

    @staticmethod
    def invalidate_feed_cache():
        if hasattr(cache, 'delete_pattern'):
            cache.delete_pattern("feed_cache_*")