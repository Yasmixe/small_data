from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

# Configuration de la base de données
app.config["MYSQL_DATABASE_HOST"] = "localhost"
app.config["MYSQL_DATABASE_PORT"] = 3306
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = "pass_root"
app.config["MYSQL_DATABASE_DB"] = "small_data"

mysql.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["GET"])
def search():
    # Récupérer le mot clé saisi par l'utilisateur
    keyword = request.args.get("keyword")

    # Connexion à la base de données et exécution de la recherche
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM small_data_url")

    url_afficher = []
    h1_afficher = []

    for row in cursor:
        if keyword in row[1] or keyword in row[0]:
            url_afficher.append(row[0])
            h1_afficher.append(row[1])

    cursor.close()
    conn.close()

    return render_template("resultats.html", urls=zip(url_afficher, h1_afficher))


if __name__ == "__main__":
    app.run(debug=True)
