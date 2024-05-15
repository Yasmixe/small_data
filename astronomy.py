import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL


class ExternalLinkCrawler:

    def __init__(self, seed_urls, max_pages):
        self.seed_urls = seed_urls
        self.max_pages = max_pages
        self.visited_urls = set()
        self.external_links = set()

    def crawl(self):
        for url in self.seed_urls:
            self._crawl_url(url)
        return self.external_links

    def _crawl_url(self, url):
        if len(self.visited_urls) >= self.max_pages:
            return

        if url in self.visited_urls:
            return

        try:
            response = requests.get(url)
            if response.status_code != 200:
                return

            soup = BeautifulSoup(response.content, "html.parser")
            self.visited_urls.add(url)

            parsed_url = urlparse(url)
            domain = parsed_url.netloc

            for link in soup.find_all("a", href=True):
                next_url = urljoin(url, link["href"])
                next_parsed_url = urlparse(next_url)
                if next_parsed_url.netloc != domain:
                    self.external_links.add(next_url)

            for link in soup.find_all("a", href=True):
                next_url = urljoin(url, link["href"])
                if next_url not in self.visited_urls:
                    self._crawl_url(next_url)

        except Exception as e:
            print(f"Error crawling {url}: {e}")


# Seed URLs
seed_urls = ["https://en.wikipedia.org/wiki/Astronomy"]
app = Flask(__name__)

mysql = MySQL()

app.config["MYSQL_DATABASE_HOST"] = "localhost"
app.config["MYSQL_DATABASE_PORT"] = 3306
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = "pass_root"
app.config["MYSQL_DATABASE_DB"] = "small_data"

mysql.init_app(app)
crawler = ExternalLinkCrawler(seed_urls, max_pages=10)
external_links = crawler.crawl()

url_astro = []

for link in external_links:
    url_astro.append(link)

h1_contents = []

for url in external_links:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            h1_tag = soup.find("h1")
            if h1_tag:
                h1_content = h1_tag.text.strip()
                h1_contents.append(h1_content)
                print(h1_content)
            else:
                h2_tag = soup.find("h2")
                if h1_tag:
                    h1_content = h2_tag.text.strip()
                    h1_contents.append(h1_content)
                    print(h1_content)
        else:
            h1_contents.append("astronomy")
    except Exception as e:
        h1_contents.append("astronomy ")


for link, title in zip(external_links, h1_contents):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO small_data_url(url, h1) VALUES (%s, %s)",
        (link, title),
    )
    conn.commit()
    url_astro.append(link)
    cursor.close()
    conn.close()
