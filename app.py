from flask import Flask, flash, redirect, render_template, request, session, url_for
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
app.config['SECRET_KEY'] = 'anystringthatyoulike'



@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response




@app.route("/", methods = ["GET", "POST"])
def index():
    results = []
    urls = []
    weight = {}
   

    if request.method == "POST":
   
       url = request.form.getlist("url")
       urls.extend(url)
       browser = selenium()

       for url in urls:
         if url == "":
            pass
         else:
            try:

               browser.get(url)
               soup = scroll(browser)
               headlines = extract(soup)
               results.extend(headlines)
               no_headlines = len(headlines)
               weight[url] = no_headlines
            except:
               flash('Invalid URL, Please try again')
               return render_template("index.html")


       single_word, bigram, cloud = word_frequency(results)

      #  return render_template("index.html", pie_chart = graph(weight, "pie"), cloud = graph(cloud,"cloud"), single_graph = graph(single_word, "Single"), bi_graph = graph(bigram, "Bigram"), tri_graph = graph(trigram, "trigram"))
       return render_template("index.html", pie_chart = graph(weight, "pie"), cloud = graph(cloud,"cloud"), single_graph = graph(single_word, "Single"), bi_graph = graph(bigram, "Bigram"))
      

    else:

      return render_template("index.html")





