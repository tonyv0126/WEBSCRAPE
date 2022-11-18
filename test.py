# loading in all the essentials for data manipulation
import pandas as pd
import numpy as np
#load in the NTLK stopwords to remove articles, preposition and other words that are not actionable
from nltk.corpus import stopwords
# This allows to create individual objects from a bog of words
from nltk.tokenize import word_tokenize
# Lemmatizer helps to reduce words to the base formfrom nltk.stem import WordNetLemmatizer
# Ngrams allows to group words in common pairs or trigrams..etc
from nltk import ngrams
# We can use counter to count the objects from collections
from collections import Counter
# This is our visual library
import seaborn as sns
import matplotlib.pyplot as plt
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer


def word_frequency(sentence):
    # joins all the sentenses
    sentence ="".join(sentence)
    # creates tokens, creates lower class, removes numbers and lemmatizes the words
    new_tokens = word_tokenize(sentence)
    new_tokens = [t.lower() for t in new_tokens]
    new_tokens =[t for t in new_tokens if t not in stopwords.words('english')]
    new_tokens = [t for t in new_tokens if t.isalpha()]
    lemmatizer = WordNetLemmatizer()
    new_tokens =[lemmatizer.lemmatize(t) for t in new_tokens]
    #counts the words, pairs and trigrams
    counted = Counter(new_tokens)
    counted_2= Counter(ngrams(new_tokens,2))
    counted_3= Counter(ngrams(new_tokens,3))
    #creates 3 data frames and returns thems
    word_freq = pd.DataFrame(counted.items(),columns=['word','frequency']).sort_values(by='frequency',ascending=False)
    word_pairs =pd.DataFrame(counted_2.items(),columns=['pairs','frequency']).sort_values(by='frequency',ascending=False)
    trigrams =pd.DataFrame(counted_3.items(),columns=['trigrams','frequency']).sort_values(by='frequency',ascending=False)
    return word_freq,word_pairs,trigrams

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


os.system("export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2; exit;}'):0.0")

# url= "https://www.afr.com/"

# url = "https://www.fnlondon.com/"

# url =  "https://au.finance.yahoo.com/"

# url = "https://www.bloomberg.com/asia" #Need to solve robot wall


# #Requests method
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'html.parser')

#Selenium method
chrome_options = webdriver.ChromeOptions()
chrome_options.headless = False  #make selenium headless (Not open browser)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)





def scroll(browser):
    #Implement automatic scroll down the webpage.
    SCROLL_PAUSE_TIME = 1
    # Get scroll height
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height





# footer = soup.find('footer')
# footer.extract()







# section = soup.find('section', attrs ={'class': '_1x9L- _1iFjP'}) #main section of afr.com.au

def extract(soup, result):
    
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

    print(df)



URLS = ["https://www.afr.com/", "https://www.fnlondon.com/", "https://au.finance.yahoo.com/"]

result = []
for URL in URLS:
    driver.get(URL)

    #Scroll to bottom
    scroll(driver)

    #Convert html to beautiful soup format
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    
    #Extract headlines
    extract(soup, result)






data2, data3, data4 = word_frequency(result)

 
# create subplot of the different data frames
fig, axes = plt.subplots(3,1,figsize=(8,20))
sns.barplot(ax=axes[0],x='frequency',y='word',data=data2.head(30))
sns.barplot(ax=axes[1],x='frequency',y='pairs',data=data3.head(30))
sns.barplot(ax=axes[2],x='frequency',y='trigrams',data=data4.head(30))
plt.show()

