from django.test import TestCase, override_settings
from django.core.cache import cache

from accounts.models import AppUser
from photos.models import Photo, Tag
from feed.services import PhotoFeedService

@override_settings(
    CACHES={
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'test-snowflake',
        }
    }
)

class FeedServiceTests(TestCase):
    def setUp(self):
        cache.clear()

        self.user = AppUser.objects.create_user(username='testuser')
        self.photo1 = Photo.objects.create(user=self.user, caption='Photo 1')
        self.tag = Tag.objects.create(name='Test Tag', slug='test-tag')
        self.photo1.tags.add(self.tag)

    def test_get_feed_cache_miss_writes_to_redis(self):
        global_key = PhotoFeedService._cache_key(tag_slug=None, limit=50)
        self.assertIsNone(cache.get(global_key))

        feed = PhotoFeedService.get_feed()

        self.assertEqual(len(feed), 1)
        self.assertIsNotNone(cache.get(global_key))

    def test_get_feed_cache_hit_prevents_db_read(self):
        PhotoFeedService._cache_key(tag_slug=self.tag.slug, limit=50)

        PhotoFeedService.get_feed(tag_slug=self.tag.slug)

        with self.assertNumQueries(0):
            cached_feed = PhotoFeedService.get_feed(tag_slug=self.tag.slug)

        self.assertEqual(len(cached_feed), 1)

    def test_get_feed_with_tag_creates_new_cache_key(self):
        PhotoFeedService.get_feed(tag_slug="test")

        tag_key = PhotoFeedService._cache_key(tag_slug="test", limit=50)
        global_key = PhotoFeedService._cache_key(tag_slug=None, limit=50)

        self.assertIsNotNone(cache.get(tag_key))
        self.assertIsNone(cache.get(global_key))

    def test_invalidate_feed_cache_clears_all_caches(self):
        global_key = PhotoFeedService._cache_key(tag_slug=None, limit=50)
        tag_key = PhotoFeedService._cache_key(tag_slug="test", limit=50)

        cache.set(global_key, [])
        cache.set(tag_key, [])

        PhotoFeedService.invalidate_feed_cache()

        self.assertIsNone(cache.get(global_key))
        self.assertIsNone(cache.get(tag_key))
