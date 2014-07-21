from sautadet.spouts.rss import Spout as RSSpout
import requests
import json
from urllib.parse import urlparse
from lxml.html import html5parser
from django import forms

class Form(forms.Form):
    content = forms.ChoiceField(choices=(
        ('https://linuxfr.org/journaux', 'journaux'),
        ('https://linuxfr.org/news', 'dépêches'),
        ('https://linuxfr.org/forums', 'forums')
    ))

class Spout(RSSpout):
    description = "LinuxFR content."
    form = Form

    def __init__(self, feed):
        self.feed = feed
        self.page_url = json.loads(self.feed.spout_options)['content']
        self.rss_url = self.page_url + '.atom'

    def update(self):

        r = requests.get(self.page_url, verify=False)
        assert r.status_code == 200
        tree = html5parser.fromstring(r.text)

        self.link_scores = {}
        for article in tree.xpath("//*[local-name()='article']"):
            link = article.xpath(".//*[local-name()='span' and @class='anonymous_reader']/*[local-name()='a']/@href")
            assert len(link) == 1
            score = article.xpath(".//*[local-name()='figure' and @class='score']/text()")
            assert len(score) == 1
            self.link_scores[link[0]] = int(score[0])

        super().update()

    def get_entry_score(self, entry, rss_entry):
        link_path = urlparse(rss_entry.link).path
        return self.link_scores[link_path]
