import time
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import nltk
import re
import matplotlib.pyplot as plt
import seaborn as sns
import io
import urllib, base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
# This allows to create individual objects from a bog of words
from nltk.tokenize import word_tokenize
# Lemmatizer helps to reduce words to the base formfrom nltk.stem import WordNetLemmatizer
# Ngrams allows to group words in common pairs or trigrams..etc
from nltk import ngrams
# We can use counter to count the objects from collections
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from wordcloud import WordCloud





os.system("export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2; exit;}'):0.0")


#Selenium method
def selenium():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True  #make selenium headless (Not open browser)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver



def scroll(browser):
    #Implement automatic scroll down the webpage.
    SCROLL_PAUSE_TIME = 1
    # Get scroll height
    last_height = browser.execute_script("return document.documentElement.scrollHeight")

    while True:
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            content = browser.page_source
            soup = BeautifulSoup(content, 'html.parser')
            return soup
        last_height = new_height


def extract(soup):
    result = []
    headlines = soup.findAll('a')
    print("Number of link: {}".format(len(headlines)))
    
    for headline in headlines:
        text = headline.text
        if len(text.split()) > 3 and not ("newsletter") in text:
            if ("min ago" or "mins ago") in text:
                result.append(text.partition('AM' or 'PM')[2])
            else:
                result.append(text)

    df =pd.DataFrame({'headlines' : result})   
    df.to_csv('headlines.csv', index = False, encoding='utf-8')

    return result



def cleanse(result):
    words=[]
    for line in result:
        token = re.findall('\w+', line.lower())
        words.extend(token)
    # download the package
    nltk.download("stopwords")
    # remove stop words
    sw= set(nltk.corpus.stopwords.words('english'))       
    #list of words with stop words removed
    words_ns = [x for x in words if x not in sw]
    #Grpah frequency of words
    sns.set_style('darkgrid')
    return words_ns
   

def graph(data, type):

      # Generate plot
    if type == "pie":
        fig = plt.figure()
        plt.rcParams["figure.autolayout"] = True
        plt.margins(x=0, y=0)
        labels = list(data.keys())
        values = list(data.values())
        plt.pie(values, autopct='%1.1f%%', textprops={'fontsize': 18})
        plt.legend(labels=labels, bbox_to_anchor=(1,0.5), loc="center right", fontsize=12, bbox_transform=plt.gcf().transFigure) 

        # Convert plot to PNG image
        pngImage = io.BytesIO()
        FigureCanvas(fig).print_png(pngImage)

        # Encode PNG image to base64 string
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    
    elif type == "cloud":

        wordcloud = WordCloud(width = 1000, height = 500, stopwords=["aussie"], background_color="white").generate_from_frequencies(data)
        plt.figure(figsize=(15,10))
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.rcParams["figure.autolayout"] = True
        plt.margins(x=0, y=0)
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        pngImageB64String = 'data:image/png;base64,' + urllib.parse.quote(string)

       

    else:
        fig, ax = plt.subplots()
        sns.barplot(ax=ax,x='frequency',y='word',data=data.head(20))
        plt.rcParams["figure.autolayout"] = True
        plt.margins(x=0, y=0)
            # Convert plot to PNG image
        pngImage = io.BytesIO()
        FigureCanvas(fig).print_png(pngImage)

        # Encode PNG image to base64 string
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')

   
    return pngImageB64String


        
def word_frequency(sentence_list):
    common_words = ["financial", "australian", "stock", "aussie", "australia", "share"]
    # joins all the sentenses
    sentence_list ="".join(sentence_list)
    # creates tokens, creates lower class, removes numbers and lemmatizes the words
    new_tokens = word_tokenize(sentence_list)
    new_tokens = [t.lower() for t in new_tokens]
    new_tokens =[t for t in new_tokens if t not in stopwords.words('english')]
    new_tokens = [t for t in new_tokens if t.isalpha()]
    new_tokens = [t for t in new_tokens if t not in common_words]
    lemmatizer = WordNetLemmatizer()
    new_tokens =[lemmatizer.lemmatize(t) for t in new_tokens]
    #counts the words, pairs 
    counted = Counter(new_tokens)
    counted_2= Counter(ngrams(new_tokens,2))
    #creates 3 data frames and returns thems
    single_word = pd.DataFrame(counted.items(),columns=['word','frequency']).sort_values(by='frequency',ascending=False)
    word_pairs =pd.DataFrame(counted_2.items(),columns=['word','frequency']).sort_values(by='frequency',ascending=False)
    return single_word,word_pairs, counted




