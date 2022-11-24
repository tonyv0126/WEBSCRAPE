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
app.config['SECRET_KEY'] = 'anystringthatyoulike'



@app.route("/", methods = ["GET", "POST"])
def index():
    results = []
    urls = []
    weight = {}
    number_of_urls = 2
   

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


       single_word, bigram, trigram, cloud = word_frequency(results)

       return render_template("index.html", pie_chart = graph(weight, "pie"), cloud = graph(cloud,"cloud"), single_graph = graph(single_word, "Single"), bi_graph = graph(bigram, "Bigram"), tri_graph = graph(trigram, "trigram"), number_of_urls = number_of_urls)

      

    else:

      return render_template("index.html", number_of_urls = number_of_urls)


