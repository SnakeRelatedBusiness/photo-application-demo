"""
URL configuration for photo_application project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from photos.views import PhotoUploadView, PhotoDetailView, PhotoDeleteView
from interactions.views import ToggleLikeView
from feed.views import GlobalFeedView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api-auth/', include('rest_framework.urls')),

    path('api/photos/upload/', PhotoUploadView.as_view(), name='photo-upload'),
    path('api/photos/<int:pk>/', PhotoDetailView.as_view(), name='photo-detail'),
    path('api/photos/<int:photo_id>/like/', ToggleLikeView.as_view(), name='toggle-like'),
    path('api/photos/<int:pk>/delete/', PhotoDeleteView.as_view(), name='photo-delete'),
    path('api/feed/', GlobalFeedView.as_view(), name='global-feed'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)