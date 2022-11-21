from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from func_webscrap import scroll, extract, cleanse, graph, selenium, word_frequency
from matplotlib.figure import Figure



#Initiate Chrome browser using selenium


#URL
# url = "https://www.afr.com/"








# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/", methods = ["GET", "POST"])
def index():
    result = []
    words = []
   

    if request.method == "POST":
       url = request.form.get("url")

       browser = selenium()
       browser.get(url)
       soup = scroll(browser)
       result = extract(soup)
       single_word, bigram, trigram = word_frequency(result)

       return render_template("index.html", words = words, single_graph = graph(single_word, "Single"), bi_graph = graph(bigram, "Bigram"), tri_graph = graph(trigram, "trigram"))

      

    else:

      return render_template("index.html", words = words, graph = None)


