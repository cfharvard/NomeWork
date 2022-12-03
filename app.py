from flask import Flask, render_template, redirect, render_template, request, session, flash, get_flashed_messages
from flask_session import Session
from helpers import login_required
import json
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

con = sqlite3.connect("nomework.db", check_same_thread=False)
db = con.cursor()

@app.route("/")
def index():
    if session.get('logged_in') == True:
        return render_template("homepage.html") 
    else:
        return render_template("index.html")

@app.route("/analytics")
@login_required
def analytics():
    return render_template("analytics.html")

@app.route("/homepage")
@login_required
def classes():
    return render_template("homepage.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        # checks if username is entered
        if not request.form.get("username"):
            flash('Enter Username')
            return render_template("register.html") 

        # checks if password is entered
        if not request.form.get("password"):
            flash('Enter Password')
            return render_template("register.html") 

        # checks if confirm is entered
        if not request.form.get("confirmation"):
            flash('Enter Confirmation')
            return render_template("register.html") 

        # check if password and confirm are the same
        if request.form.get("password") != request.form.get("confirmation"):
            flash('Password and Confirmation do not match')
            return render_template("register.html") 

        # rows with that username (should be 0 b/c username shouldn't taken)
        db.execute("SELECT username FROM users WHERE username=?;", [request.form.get("username")])
        rows = db.fetchone()

        # check if username is already taken
        if rows is not None:
            flash('Username is already taken')
            return render_template("register.html") 

        # hash password
        hashed = generate_password_hash(request.form.get("password"))

        # add username and password to database users table after passing all cases
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (request.form.get("username"), hashed))
        con.commit()

        # get id from updated users table
        rows = db.execute("SELECT id FROM users WHERE username=?", [request.form.get("username")])

        # log user in
        session["user_id"] = rows.fetchall()[0]

        return render_template("login.html")

    # when requested via get, display registration form
    else:
        return render_template("register.html")

@app.route("/login", methods=['GET', 'POST'])
def login(): 
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash('Enter Username')
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash('Enter Password')
            return render_template("login.html")
        
        username_field = request.form.get("username")

        # Query database for username
        db.execute("SELECT username FROM users WHERE username = ?", [username_field])
        username = db.fetchone()
   
        db.execute("SELECT hash FROM users WHERE username = ?", [username_field])
        pwhash = db.fetchone()

        # Ensure username exists and password is correct
        # if rows is None or not check_password_hash(rows.fetchall()[0], request.form.get("password")):
        #     flash('Username or Password is incorrect')
        #     return render_template("login.html")

        if username is None or not check_password_hash(pwhash[0], request.form.get("password")):
            flash('Username or Password is incorrect')
            return render_template("login.html")
   
        # Remember which user has logged in
        session["user_id"] = username[0]

        # Redirect user to home page
        return render_template("homepage.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route('/ProcessSeconds', methods=["GET","POST"])
def ProcessSeconds():
    if request.method == "POST":
        seconds = request.json("seconds")
        print(seconds)
    flash('Submitted!')
    return render_template("timer.html")
    
@app.route("/timer", methods=['GET', 'POST'])
@login_required
def timer():
    return render_template("timer.html")

@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


