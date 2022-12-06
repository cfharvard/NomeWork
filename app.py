from flask import Flask, render_template, redirect, render_template, request, session, flash, get_flashed_messages
from flask_session import Session
from helpers import login_required
import json
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date

# Initializes app for the user
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

con = sqlite3.connect("nomework.db", check_same_thread=False)
db = con.cursor()
time = 0

@app.route("/", methods=['GET', 'POST'])
@login_required
def index():
    if request.method == "POST":
        # Logs user in
        db.execute("INSERT INTO classes (name, user_id) VALUES (?, ?)", [request.form.get("classname"), session["user_id"]])
        con.commit()
        return redirect("/")

    else:
        # Selects list of user's classes from the database to be displayed
        db.execute("SELECT name FROM classes WHERE user_id = ?", [session["user_id"]])
        userclasses = db.fetchall()

        classes = []
        for x in range(len(userclasses)):
            classes.append(userclasses[x][0])
        
        # Selects class ids from databse to find class times
        db.execute("SELECT id FROM classes WHERE user_id = ?", [session["user_id"]])
        classesid = db.fetchall()

        ids = []
        for x in range(len(classesid)):
            ids.append(classesid[x][0])
        
        # Selects class times from the database to be displayed
        classtimes = []
        for x in ids:
            db.execute("SELECT SUM(seconds) FROM times WHERE class_id = ?", [x])
            times = db.fetchone()[0]
            classtimes.append(times)
        
        for x in range(len(classtimes)):
            if classtimes[x] == None:
                classtimes[x] = 0

        tabledata = list(zip(classes, classtimes))

        

        db.execute("SELECT name FROM classes WHERE user_id = ?", [session["user_id"]])
        userclasses = db.fetchall()

        classes = []
        for x in range(len(userclasses)):
            classes.append(userclasses[x][0])
        return render_template("index.html", tabledata=tabledata, classes=classes)

@app.route("/delete", methods=['POST'])
@login_required
def delete():
    # Deletes classes from user's table
    db.execute("DELETE FROM classes WHERE name = ?", [request.form.get("class")])
    return redirect("/")

@app.route("/analytics", methods=['GET', 'POST'])
@login_required
def analytics():
    if request.method == "POST":
        # Generates drop down menu
        db.execute("SELECT name FROM classes WHERE user_id = ?", [session["user_id"]])
        userclasses = db.fetchall()

        classes = []
        for x in range(len(userclasses)):
            classes.append(userclasses[x][0])
        
        # Requests the class to make a graph of
        class_graph = request.form.get("classanalytics")
        db.execute("SELECT SUM(seconds), date FROM times WHERE class_id = (SELECT id FROM classes WHERE name = ?) GROUP BY date", [class_graph])
        data = db.fetchall()
        print(data)

        seconds = [row[0] for row in data]

        # Formats time into hours to be displayed on the graph
        hours = ["{:.2f}".format(time/3600) for time in seconds]
        dates = [row[1] for row in data]

        return render_template("analytics.html", classes = classes, class_graph=class_graph, hours=hours, dates=dates)

    else:
        # Generates drop down menu
        db.execute("SELECT name FROM classes WHERE user_id = ?", [session["user_id"]])
        userclasses = db.fetchall()

        classes = []
        for x in range(len(userclasses)):
            classes.append(userclasses[x][0])
        
        return render_template("analytics.html", classes=classes)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        # Checks if username is entered
        if not request.form.get("username"):
            flash('Enter Username')
            return render_template("register.html") 

        # Checks if password is entered
        if not request.form.get("password"):
            flash('Enter Password')
            return render_template("register.html") 

        # Checks if confirm is entered
        if not request.form.get("confirmation"):
            flash('Enter Confirmation')
            return render_template("register.html") 

        # Check if password and confirm are the same
        if request.form.get("password") != request.form.get("confirmation"):
            flash('Password and Confirmation do not match')
            return render_template("register.html") 

        # Rows with that username (should be 0 b/c username shouldn't taken)
        db.execute("SELECT username FROM users WHERE username=?;", [request.form.get("username")])
        rows = db.fetchone()

        # Check if username is already taken
        if rows is not None:
            flash('Username is already taken')
            return render_template("register.html") 

        # Hash password
        hashed = generate_password_hash(request.form.get("password"))

        # Add username and password to database users table after passing all cases
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (request.form.get("username"), hashed))
        con.commit()

        # Get id from updated users table
        rows = db.execute("SELECT id FROM users WHERE username=?", [request.form.get("username")])

        return render_template("login.html")

    # When requested via get, display registration form
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

        if username is None or not check_password_hash(pwhash[0], request.form.get("password")):
            flash('Username or Password is incorrect')
            return render_template("login.html")
   
        # Remember which user has logged in
        session["user_id"] = username[0]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route('/submit/<string:seconds>', methods=["GET","POST"])
@login_required
def submit(seconds):
    global time
    time = json.loads(seconds)
    
    return redirect("/timer")
    
@app.route("/timer", methods=["GET","POST"])
@login_required
def timer():
    if request.method == "POST":
        global time
        
        classname = request.form.get("class")

        # add seconds to database
        db.execute("SELECT id FROM classes WHERE user_id = ? AND name = ?", [session["user_id"], classname])
        classid = db.fetchone()[0]

        # changes seconds to hour format
        #time = "{:.2f}".format(time/3600)

        today = date.today()

        db.execute("INSERT INTO times (seconds, user_id, class_id, date) VALUES (?, ?, ?, ?)", [time, session["user_id"], classid, today])
        con.commit()

        db.execute("SELECT name FROM classes WHERE user_id = ?", [session["user_id"]])
        userclasses = db.fetchall()

        classes = []
        for x in range(len(userclasses)):
            classes.append(userclasses[x][0])

        return render_template("timer.html", classes=classes)

    else:
        db.execute("SELECT name FROM classes WHERE user_id = ?", [session["user_id"]])
        userclasses = db.fetchall()

        classes = []
        for x in range(len(userclasses)):
            classes.append(userclasses[x][0])
        
        return render_template("timer.html", classes=classes)
    
@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


