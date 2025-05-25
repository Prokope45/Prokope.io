"""Gallery admin.

Author: Jared Paubel
Version: 0.1
"""
from django.contrib import admin
from apps.gallery.models import (
    CountryAlbum,
    CityGallery,
    CountryPhoto,
    City,
    Country
)
from photologue.admin import (
    PhotoAdmin as BasePhotoAdmin
)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['country']


@admin.register(CountryPhoto)
class CountryPhotoAdmin(BasePhotoAdmin):
    autocomplete_fields = ['country', 'city']


class CityGalleryInline(admin.StackedInline):
    model = CityGallery
    extra = 0
    show_change_link = True
    fields = [
        'city', 'date_added', 'is_public', 'photos'
    ]
    filter_horizontal = ['photos']
    exclude = ('title', 'slug',)


@admin.register(CountryAlbum)
class CountryGalleryAdmin(admin.ModelAdmin):
    autocomplete_fields = ['country']
    inlines = [CityGalleryInline]
    exclude = ('title', 'slug',)
