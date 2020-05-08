import os
from flask import Flask, session,render_template, request,redirect,url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests



app = Flask(__name__)
#bcrypt = Bcrypt(app)
# Check for environment variable
#if not os.getenv("DATABASE_URL"):
#   raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
KEY="6iGmZfPMsrgbm0i8iqfcw"


# Set up database (uncomment below before push)
#engine = create_engine(os.getenv("DATABASE_URL"))

#comment this before push
engine=create_engine("postgresql://postgres:password@localhost/project1")
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def root():

    #if session["id"]!=None:
    #    return redirect(url_for('home'))
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


@app.route("/home",methods=["POST","GET"])
def home():
   # if session["id"]==None:
   #     return render_template("index.html",message="noob!!<br> login to access")
    if(request.method=="GET"):
        return render_template("home.html",username=session["username"])
    try:
        username = request.form.get("username")
        password = request.form.get("password")
    except ValueError:
        return render_template("index.html", message="Invalid password/username.")
    usercount= db.execute("SELECT * FROM users WHERE username=:username and passhash=:password",{'username':username,'password':password}).rowcount
    user= db.execute("SELECT * FROM users WHERE username=:username and passhash=:password",{'username':username,'password':password}).fetchone()
    
    if usercount!=0:
        session["id"]=user[0]
        session["username"]=user[1]
        return render_template("home.html",username=username)
    else:
        return render_template("index.html", message="Invalid password/username.")

@app.route("/title")
def title():
  #  if session["id"]==None:
   #     return render_template("index.html",message="noob!!<br> login to access")

    return render_template("search.html",username=session["username"],name="title",next="title_search")
    
@app.route("/isbn")
def isbn():
  #  if session["id"]!=None:
  #      return render_template("search.html",username=session["username"],name="isbn",next="isbn_search")
  #  else:
    return render_template("index.html",message="noob!!<br> login to access")
@app.route("/author")
def author():
  #  if session["id"]!=None:
    return render_template("search.html",username=session["username"],name="author",next="author_search")
 #   else:
   #     return render_template("index.html",message="noob!!<br> login to access")



@app.route("/title_search",methods=["post"])
def title_search():
    try:
        title=request.form.get("title")
    except ValueError:
        return render_template("home.html",username=session["username"])
    result=db.execute("SELECT * FROM books WHERE title LIKE ('%'|| :title || '%')",{"title":title})
    return render_template("result.html",name="title",username=session["username"],search_type="Title",search=title,result=result,next="title_search")


@app.route("/isbn_search",methods=["post"])
def isbn_search():
    try:
        isbn=request.form.get("isbn")
    except ValueError:
        return render_template("home.html",username=session["username"])    
    result=db.execute("SELECT * FROM books WHERE isbn LIKE ('%' || :isbn || '%')",{"isbn":isbn})
    return render_template("result.html",name="isbn",username=session["username"],search_type="ISBN",search=isbn,result=result,next="isbn_search")

@app.route("/author_search",methods=["post"])
def author_search():
    try:
        author=request.form.get("author")
    except ValueError:
        return render_template("home.html",username=session["username"])
    
    result=db.execute("SELECT * FROM books WHERE title LIKE ('%' || :author || '%')",{"author":author})
    return render_template("result.html",name="author",username=session["username"],search_type="Author",search=title,result=result,next="author_search")

@app.route("/books")
def books():
    return redirect(url_for('home'))


@app.route("/books/<int:book_id>")
def book(book_id):
    if True:
        book=db.execute("SELECT * FROM books WHERE id=:id",{"id":book_id}).fetchone()
        
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": KEY, "isbns": book.isbn})
        res=res.json()
        reviews=db.execute("SELECT * FROM reviews WHERE bookid=:id",{"id":book_id}).fetchall()
        return render_template("book.html",username=session["username"],book=book,rating=res['books'][0]['average_rating'],reviews=reviews)
    else:
        return render_template("index.html",message="noob!!<br> login to access")

    
@app.route("/bookreview/<int:bookid>",methods=["POST"])
def bookreview(bookid):
    if request.method == "POST":
        try:
            rating=request.form.get("rating")
            review=request.form.get("review")
        except ValueError:
            return render_template("home.html",username=session["username"])
        check=db.execute("SELECT * FROM reviews WHERE bookid=:bookid AND userid=:userid",{"bookid":bookid,"userid":session["id"]}).rowcount
        if check==0:
            db.execute("INSERT INTO reviews (rating,review,userid,bookid) values (:rating,:review,:userid,:bookid)",{"rating":rating,"review":review,"userid":session["id"],"bookid":bookid})
            db.commit()
        else:
            book=db.execute("SELECT * FROM books WHERE id=:id",{"id":bookid}).fetchone()       
            res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": KEY, "isbns": book.isbn})
            res=res.json()
            reviews=db.execute("SELECT * FROM reviews WHERE bookid=:id",{"id":bookid}).fetchall()
            return render_template("book.html",username=session["username"],book=book,rating=res['books'][0]['average_rating'],reviews=reviews,error="You can review only once :(")
            
    return redirect(url_for('book',book_id=bookid))
        

