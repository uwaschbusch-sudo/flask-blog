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


def fetch_post_by_id(posts, post_id):
    """Gibt den Beitrag mit der ID zurück oder None."""
    for post in posts:
        if post["id"] == post_id:
            return post
    return None


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
            "likes": 0,
        }
        blog_posts.append(new_post)
        save_posts(blog_posts)
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Löscht den Beitrag mit der angegebenen ID."""
    blog_posts = load_posts()
    blog_posts = [post for post in blog_posts if post["id"] != post_id]
    save_posts(blog_posts)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Zeigt das Formular oder speichert den geänderten Beitrag."""
    blog_posts = load_posts()
    post = fetch_post_by_id(blog_posts, post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        post["author"] = request.form.get("author")
        post["title"] = request.form.get("title")
        post["content"] = request.form.get("content")
        save_posts(blog_posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


@app.route('/like/<int:post_id>')
def like(post_id):
    """Erhöht die Like-Zahl des Beitrags um 1."""
    blog_posts = load_posts()
    post = fetch_post_by_id(blog_posts, post_id)
    if post is None:
        return "Post not found", 404

    post["likes"] = post.get("likes", 0) + 1
    save_posts(blog_posts)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)