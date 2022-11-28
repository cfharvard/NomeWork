from flask import Flask, render_template, redirect, render_template, request, session
from flask_session import Session
from helpers import login_required

app = Flask(__name__)
Session(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analytics")
@login_required
def analytics():
    return render_template("analytics.html")
    
@app.route("/classes")
@login_required
def classes():
    return render_template("classes.html") 

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/timer")
@login_required
def timer():
    return render_template("timer.html")

