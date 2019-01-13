import os, requests, xml.etree.ElementTree

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        x = db.execute('SELECT password FROM users WHERE email = :email', {'email': email}).fetchone()
        if x['password'] == password:
            session['logged_in'] = True
            session['email'] = email
            return index()
        else:
            return 'Incorrect username or password. Please try again.'
    if request.method == "GET":
        return render_template("login.html")

@app.route("/logout")
def logout():
    session['logged_in']=False
    session['email'] = None
    return index()

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

@app.route("/confirmation", methods=["POST", "GET"])
def confirmation():
        pwd = request.form.get('psw')
        email = request.form.get('email')
        email_check = db.execute("SELECT email FROM users WHERE email = :email",{'email':email}).fetchone()
        if email_check['email'] == email:
            return f"Your email {email} already has an account associated with it. Please log in <a href='/login'> here <a>"
        db.execute("INSERT INTO users (email, password) VALUES(:email,:pwd)",{"email":email, "pwd":pwd})
        db.commit()
        return "Success"

@app.route("/<string:isbn>", methods=["POST", "GET"])
def book():
    book_data = db.execute("SELECT * FROM books WHERE isbn=:isbn"){"isbn":isbn}).fetchone()
    title = book_data['title']
    author = book_data['author']
    year = book_data['year']
    '''
    text = request.form.get('search')
    res = requests.get("https://www.goodreads.com/search/index.xml", params={'key':'EOquiAwYzuZQkS4FGKIQ', 'q':text})
    '''
    render_template("book.html", title=title, author=author, year = year)
    