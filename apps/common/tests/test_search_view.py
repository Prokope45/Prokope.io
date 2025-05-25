"""Common test search view.

Author: Jared Paubel
Version: 0.1
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.http import urlencode

from apps.index.models import Index
from apps.blog.models import Post
from apps.gallery.models import City, Country, CountryAlbum, CityGallery


class TestSearchView(TestCase):
    """Test common search view."""

    def setUp(self):
        self.index_entry = Index.objects.create(
            about_me_title="My Journey",
            about_me_description="A long story...",
            about_prokope_title="Prokope Origins",
            about_prokope_description="Ancient tales..."
        )

        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='securepass123'
        )

        self.post = Post.objects.create(
            title="Exploring Django",
            content="Django is amazing!",
            author=self.user,
            slug="exploring-django"
        )
        self.post.tag.add("django")

        # TODO: Update search gallery tests.
        # self.gallery = Gallery.objects.create(
        #     title="Greek Islands",
        #     description="Blue and white houses"
        # )
        # self.photo = CountryAlbum.objects.create(
        #     country="Greece",
        #     slug="greek-islands"
        # )
        # self.photo.galleries.add(self.gallery)

    def test_empty_query_returns_no_results(self):
        response = self.client.get(reverse('search'))

        self.assertContains(
            response,
            text="No results found.",
            status_code=200
        )
        self.assertEqual(len(response.context['blog_results']), 0)
        self.assertIsNone(response.context['error_message'])

    def test_valid_query_returns_matching_index_and_blog(self):
        response = self.client.get(
            reverse('search') + '?' + urlencode({'q': 'Django'})
        )

        self.assertContains(response, text="Django", status_code=200)
        self.assertIn(self.post, response.context['blog_results'])
        self.assertEqual(response.context['error_message'], None)

    def test_query_matching_index_content(self):
        response = self.client.get(
            reverse('search') + '?' + urlencode({'q': 'Journey'})
        )
        self.assertContains(response, text="Journey", status_code=200)
        self.assertIn(self.index_entry, response.context['index_results']['about_me'])

    def test_sql_injection_pattern_blocks_search(self):
        response = self.client.get(
            reverse('search') + '?' + urlencode({'q': 'SELECT * FROM users;'})
        )

        self.assertContains(
            response,
            text="Invalid search query. Please refine your input.",
            status_code=200
        )
        self.assertEqual(len(response.context['blog_results']), 0)
        self.assertEqual(
            response.context['error_message'],
            "Invalid search query. Please refine your input."
        )

    # def test_query_matches_gallery_content(self):
    #     response = self.client.get(
    #         reverse('search') + '?' + urlencode({'q': 'Greece'})
    #     )

    #     self.assertContains(
    #         response,
    #         text="Santorini",
    #         status_code=200
    #     )
    #     self.assertIn(self.photo, response.context['gallery_results'])

    def test_tagged_search_returns_post(self):
        response = self.client.get(
            reverse('search') + '?' + urlencode({'q': 'django'})
        )

        self.assertContains(
            response,
            text="django",
            status_code=200
        )
        self.assertIn(self.post, response.context['blog_results'])
