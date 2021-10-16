import json

import requests
from bs4 import BeautifulSoup
from datetime import datetime # for time stamps
from celery.schedules import crontab # scheduler
from celery import Celery

app = Celery('tasks')  # defining the app name to be used in our flag
app.conf.beat_schedule = {
    # executes every 1 minute
    'scraping-task-one-min': {
        'task': 'tasks.hackernews_rss',
        'schedule': crontab()
    }
}

# Save articles to text file
@app.task
def save_function(article_list):
    # timestamp and filename
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    filename = 'articles-{}.json'.format(timestamp)
    with open(filename, 'w') as outfile:
        json.dump(article_list, outfile)


# Scraping function
@app.task
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
                'published': published,
                'created_at': str(datetime.now()),
                'source': 'HackerNews RSS'
            }
            article_list.append(article)
        return save_function(article_list)

    except Exception as e:
        print('The scraping job failed. See exception: ')
        print(e)


print('Starting scraping')
hackernews_rss()
print('Finished scraping')

