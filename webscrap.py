import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service




url= "https://www.afr.com/"

# #Selenium method
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# driver.get(url)
# content = driver.page_source
# soup = BeautifulSoup(content, 'html.parser')

#Requests method
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

result = []
title = soup.title #Get title block of the HTML

h1 = soup.findAll('h1')  #All the elements with tag h1
h2 = soup.findAll('h2')  #All the elements with tag h2




section = soup.find('section', attrs ={'class': '_1x9L- _1iFjP'}) #main section of afr.com.au

for element in section:
    headlines = element.findAll('a')
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