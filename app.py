import os
from flask import Flask, session,render_template, request,redirect,url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask.ext.bcrypt import Bcrypt



app = Flask(__name__)
bcrypt = Bcrypt(app)
# Check for environment variable
#if not os.getenv("DATABASE_URL"):
#   raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database (uncomment below before push)
#engine = create_engine(os.getenv("DATABASE_URL"))

#comment this before push
engine=create_engine("postgresql://postgres:bindu1973@localhost/project")
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

@app.route('signup')
def signup():
    return render_template("index.html")


@app.route("Register",methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    isUserUnique=db.execute("SELECT * FROM users WHERE username=:username","username":username).rowcount
    if isUserUnique==0:
        passhash = bcrypt.generate_password_hash(password).decode(‘utf-8’)
        db.execute("INSERT INTO users (username,passhash) values(:username,:passhash)","username":username,"passhash"=passhash)
        return redirect()

@app.route("/home",methods=["POST"])
def home():
    try:
        username = request.form.get("username")
        password = request.form.get("password")
    except ValueError:
        return render_template("index.html", message="Invalid password/username.")
    passhash= db.execute("SELECT passhash FROM users WHERE username=:username","username":username)
    if bcrypt.check_password_hash(passhash, password):
        return render_template("home.html",username=username)
    else:
        return render_template("index.html", message="Invalid password/username.")
    
  


