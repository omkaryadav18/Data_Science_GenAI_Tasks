from flask import Flask, render_template, request, redirect, url_for
from models import db, URL
import string
import random
import validators

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

def generate_short_code(length=6):
    characters = string.ascii_letters +string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/', methods=['GET', 'POST'])
def home():
    short_url=None
    error = None

    if request.method == "POST":
        original_url = request.form.get('url')

        if not validators.url(original_url):
            error = "Invalid URL! Please enter a valid URL."
        else:
            existing = URL.query.filter_by(original_url=original_url).first()
            if existing:
                short_url=request.host_url + existing.short_code
            else:
                short_code = generate_short_code()
                new_url = URL(
                    original_url=original_url,
                    short_code=short_code
                )
                db.session.add(new_url)
                db.session.commit()
                short_url=request.host_url + short_code
    return render_template('home.html', short_url=short_url, error=error)

@app.route('/<short_code>')
def redirect_url(short_code):
    url_entry = URL.query.filter_by(short_code=short_code).first_or_404()
    return redirect(url_entry.original_url)

@app.route('/history')
def history():
    urls = URL.query.order_by(URL.created_at.desc()).all()
    return render_template('history.html',urls=urls)

if __name__ == '__main__':
    app.run(debug=True)