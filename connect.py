import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

app.config["MYSQL_DATABASE_HOST"] = "localhost"
app.config["MYSQL_DATABASE_PORT"] = 3306
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = "pass_root"
app.config["MYSQL_DATABASE_DB"] = "small_data"

mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()


cursor.execute("select * from small_data_url")

url = []
h1 = []

for row in cursor:
    url.append(row[0])
    h1.append(row[1])


cursor.close()
mot = "physics"
url_afficher = []
h1_afficher = []
for i, j in zip(url, h1):
    if mot in j:
        url_afficher.append(i)
        h1_afficher.append(j)
    else:
        if mot in i:
            url_afficher.append(i)
            h1_afficher.append(j)


for i, j in zip(url_afficher, h1_afficher):
    print(i, j)
    print("\n")
