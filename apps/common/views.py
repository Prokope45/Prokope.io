from django.views.defaults import (
    page_not_found, bad_request, server_error, permission_denied
)

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.db.models import Q

from taggit.models import TaggedItem
import re

from apps.index.models import Index
from apps.blog.models import Post
from apps.gallery.models import CountryAlbum


def custom_bad_request_view(request, exception=None):
    return bad_request(request, exception, "errors/400.html")


def custom_page_not_found_view(request, exception=None):
    return page_not_found(request, exception, "errors/404.html")


def custom_permission_denied_view(request, exception=None):
    return permission_denied(
        request,
        exception,
        template_name='errors/403.html'
    )


def custom_error_view(request):
    return server_error(request, "errors/500.html")


def search(request: HttpRequest) -> HttpResponse:
    """Search the index, blog, and gallery for an related values to the term.

    Args:
        request (HttpRequest): Request containing search terms.

    Returns:
        HttpResponse: Response of found results.
    """
    query = request.GET.get('q', '').strip()

    about_me_results = []
    about_prokope_results = []
    blog_results = []
    gallery_results = []
    error_message = None

    if query:
        forbidden_patterns = re.compile(
            r'(DROP|SELECT|INSERT|DELETE|UPDATE|;|--)',
            re.IGNORECASE
        )

        if forbidden_patterns.search(query):
            error_message = "Invalid search query. Please refine your input."
            query = ''  # Clear the query to prevent further processing
        else:
            about_me_results = Index.objects.filter(
                Q(about_me_title__icontains=query) |
                Q(about_me_description__icontains=query)
            )
            about_prokope_results = Index.objects.filter(
                Q(about_prokope_title__icontains=query) |
                Q(about_prokope_description__icontains=query)
            )

            tag_ids = TaggedItem.objects.filter(
                tag__name__icontains=query
            ).values_list('object_id', flat=True)

            blog_results = Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(id__in=tag_ids)  # Search in tags
            ).distinct()

            gallery_results = CountryAlbum.objects.filter(
                Q(country__name__icontains=query) |
                Q(title__icontains=query) |
                Q(city_galleries__city__name__icontains=query) |
                Q(city_galleries__photos__title__icontains=query) |
                Q(city_galleries__photos__caption__icontains=query)
            ).distinct()

    context = {
        'index_results': {
            'about_me': about_me_results,
            'about_prokope': about_prokope_results,
        },
        'blog_results': blog_results,
        'gallery_results': gallery_results,
        'query': query,
        'error_message': error_message,
    }

    return render(request, 'search_results.html', context)
