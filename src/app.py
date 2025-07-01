from flask import Flask, render_template, url_for
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

def w_definitions(word):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT def FROM words WHERE word = ? COLLATE NOCASE", (escape(word), ))

    defi = cur.fetchall()
    res = [''.join(i) for i in defi] #tuples to list

    con.close()
    return res

if __name__ == "__main__":
    app.run(debug=False)
