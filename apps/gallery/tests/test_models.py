"""Gallery models tests.

Author: Jared Paubel
Version: 0.1
"""
from django.test import TestCase
from apps.gallery.models import (
    City, Country, CountryAlbum, CountryPhoto, CityGallery
)
from django.utils.text import slugify


class CountryAlbumModelTests(TestCase):
    """Country Album model tests."""

    def setUp(self):
        """Create clean test data for each test."""
        self.france = Country.objects.create(name="France")
        self.country_1 = CountryAlbum.objects.create(
            country=self.france,
        )
        self.japan = Country.objects.create(name="Japan")
        self.country_2 = CountryAlbum.objects.create(
            country=self.japan,
        )

    def test_create_country_album(self):
        """Test creation of a new country album."""
        self.assertEqual(self.country_1.country.name, "France")
        self.assertEqual(self.country_1.slug, "france")

    def test_model_name(self):
        """Test model name."""
        self.assertEqual(str(self.country_1), "France")

    def test_slug_creation(self):
        """Test slug is created automatically."""
        self.assertEqual(
            self.country_1.slug,
            slugify(self.country_1.country.name)
        )


class CityGalleryModelTests(TestCase):
    """City Album model tests."""

    def setUp(self):
        """Create clean test data for each test."""
        self.italy = Country.objects.create(name="Italy")
        self.country = CountryAlbum.objects.create(
            country=self.italy,
        )
        self.rome = City.objects.create(name="Rome", country=self.italy)
        self.city_1 = CityGallery.objects.create(
            album=self.country,
            city=self.rome
        )

    def test_create_city_album(self):
        """Test creation of a new city album."""
        self.assertEqual(self.city_1.city.name, "Rome")

    def test_model_name(self):
        """Test model name."""
        self.assertEqual(str(self.city_1), "Italy - Rome")


class CountryPhotoModelTests(TestCase):
    """Country Photo model tests."""

    def setUp(self):
        """Create clean test data for each test."""
        self.spain = Country.objects.create(name="Spain")
        self.country_album = CountryAlbum.objects.create(country=self.spain)
        self.city = City.objects.create(name="Barcelona", country=self.spain)
        self.city_gallery = CityGallery.objects.create(
            album=self.country_album,
            city=self.city
        )
        self.photo_1 = CountryPhoto.objects.create(
            city=self.city,
            country=self.spain,
            title="Park Güell",
        )

    def test_create_country_photo(self):
        """Test creation of country photo."""
        self.assertEqual(self.photo_1.title, "Park Güell")

    def test_model_name(self):
        """Test model name."""
        self.assertEqual(str(self.photo_1), "Park Güell")
