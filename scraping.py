import json

import requests
from bs4 import BeautifulSoup


# Save articles to text file
def save_function(article_list):
    with open('articles.txt', 'w') as outfile:
        json.dump(article_list, outfile)


# Scraping function
def hackernews_rss():
    article_list = []
    try:
        r = requests.get('https://news.ycombinator.com/rss')
        soup = BeautifulSoup(r.content, "html.parser")
        articles = soup.findAll('item')
        for article in articles:
            title = article.find('title').text
            link = article.find('link').text
            published = article.find('pubdate').text

            article = {
                'title': title,
                'link': link,
                'published': published
            }
            article_list.append(article)
        return save_function(article_list)

    except Exception as e:
        print('The scraping job failed. See exception: ')
        print(e)


print('Starting scraping')
hackernews_rss()
print('Finished scraping')
