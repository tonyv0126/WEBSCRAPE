from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from func_webscrap import scroll, extract, selenium


#Initiate Chrome browser using selenium


#URL
# url = "https://www.afr.com/"








# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/", methods = ["GET", "POST"])
def index():

    if request.method == "POST":
       url = request.form.get("url")
       browser = selenium()
       browser.get(url)
       scroll(browser)



    return render_template("index.html")


