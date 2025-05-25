"""Gallery urls.

Author: Jared Paubel
Version: 0.1
"""
from django.urls import path
from apps.gallery.views import CountryGalleryList, CountryGalleryDetail


urlpatterns = [
    path('', CountryGalleryList.as_view(), name='gallery'),
    path(
        '<slug:slug>/',
        CountryGalleryDetail.as_view(),
        name='gallery_detail'
    ),
]
