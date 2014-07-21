from django.core.management.base import BaseCommand
from sautadet import models
from sautadet import spouts

class Command(BaseCommand):
    help = "Update everything"

    def handle(self, feed_id=None, **kwargs):
        if feed_id is None:
            queryset = models.Feed.objects.all()
        else:
            queryset = [models.Feed.objects.get(id=int(feed_id))]

        for feed in queryset:
            print("Updating %s" % feed)
            spout = getattr(spouts, feed.spout).Spout(feed)
            spout.update()
