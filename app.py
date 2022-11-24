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

@app.route("/login")
def login():
    return render_template("login.html")
