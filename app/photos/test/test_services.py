from django.test import TestCase

from photos.services import TagService
from photos.models import Photo, Tag
from accounts.models import AppUser

class TagServiceTests(TestCase):
    def setUp(self):
        self.user = AppUser.objects.create()
        self.user.save()

        self.photo = Photo.objects.create(user=self.user)

    def test_tags_assigned_successfully(self):
        test_tags = ["tag1", "tag2"]

        TagService.assign_tags_to_photo(
            photo=self.photo,
            tags=test_tags
        )

        tags = self.photo.tags.all().order_by("name")

        self.assertEqual(len(tags), len(test_tags))
        self.assertTrue(Tag.objects.filter(slug='tag1').exists())
        self.assertTrue(Tag.objects.filter(slug='tag2').exists())

    def test_tag_normalisation(self):
        test_tags = ["CAPS TAG", "Title Tag"]

        TagService.assign_tags_to_photo(
            photo=self.photo,
            tags=test_tags
        )

        self.assertTrue(Tag.objects.filter(slug='caps-tag').exists())
        self.assertTrue(Tag.objects.filter(slug='title-tag').exists())

    def test_empty_string_ignored(self):
        test_tags = ["tag", ""]

        TagService.assign_tags_to_photo(
            photo=self.photo,
            tags=test_tags
        )

        self.assertEqual(self.photo.tags.count(), 1)


    def test_unsaved_photo_raises_value_error(self):
        photo = Photo(user=self.user) # created unsaved image

        with self.assertRaises(ValueError):
            TagService.assign_tags_to_photo(
                tags=["test", "tags"],
                photo=photo,
                )
