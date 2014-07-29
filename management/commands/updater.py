from django.core.management.base import BaseCommand
from sautadet import models
from sautadet import spouts
from multiprocessing import Pool

def update_feed(feed):
    print("Updating %s" % feed)
    spout = getattr(spouts, feed.spout).Spout(feed)
    spout.update()

class Command(BaseCommand):
    help = "Update everything"

    def handle(self, feed_id=None, **kwargs):
        if feed_id is None:
            queryset = models.Feed.objects.all()
        else:
            queryset = [models.Feed.objects.get(id=int(feed_id))]

        p = Pool(20)
        p.map(update_feed, queryset)
