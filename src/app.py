from flask import Flask, render_template, url_for, jsonify
from markupsafe import escape
import sqlite3
import os

app = Flask(__name__)
current_dir = os.path.dirname(os.path.abspath(__file__))
DATABASE = f"{current_dir}/dictionary.db"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/words/<word>")
def word_def(word):
    definitions = w_definitions(word)
    return render_template("word.html", word=word, definitions=definitions)


@app.route("/api/<word>")
def api_def(word):
    definitions = w_definitions(word)
    data = {"word": word, "definitions": definitions}
    return jsonify(data)


def w_definitions(word):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT def FROM words WHERE word = ? COLLATE NOCASE", (escape(word),))

    defi = cur.fetchall()
    res = ["".join(i) for i in defi]  # tuples to list

    con.close()
    return res


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=False)
