"""Gallery views tests.

Author: Jared Paubel
Version: 0.1
"""
from django.test import TestCase
from django.urls import reverse
from apps.gallery.models import (
    City, Country, CountryAlbum, CityGallery, CountryPhoto
)


class CountryGalleryListViewTests(TestCase):
    """Test country gallery list view."""

    def setUp(self):
        """Create clean test data for each test."""
        self.japan = Country.objects.create(name="Japan")
        self.country1 = CountryAlbum.objects.create(
            country=self.japan
        )
        self.brazil = Country.objects.create(name="Brazil")
        self.country2 = CountryAlbum.objects.create(
            country=self.brazil
        )

    def test_list_view_status_code(self):
        """Test that endpoint is reached with status 200."""
        response = self.client.get(reverse("gallery"))
        self.assertEqual(response.status_code, 200)

    def test_list_view_uses_template(self):
        """Test that endpoint uses correct template."""
        response = self.client.get(reverse("gallery"))
        self.assertTemplateUsed(response, "gallery.html")

    def test_list_view_context(self):
        """Test that context data is expected."""
        response = self.client.get(reverse("gallery"))
        self.assertIn("albums", response.context)
        countries = list(
            response.context["albums"].values_list("country", flat=True)
        )
        self.assertEqual(countries, [1, 2])


class CountryGalleryDetailViewTests(TestCase):
    """Test country gallery detail view."""

    def setUp(self):
        """Create clean test data for each test."""
        self.france = Country.objects.create(name="France")
        self.country = CountryAlbum.objects.create(
            country=self.france,
        )
        self.city_1 = City.objects.create(name="Paris", country=self.france)
        self.city_gallery_1 = CityGallery.objects.create(
            album=self.country,
            city=self.city_1
        )
        self.city_2 = City.objects.create(name="Lyon", country=self.france)
        self.city_gallery_2 = CityGallery.objects.create(
            album=self.country,
            city=self.city_2
        )
        self.photo_1 = CountryPhoto.objects.create(
            city=self.city_1,
            country=self.france,
            title="Eiffel Tower"
        )
        self.photo_2 = CountryPhoto.objects.create(
            city=self.city_2,
            country=self.france,
            title="Place Bellecour"
        )

    def test_detail_view_status_code(self):
        """Test that endpoint is reached with status 200."""
        response = self.client.get(
            reverse("gallery_detail", args=[self.country.slug])
        )
        self.assertEqual(response.status_code, 200)

    def test_detail_view_uses_template(self):
        """Test that endpoint uses correct template."""
        response = self.client.get(
            reverse("gallery_detail", args=[self.country.slug])
        )
        self.assertTemplateUsed(response, "gallery_detail.html")

    def test_detail_view_context(self):
        """Test that context data is expected."""
        response = self.client.get(
            reverse("gallery_detail", args=[self.country.slug])
        )
        self.assertEqual(response.context["gallery"], self.country)
        self.assertIn("city_galleries", response.context)
        self.assertIn("cities", response.context)
        self.assertIn("selected_city", response.context)

    def test_detail_view_404(self):
        """Test that endpoint displays 404 for invalid detail view."""
        response = self.client.get(
            reverse("gallery_detail", args=["non-existent-slug"])
        )
        self.assertEqual(response.status_code, 404)

    def test_detail_view_city_filter(self):
        """Test that city filter works correctly."""
        response = self.client.get(
            reverse("gallery_detail", args=[self.country.slug]),
            {'city': 'Paris'}
        )
        city_galleries = response.context['city_galleries']
        self.assertEqual(len(city_galleries), 1)
        self.assertEqual(city_galleries[0].city.name, "Paris")
