from sautadet.spouts.rss import Spout as RSSpout
import requests
from readability import Document

class Spout(RSSpout):
    description = "A RSS feed, but all the entries are fetched on the website using readability."

    def get_entry_content(self, entry, rss_entry):
        try:
            r = requests.get(rss_entry.link)
            assert r.status_code == 200
        except Exception:
            return '<div class="alert alert-warning" role="alert">Unable to get the full article with readability, because the page didn\'t load :(</div>\n' + super().get_entry_content(entry, rss_entry)
        return Document(r.text).summary()
