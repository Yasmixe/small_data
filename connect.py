import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL

h1_contents = []

import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/Astronomy"

try:
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        h1_tag = soup.find("h1")
        if h1_tag:
            h1_content = h1_tag.text.strip()
            print("Contenu de la balise <h1>:", h1_content)
        else:
            print("La balise <h1> n'a pas été trouvée sur la page.")
            h2_tag = soup.find("h2")
            h2_content = h2_tag.text.strip()
            print("Contenu de la balise <h2>:", h2_content)

    else:
        print("La requête HTTP a échoué avec le code de statut:", response.status_code)
except Exception as e:
    print("Une erreur s'est produite lors de la récupération du contenu de la page:", e)
