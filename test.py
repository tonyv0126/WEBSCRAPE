from func_webscrap import scroll, extract, cleanse, graph, selenium, word_frequency
from wordcloud import WordCloud
from matplotlib import pyplot as plt

url = "https://www.afr.com/"

browser = selenium()
browser.get(url)
soup = scroll(browser)
result = extract(soup)
single_word = word_frequency(result)[3]

wordcloud = WordCloud(width = 1000, height = 500).generate_from_frequencies(single_word)

plt.figure(figsize=(15,8))
plt.imshow(wordcloud)
plt.axis("off")
plt.show()