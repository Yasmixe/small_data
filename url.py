import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin


class Crawler:
    def __init__(self, max_pages, urls=[]):
        self.max_pages = max_pages
        self.urls_ro_visit = urls
        self.visiting_urls = []

    def valid_url(self, url):
        r = requests.get(url)
        if r.status_code == 200:
            print(r.status_code)
            soup = BeautifulSoup(r.content, "html.parser")
            return soup
        else:
            print("Erreur")
            print(r.status_code)
            return None

    def domaine(self, url):
        domaine = re.search(r"w?[a-v|x-z][\w%\+-\.]+\.(org|fr|com|net)", url)
        domaine_site = domaine.group()
        return domaine_site

    def get_internal_url(self, url):
        html = self.valid_url(url)
        domaine_site = self.domaine(url)

        for link in html.find_all("a"):
            if "href" in link.attrs:
                if domaine_site in link.attrs["href"]:
                    if "http" in link.attrs["href"]:
                        print(link.attrs["href"])
                else:
                    if link.attrs["href"].startswith("/"):
                        internal_link = urljoin(url, link.attrs["href"])
                        if domaine_site in internal_link:
                            print(internal_link)


Crawler(max_pages=5).get_internal_url("https://www.google.com/")
