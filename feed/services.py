import logging

from django.db.models import Count
from django.db.models import QuerySet
from django.core.cache import cache

from photos.models import Photo

logger = logging.getLogger(__name__)

FEED_CACHE_PREFIX = "feed_cache_"
FEED_CACHE_TTL = 60 * 15  # Cache expires after 15 minutes

class PhotoFeedService():
    @staticmethod
    def _cache_key(tag_slug: str | None, limit: int) -> str:
        if tag_slug:
            return f"{FEED_CACHE_PREFIX}tag_{tag_slug.lower()}_{limit}"
        return f"{FEED_CACHE_PREFIX}all_{limit}"

    @staticmethod
    def get_feed(tag_slug: str | None = None, limit: int = 50) -> list[Photo]:
        cache_key = PhotoFeedService._cache_key(tag_slug, limit)

        cached_feed = cache.get(cache_key)
        if cached_feed is not None:
            logger.info("CACHE HIT: feed key '%s'", cache_key)
            return cached_feed

        logger.info("CACHE MISS: querying PostgreSQL for key '%s'", cache_key)

        query = (
            Photo.objects
            .select_related("user")
            .prefetch_related("tags")
            .annotate(total_likes=Count("likes"))
        )
        if tag_slug:
            query = query.filter(tags__slug=tag_slug.lower())

        photos = list(query.order_by("-uploaded_at")[:limit])
        cache.set(cache_key, photos, FEED_CACHE_TTL)
        return photos

    @staticmethod
    def invalidate_feed_cache() -> None:
        deleted = cache.delete_pattern(f"{FEED_CACHE_PREFIX}*")
        logger.info("Feed cache invalidated, %s keys deleted", deleted)