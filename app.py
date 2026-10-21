import json
import os

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

POSTS_FILE = os.path.join(os.path.dirname(__file__), "blog_posts.json")


def load_posts():
    """Liest die Beiträge aus der JSON-Datei."""
    with open(POSTS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_posts(posts):
    """Schreibt die Beiträge in die JSON-Datei."""
    with open(POSTS_FILE, "w", encoding="utf-8") as file:
        json.dump(posts, file, indent=4, ensure_ascii=False)


def generate_id(posts):
    """Gibt die nächste freie ID zurück."""
    return max((post["id"] for post in posts), default=0) + 1


@app.route('/')
def index():
    """Zeigt alle Beiträge auf der Startseite."""
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Zeigt das Formular oder speichert einen neuen Beitrag."""
    if request.method == 'POST':
        blog_posts = load_posts()
        new_post = {
            "id": generate_id(blog_posts),
            "author": request.form.get("author"),
            "title": request.form.get("title"),
            "content": request.form.get("content"),
        }
        blog_posts.append(new_post)
        save_posts(blog_posts)
        return redirect(url_for('index'))

    return render_template('add.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
