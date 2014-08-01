from django.db import models
from django.core.urlresolvers import reverse

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Feed(models.Model):
    title = models.CharField(help_text="Title of the feed", max_length=255)

    tags = models.ManyToManyField(Tag, related_name='feeds')

    # in an entry, score = base_score + mult_score * entry_score
    base_score = models.FloatField()
    mult_score = models.FloatField()

    spout = models.CharField(max_length=255)
    spout_options = models.TextField(help_text="JSON-encoded options for this spout")

    last_update = models.DateTimeField()

    def __str__(self):
        return "%s (%s)" % (self.title, self.spout)
    
    def get_comma_separated_tags(self):
        return ', '.join(tag.name for tag in self.tags.all())

    def get_absolute_url(self):
        return reverse('ponyrss-feed_entries', args=[self.id])

    class Meta:
        ordering = ('-base_score',)
    
class Entry(models.Model):
    feed = models.ForeignKey(Feed, related_name='entries')

    read = models.BooleanField(default=False)

    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    date = models.DateTimeField()

    url = models.TextField(blank=True)
    score = models.FloatField(default=0)

    # Automatically set.
    total_score = models.FloatField()

    def save(self, *args, **kwargs):
        self.total_score = self.feed.base_score + self.feed.mult_score * self.score
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('read', '-total_score', 'date')
        verbose_name_plural = 'entries'
        unique_together = ('url', 'feed')
