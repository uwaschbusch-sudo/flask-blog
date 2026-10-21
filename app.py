import json
import os

from flask import Flask, render_template

app = Flask(__name__)

POSTS_FILE = os.path.join(os.path.dirname(__file__), "blog_posts.json")


def load_posts():
    """Liest die Beiträge aus der JSON-Datei."""
    with open(POSTS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


@app.route('/')
def index():
    """Zeigt alle Beiträge auf der Startseite."""
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)