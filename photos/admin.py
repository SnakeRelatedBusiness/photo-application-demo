from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Photo, Tag

class TagInline(admin.TabularInline):
    model = Photo.tags.through
    extra = 1

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    inlines = [TagInline]


admin.site.register(Tag)
