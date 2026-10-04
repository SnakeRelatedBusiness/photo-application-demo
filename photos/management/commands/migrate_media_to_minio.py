import os
from pathlib import Path
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from photos.models import Photo

class Command(BaseCommand):
    help = "Migrates existing local media files to MinIO object storage"

    def handle(self, *args, **options):
        photos = Photo.objects.all()
        migrated_count = 0
        skipped_count = 0

        self.stdout.write(f"Found {photos.count} photo record in the databse. Starting migration...")

        for photo in photos:
            if not photo.image:
                continue

            local_path = Path.joinpath(settings.BASE_DIR, 'media', str(photo.image))

            if local_path.exists():
                try:
                    with open(local_path, 'rb') as f:
                        default_storage.save(photo.image.name, f)
                        migrated_count += 1
                        self.stdout.write(self.style.SUCCESS(f"Successfully migrated: {photo.image.name}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Failed to migrate {photo.image.name}: {e}"))

            else:
                skipped_count += 1
                self.stdout.write(self.style.WARNING(f"Local file missing for Photo ID {photo.id}: {local_path}"))


        self.stdout.write(
            self.style.SUCCESS(
                f"\nMigration complete! Migrated: {migrated_count}, Skipped (Missing locally): {skipped_count}"
            )
        )