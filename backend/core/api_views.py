from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def api_root(request, format=None):
    """Корневой API endpoint со списком всех доступных endpoints"""
    base_url = request.build_absolute_uri('/api/').rstrip('/')

    return Response({
        'lodges': {
            'list': f'{base_url}/lodges/',
            'types': f'{base_url}/lodges/types/',
        },
        'activities': {
            'list': f'{base_url}/activities/',
        },
        'events': {
            'list': f'{base_url}/events/',
        },
        'news': {
            'list': f'{base_url}/news/',
        },
        'restaurant': {
            'detail': f'{base_url}/restaurant/',
            'images': f'{base_url}/restaurant/images/',
            'meal-types': f'{base_url}/restaurant/meal-types/',
            'benefits': f'{base_url}/restaurant/benefits/',
        },
        'core': {
            'hero': f'{base_url}/hero/',
            'site-settings': f'{base_url}/site-settings/',
            'statistics': f'{base_url}/statistics/',
            'gallery': f'{base_url}/gallery/',
        },
        'sitemap': f'{base_url}/sitemap.xml',
        'robots': f'{base_url}/robots.txt',
    })

