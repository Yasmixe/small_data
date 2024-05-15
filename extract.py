import requests
from bs4 import BeautifulSoup
import spacy
from collections import Counter
import re


class AstronomyWordExtractor:
    def __init__(self, seed_urls, max_pages):
        self.seed_urls = seed_urls
        self.max_pages = max_pages
        self.visited_urls = set()
        self.words_counter = Counter()

        # Charger le modèle de traitement du langage naturel de SpaCy
        self.nlp = spacy.load("en_core_web_sm")

    def extract_words(self):
        for url in self.seed_urls:
            self._extract_words_from_url(url)
        return self.words_counter

    def _extract_words_from_url(self, url):
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

            # Extract text content from the page
            text = soup.get_text()

            # Utiliser SpaCy pour traiter le texte et extraire les mots pertinents
            doc = self.nlp(text)

            # Filtrer et compter les mots liés à l'astronomie
            astronomy_words = [
                token.text.lower()
                for token in doc
                if token.text.lower() == "astronomy" or "astro" in token.text.lower()
            ]
            self.words_counter.update(astronomy_words)

            for link in soup.find_all("a", href=True):
                next_url = urljoin(url, link["href"])
                if next_url not in self.visited_urls:
                    self._extract_words_from_url(next_url)

        except Exception as e:
            print(f"Error extracting words from {url}: {e}")


# Seed URLs
seed_urls = ["https://en.wikipedia.org/wiki/Astronomy"]

word_extractor = AstronomyWordExtractor(seed_urls, max_pages=10)
word_counter = word_extractor.extract_words()
# Afficher les mots pertinents
print("Mots pertinents liés à l'astronomie:")
for word, count in word_counter.items():
    print(f"{word}: {count}")
