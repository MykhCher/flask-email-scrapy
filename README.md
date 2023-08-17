# Flask E-Mail Scraping

You are welcome at the page of Flask E-Mail Scraping project. Here I will use [Flask](https://flask.palletsprojects.com/en/2.3.x/) and [Scrapy](https://scrapy.org/) to implement the scrapping of mails from different websites. 

I also plan to use [Golang](https://go.dev/) as connector to a [Mongo](https://www.mongodb.com/) database and [Docker](https://www.docker.com/). Project is still in development.

## Set up
Project is still in development, though, you can use it to scrap email adresses from different websites. First, you need to set this project up. Clone a project from repository:

```sh
$ git clone https://github.com/MykhCher/flask-email-scrapy.git email_scraping
$ cd email_scraping
```

After you cloned project and changed work directory to the one, where project is cloned, create a virtual environment and install all dependencies:

```sh
python3 -m venv scrap_env
source scrap_env/bin/activate
pip install -r requirements.txt
```

When all dependencies are installed, you can launch a server and test an app:

```sh
export FLASK_APP=main.py
flask run --debug -p 5000
```

## Functional
After you launched a server, you can visit a [local server](http://127.0.0.1:5000/) and test the app. Enter a url of a site where you want an app to find email and press "Submit". Wait for 20sec: application is searching for all possible adresses. Then you will be provided with JSON-like page of search results. That's all!