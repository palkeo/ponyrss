from readability import Document
from ponyrss import models
import requests
import json
from django import forms
import datetime
import logging

class Form(forms.Form):
    pass

class Spout:
    description = "Shaarli."
    form = Form

    base_url = 'https://nexen.mkdir.fr/shaarli-api/top?interval=48h'

    def __init__(self, feed):
        self.feed = feed

    def get_entries(self):
        r = requests.get(self.base_url, verify=False)
        assert r.status_code == 200
        d = json.loads(r.text)

        d = []
        for entry in json.loads(r.text):
            d.append((entry['title'], int(entry['count']), entry['permalink']))

        return d

    def update(self):
        for title, score, link in self.get_entries():
            try:
                entry = self.feed.entries.get(url=link)
            except models.Entry.DoesNotExist:
                entry = models.Entry(url=link)

            entry.date = entry.date or datetime.datetime.now()
            entry.feed = self.feed

            entry.title = title
            entry.score = score
            entry.link = link

            if not entry.read:
                try:
                    entry.content = self.get_entry_content(link)
                except Exception as e:
                    logging.error("Unable to get an entry : %s" % e)
                    continue

            entry.save()

    def get_entry_content(self, link):
        r = requests.get(link)
        assert r.status_code == 200
        return Document(r.text).summary()

