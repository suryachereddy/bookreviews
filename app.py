import os
from flask import Flask, session,render_template, request,redirect,url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker



app = Flask(__name__)
#bcrypt = Bcrypt(app)
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
engine=create_engine("postgresql://postgres:password@localhost/project1")
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def root():
    return redirect(url_for('signin'))

@app.route('/signin')
def signin():
    return render_template("index.html")
@app.route('/signup')
def signup():
    return render_template("signup.html")


@app.route("/register",methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    isUserUnique=db.execute("SELECT * FROM users WHERE username=:username",{"username":username}).rowcount
    if isUserUnique==0:
        #passhash = bcrypt.generate_password_hash(password).decode(‘utf-8’)
        db.execute("INSERT INTO users (username,passhash) values(:username,:passhash)",{'username':username,'passhash':password})
        db.commit()
        return render_template("registered.html")
    else:
        return render_template("signup.html",message="Please choose another username.")


@app.route("/home",methods=["POST"])
def home():
    try:
        username = request.form.get("username")
        password = request.form.get("password")
    except ValueError:
        return render_template("index.html", message="Invalid password/username.")
    passhashlist= db.execute("SELECT * FROM users WHERE username=:username and passhash=:password",{'username':username,'password':password}).rowcount
    
    print(passhashlist)
    if passhashlist!=0:
        return render_template("home.html",username=username)
    else:
        return render_template("index.html", message="Invalid password/username.")
    
  


