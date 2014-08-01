import json
import datetime
import time
from django import forms
import feedparser
from ponyrss import models

feedparser.SANITIZE_HTML = 0

class Form(forms.Form):
    url = forms.CharField()

class Spout:
    description = "A normal RSS feed."
    form = Form

    def __init__(self, feed):
        self.feed = feed
        self.rss_url = json.loads(self.feed.spout_options)['url']

    def update(self):
        self.rss = feedparser.parse(self.rss_url)

        for rss_entry in self.rss.entries:
            try:
                entry = self.feed.entries.get(url=rss_entry.link)
            except models.Entry.DoesNotExist:
                entry = models.Entry(url=rss_entry.link)

            entry.title = rss_entry.title

            if not entry.read:
                entry.content = self.get_entry_content(entry, rss_entry)

            try:
                entry.date = datetime.datetime.fromtimestamp(time.mktime(rss_entry.published_parsed))
            except AttributeError:
                entry.date = entry.date or datetime.datetime.now()

            entry.score = self.get_entry_score(entry, rss_entry)
            entry.feed = self.feed

            entry.save()

    def get_entry_score(self, entry, rss_entry):
        return 0

    def get_entry_content(self, entry, rss_entry):
        content = ''
        if hasattr(rss_entry, 'content'):
            for e in rss_entry.content:
                if len(e['value']) > len(content):
                    content = e['value']
        elif hasattr(rss_entry, 'summary'):
            content = rss_entry.summary
        assert content
        return content
