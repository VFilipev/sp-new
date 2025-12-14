from django.contrib.sitemaps import Sitemap
from lodges.models import LodgeType, Lodge
from news.models import News
from activities.models import Activity
from events.models import EventType


class LodgeTypeSitemap(Sitemap):
    """Sitemap для типов размещения"""
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return LodgeType.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else None


class LodgeSitemap(Sitemap):
    """Sitemap для размещений"""
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Lodge.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else None


class NewsSitemap(Sitemap):
    """Sitemap для новостей"""
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return News.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at


class ActivitySitemap(Sitemap):
    """Sitemap для активностей"""
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Activity.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else None


class EventTypeSitemap(Sitemap):
    """Sitemap для типов мероприятий"""
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return EventType.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else None

