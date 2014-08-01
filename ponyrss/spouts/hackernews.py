from readability import Document
from ponyrss import models
import requests
from lxml.html import html5parser
from urllib.parse import urljoin
from django import forms
import datetime
import logging
from .shaarli import Spout as ShaarliSpout

def group(lst, n):
    assert len(lst) % n == 0
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

class Spout(ShaarliSpout):
    description = "HackerNews frontpage."

    xpath_entry = "//*[local-name()='table']//*[local-name()='table']//*[local-name()='tr']"
    xpath_link = ".//*[@class='title']/*[local-name()='a']/@href"
    xpath_title = ".//*[@class='title']/*[local-name()='a']/text()"
    xpath_score = ".//*[@class='subtext']/*[local-name()='span']/text()"

    base_url = 'https://news.ycombinator.com'

    def __init__(self, feed):
        self.feed = feed

    def get_entries(self):
        r = requests.get(self.base_url, verify=False)
        assert r.status_code == 200
        tree = html5parser.fromstring(r.text)

        d = []
        for entry1, entry2, entry3 in group(tree.xpath(self.xpath_entry)[1:], 3):
            link = entry1.xpath(self.xpath_link)
            assert len(link) in (0, 1)
            if len(link) == 0:
                break
            title = entry1.xpath(self.xpath_title)
            assert len(title) == 1
            score = entry2.xpath(self.xpath_score)
            assert len(score) in (0, 1)
            if len(score) == 0:
                continue

            link = urljoin(self.base_url, link[0])
            title = title[0]
            score = int(score[0].split()[0])

            d.append((title, score, link))

        assert len(d) > 10
        return d
