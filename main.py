"""
A server file where all the routing and ASGI setup implemented.
"""

import crochet
crochet.setup()

import os
import json
import asyncio
import requests

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
    Launch scrapy script. Call Golang script to insert data into MongoDB.
    """

    # Passing URL to Scraping Function.
    scrape_with_crochet(baseURL=url_to_crawl[0]) 

    # Pause the function while the scrapy spider is running.
    await asyncio.sleep(3) 

    # Write result into data.json file.
    json_obj = json.dumps(output_data, indent=4)
    with open("data.json", "w") as outfile:
        outfile.write(json_obj)
    
    # Call Golang script to insert data into MongoDB
    for item in output_data:
        golang_url = "http://localhost:8081/insert"
        response = requests.post(golang_url, json=item)
        if response.status_code != 200:
            return jsonify({"error": "Failed to insert data into Golang script"})

    return jsonify(output_data)

@crochet.run_in_reactor
def scrape_with_crochet(baseURL: str):
    """
    Connect to the dispatcher that will kind of loop the code 
    between this function and `crawler_result(item, response, spider)`.
    """
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    
    # This will connect to the spider function in scrapy file and after each yield will pass to the crawler_result function.
    eventual = crawl_runner.crawl(ScrapingSpider, category = baseURL)
    return eventual

def _crawler_result(item, response, spider):
    """
    Append the data to the output data list.
    """
    output_data.append(dict(item))


if __name__ == '__main__':
    app.run(threaded=True)
