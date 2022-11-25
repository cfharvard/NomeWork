from flask import Flask, render_template, redirect, render_template, request, session
from flask_session import Session
from helpers import login_required

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/homepage")
@login_required
def homepage():
    return render_template("homepage.html")

@app.route("/classes")
def classes():
    return render_template("classes.html")

@app.route("/timer")
def timer():
    return render_template("timer.html")

@app.route("/analytics")
def analytics():
    return render_template("analytics.html")

@app.route("/login")
def login():
    return render_template("login.html")