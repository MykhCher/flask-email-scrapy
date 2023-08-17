"""
A server file where all the routing and ASGI setup implemented.
"""

import crochet
crochet.setup()

import os
import time
import json
import asyncio

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask.wrappers import Response
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
from scraping import ScrapingSpider

# Initialize the client.
app = Flask(__name__)

# Initialize data container. 
# This is where our email adresses will be stored.
output_data = [] 
url_to_crawl = []
crawl_runner = CrawlerRunner()


@app.route("/")
def index() -> str:
    """
    Render a page with form, where user submits url to crawl from.
    """
    return render_template('index.html')

@app.route("/", methods=['POST', ])
def submit() -> str:
    """
    Recieve and validate URL, pass it into the scraping function.
    """
    if len(url_to_crawl) != 0:
        url_to_crawl.clear()
    url_to_crawl.append(request.form['url'])
    
    output_data.clear()
    if os.path.exists("data.json"): 
        os.remove("data.json")
        
    return redirect(url_for('scrape'))

@app.route("/scrape")
async def scrape() -> Response:
    """
    Launch scrapy script.
    """

    scrape_with_crochet(baseURL=url_to_crawl[0]) # Passing that URL to our Scraping Function

    await asyncio.sleep(20) # Pause the function while the scrapy spider is running

    json_obj = json.dumps(output_data, indent=4)
    with open("data.json", "w") as outfile:
        outfile.write(json_obj)

    return jsonify(output_data)

@crochet.run_in_reactor
def scrape_with_crochet(baseURL):
    # This will connect to the dispatcher that will kind of loop the code between these two functions.
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    
    # This will connect to the ReviewspiderSpider function in our scrapy file and after each yield will pass to the crawler_result function.
    eventual = crawl_runner.crawl(ScrapingSpider, category = baseURL)
    return eventual

#This will append the data to the output data list.
def _crawler_result(item, response, spider):
    output_data.append(dict(item))


if __name__ == '__main__':
    app.run(threaded=True)


# https://www.scrapebay.com/data_tables/