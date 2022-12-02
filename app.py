from flask import Flask, render_template, redirect, render_template, request, session
from flask_session import Session
from helpers import login_required, generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
Session(app)

con = sqlite3.connect("nomework.db")
db = con.cursor()

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/analytics")
@login_required
def analytics():
    return render_template("analytics.html")

@app.route("/register")
def register():
    if request.method == "POST":
        # checks if username is entered
        if not request.form.get("username"):
            return render_template("register.html") 

        # checks if password is entered
        if not request.form.get("password"):
            return render_template("register.html") 

        # checks if confirm is entered
        if not request.form.get("confirmation"):
            return render_template("register.html") 

        # password length check
        if len(request.form.get("password")):
            return render_template("register.html") 

        # check if password and confirm are the same
        if request.form.get("password") != request.form.get("confirmation"):
            return render_template("register.html") 

        # rows with that username (should be 0 b/c username shouldn't taken)
        rows = db.execute("SELECT username FROM users WHERE username=?", request.form.get("username"))

        # check if username is already taken
        if len(rows) == 1:
            return render_template("register.html") 

        # hash password
        hashed = generate_password_hash(request.form.get("password"))

        # add username and password to database users table after passing all cases
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), hashed)

        # get id from updated users table
        rows = db.execute("SELECT id FROM users WHERE username=?", request.form.get("username"))

        # log user in
        session["user_id"] = rows[0]["id"]

        return redirect("/")

    # when requested via get, display registration form
    else:
        return render_template("register.html")

@app.route("/login")
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/timer")
#@login_required
def timer():
    return render_template("timer.html")

