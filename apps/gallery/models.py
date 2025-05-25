"""Gallery models.

Author: Jared Paubel
Version: 0.1
"""
from django.db import models
from django.utils.text import slugify
from photologue.models import Gallery, Photo
from taggit.managers import TaggableManager


class Country(models.Model):
    """A specified country."""
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


class City(models.Model):
    """A city that is located in a particular country."""
    name = models.CharField(max_length=100)
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='cities'
    )

    class Meta:
        unique_together = ('name', 'country')
        ordering = ['name']
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name


class CountryPhoto(Photo):
    """Extended Photo with country metadata."""

    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Country Photo"
        verbose_name_plural = "Country Photos"

    def save(self, *args, **kwargs):
        if self.country or self.city:
            if not self.title:
                self.title = "{}, {}".format(self.city, self.country)
            if not self.slug:
                self.slug = "{} {}".format(self.city, self.country)
        super().save(*args, **kwargs)


class CountryAlbum(models.Model):
    """A collection of albums for a specific country."""
    country = models.OneToOneField(
        Country,
        on_delete=models.CASCADE,
        related_name='album'
    )
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    tags = TaggableManager(blank=True)

    class Meta:
        verbose_name = "Country Album"
        verbose_name_plural = "Country Albums"

    def __str__(self):
        return f"{self.country}"

    def save(self, *args, **kwargs):
        if self.country:
            if not self.title:
                self.title = self.country
            if not self.slug:
                self.slug = slugify(self.country)
        super().save(*args, **kwargs)


class CityGallery(Gallery):
    """Gallery scoped to a specific city, belonging to a CountryAlbum."""
    album = models.ForeignKey(
        CountryAlbum,
        on_delete=models.CASCADE,
        related_name='city_galleries'
    )
    city = models.OneToOneField(
        City,
        on_delete=models.CASCADE,
        related_name='gallery'
    )

    class Meta:
        verbose_name = "City Gallery"
        verbose_name_plural = "City Galleries"

    def __str__(self):
        return f"{self.album.country} - {self.city}"

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = f"{self.city.name} Gallery"
        if not self.slug:
            self.slug = slugify(f"{self.city.name}-gallery")
        super().save(*args, **kwargs)
