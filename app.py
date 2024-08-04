from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
from lxml import etree

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
POSTS_FILE = 'posts.json'
LIKES_FILE = 'likes.json'

ADMIN_PASSWORD = 'jupiter2024'

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
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

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
            'id': len(posts) + 1,  # Simple ID for each post
            'likes': 0  # Initialize likes for each post
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
    posts = load_posts()
    post = next((post for post in posts if post['id'] == post_id), None)
    if post:
        post['likes'] = post.get('likes', 0) + 1
        save_posts(posts)
        return jsonify({'likes': post['likes']})
    return jsonify({'error': 'Post not found'}), 404

# contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').lower()
    posts = load_posts()
    results = [post for post in posts if query in post['title'].lower() or query in post['content'].lower()]
    return render_template('search.html', posts=results, query=query)


@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    posts = load_posts()
    post = next((post for post in posts if post['id'] == post_id), None)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        post_date = request.form['date_time']
        images = request.files.getlist('images')
        image_urls = post['image_urls']

        if images:
            ensure_upload_folder_exists()
            image_urls = []
            for image in images:
                if image and image.filename != '':
                    filename = secure_filename(image.filename)
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image_urls.append(url_for('static', filename=f'uploads/{filename}'))

        post.update({
            'title': title,
            'content': content,
            'image_urls': image_urls,
            'date': post_date
        })
        save_posts(posts)

        # Generate sitemap whenever a post is edited
        generate_sitemap()

        flash('Post updated!', 'success')
        return redirect(url_for('view_post', post_id=post_id))

    return render_template('edit_post.html', post=post)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash('Invalid password', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

# search engine optimization-------------------------------


@app.route('/sitemap.xml', methods=['GET'])
def serve_sitemap():
    return app.send_static_file('sitemap.xml')


def generate_sitemap():
    with app.test_request_context():
        posts = load_posts()

        urlset = etree.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

        # Add static pages
        static_urls = [
            {'url': url_for('index', _external=True), 'last_modified': datetime.now().strftime('%Y-%m-%d')},
            {'url': url_for('about', _external=True), 'last_modified': datetime.now().strftime('%Y-%m-%d')},
            {'url': url_for('contact', _external=True), 'last_modified': datetime.now().strftime('%Y-%m-%d')}
        ]

        for static_url in static_urls:
            url = etree.SubElement(urlset, "url")
            loc = etree.SubElement(url, "loc")
            loc.text = static_url['url']

            lastmod = etree.SubElement(url, "lastmod")
            lastmod.text = static_url['last_modified']

            changefreq = etree.SubElement(url, "changefreq")
            changefreq.text = "monthly"

            priority = etree.SubElement(url, "priority")
            priority.text = "0.8"

        # Add post URLs
        for post in posts:
            url = etree.SubElement(urlset, "url")
            loc = etree.SubElement(url, "loc")
            loc.text = url_for('view_post', post_id=post['id'], _external=True)

            lastmod = etree.SubElement(url, "lastmod")
            lastmod.text = post['date']

            changefreq = etree.SubElement(url, "changefreq")
            changefreq.text = "weekly"

            priority = etree.SubElement(url, "priority")
            priority.text = "0.5"

        sitemap = etree.tostring(urlset, pretty_print=True, xml_declaration=True, encoding="UTF-8")

        with open("static/sitemap.xml", "wb") as f:
            f.write(sitemap)

if __name__ == '__main__':
    with app.app_context():
        generate_sitemap()
    app.run(debug=True)