from photos.models import Photo
from django.db.models import Count

def get_global_feed(limit=50):
    """
    Retrieves the latest photos and annotates them with their like count.
    In Phase 4 (Microservices), this function will be rewritten to make 
    HTTP or gRPC network calls to the Photo and Interaction microservices 
    instead of using the Django ORM to query the local database.
    """
    return Photo.objects.select_related('user').annotate(
        total_likes=Count('likes')
    ).order_by('-uploaded_at')[:limit]