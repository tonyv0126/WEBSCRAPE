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
def selenium():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = False  #make selenium headless (Not open browser)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


driver = selenium()



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




words=[]
for line in result:
    token = re.findall('\w+', line.lower())
    words.extend(token)
   

    


# download the package
nltk.download("stopwords")
# remove stop words
sw= set(nltk.corpus.stopwords.words('english'))
print(sw)

#list of words with stop words removed
words_ns = [x for x in words if x not in sw]



#Grpah frequency of words
sns.set_style('darkgrid')
nlp_words=nltk.FreqDist(words_ns)
nlp_words.plot(50)
