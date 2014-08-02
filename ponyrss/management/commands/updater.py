from django.core.management.base import BaseCommand
from ponyrss import models
from ponyrss import spouts
from multiprocessing import Pool
from django.db.models import Q
import datetime

KEEP_READ_ARTICLE_FOR = datetime.timedelta(days=15)
KEEP_UNREAD_ARTICLE_FOR = datetime.timedelta(days=30)

def update_feed(feed):
    print("Updating %s" % feed)
    spout = getattr(spouts, feed.spout).Spout(feed)
    spout.update()

class Command(BaseCommand):
    help = "Update everything"

    def handle(self, feed_id=None, **kwargs):
        # Delete old entries

        #Qread = Q(read=True, date__lt=(datetime.datetime.now() - KEEP_READ_ARTICLE_FOR))
        #Qunread = Q(read=False, date__lt=(datetime.datetime.now() - KEEP_UNREAD_ARTICLE_FOR))

        #models.Entry.objects.filter(Qread | Qunread).delete()

        # Add new entries

        if feed_id is None:
            queryset = models.Feed.objects.all()
        else:
            queryset = [models.Feed.objects.get(id=int(feed_id))]

        p = Pool(20)
        p.map(update_feed, queryset)
