from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
POSTS_FILE = 'posts.json'
LIKES_FILE = 'likes.json'


def ensure_upload_folder_exists():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])


def load_posts():
    if os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []


def save_posts(posts):
    with open(POSTS_FILE, 'w') as file:
        json.dump(posts, file)


def load_likes():
    if os.path.exists(LIKES_FILE):
        with open(LIKES_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}


def save_likes(likes):
    with open(LIKES_FILE, 'w') as file:
        json.dump(likes, file)


@app.route('/')
def index():
    posts = load_posts()
    return render_template('index.html', posts=posts)


@app.route('/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        post_date = request.form['date_time']
        images = request.files.getlist('images')
        image_urls = []

        ensure_upload_folder_exists()
        for image in images:
            if image and image.filename != '':
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_urls.append(url_for('static', filename=f'uploads/{filename}'))

        posts = load_posts()
        posts.append({
            'title': title,
            'content': content,
            'image_urls': image_urls,
            'date': post_date,
            'id': len(posts) + 1  # Simple ID for each post
        })
        save_posts(posts)

        flash('New post created!', 'success')
        return redirect(url_for('index'))
    return render_template('new_post.html')


@app.route('/post/<int:post_id>')
def view_post(post_id):
    posts = load_posts()
    post = next((post for post in posts if post['id'] == post_id), None)
    return render_template('view_post.html', post=post)


@app.route('/like/<int:post_id>', methods=['POST'])
def like_post(post_id):
    likes = load_likes()
    if str(post_id) in likes:
        likes[str(post_id)] += 1
    else:
        likes[str(post_id)] = 1
    save_likes(likes)
    return jsonify({'likes': likes[str(post_id)]})


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')



if __name__ == '__main__':
    app.run(debug=True)
