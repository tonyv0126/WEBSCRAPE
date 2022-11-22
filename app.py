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
    results = []
    words = []
    urls = []
   

    if request.method == "POST":
       url1 = request.form.get("url1")
       url2 = request.form.get("url2")
       url3 = request.form.get("url3")
       urls.append(url1)
       urls.append(url2)
       urls.append(url3)
       browser = selenium()

       for url in urls:
         if url == "":
            pass
         else:
            browser.get(url)
            soup = scroll(browser)
            result = extract(soup)
            results.append(result)

       single_word, bigram, trigram, cloud = word_frequency(result)

       return render_template("index.html", cloud = graph(cloud,"cloud"), single_graph = graph(single_word, "Single"), bi_graph = graph(bigram, "Bigram"), tri_graph = graph(trigram, "trigram"))

      

    else:

      return render_template("index.html", words = words, graph = None)


