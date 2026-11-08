from django.test import TestCase
from django.core.cache import cache

from accounts.models import AppUser
from photos.models import Photo, Tag
from feed.services import PhotoFeedService


class FeedServiceTests(TestCase):
    def setUp(self):
        cache.clear()

        self.user = AppUser.objects.create_user(username='testuser')
        self.photo1 = Photo.objects.create(user=self.user, caption='Photo 1')
        self.tag = Tag.objects.create(name='Test Tag', slug='test-tag')
        self.photo1.tags.add(self.tag)

    def test_get_feed_cache_miss_writes_to_redis(self):
        self.assertIsNone(cache.get("feed_cache_global"))

        feed = PhotoFeedService.get_feed()

        self.assertEqual(len(feed), 1)
        self.assertIsNotNone(cache.get("feed_cache_global"))

    def test_get_feed_cache_hit_prevents_db_read(self):
        PhotoFeedService.get_feed(tag_slug=self.tag.slug)

        with self.assertNumQueries(0):
            cached_feed = PhotoFeedService.get_feed(tag_slug=self.tag.slug)

        self.assertEqual(len(cached_feed), 1)

    def test_get_feed_with_tag_creates_new_cache_key(self):
        PhotoFeedService.get_feed(tag_slug="test")

        self.assertIsNotNone(cache.get("feed_cache_tag_test"))
        self.assertIsNone(cache.get("feed_cache_global"))

    def test_invalidate_feed_cache_clears_all_caches(self):
        cache.set("feed_cache_global", [])
        cache.set("feed_cache_tag_test", [])

        PhotoFeedService.invalidate_feed_cache()

        self.assertIsNone(cache.get("feed_cache_global"))
        self.assertIsNone(cache.get("feed_cache_tag_test"))
