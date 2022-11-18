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


#Selenium method
def selenium():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = False  #make selenium headless (Not open browser)
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
            break
        last_height = new_height


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

