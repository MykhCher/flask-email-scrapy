# Flask E-Mail Scraping

You are welcome at the page of Flask E-Mail Scraping project. Here I will use [Flask](https://flask.palletsprojects.com/en/2.3.x/) and [Scrapy](https://scrapy.org/) to implement the scrapping of mails from different websites. [Golang](https://go.dev/) is used here as connector to a [Mongo](https://www.mongodb.com/) database 

I also plan to use [Docker](https://www.docker.com/) to make containers for several services. Project is still in development.

## Set up
It is assumed, that you have MongoDB and Golang installed locally. If not, you can install it using the guide from official pages:
For Linux: 
[MongoDB](https://www.mongodb.com/docs/manual/administration/install-on-linux/)
[Golang](https://go.dev/doc/install)
For Windows: 
[MongoDB](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-windows/)
[Golang](https://go.dev/doc/install)

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

After you install all dependencies, launch MongoDB on your machine and start Golang server. It would listen to 8081 port, accept all data from Flask app and write it to MongoDB:

```sh
# Start MongoDB locally
sudo systemctl start mongod

# Launch Golang server
cd db/
sudo go mod init main.com
sudo go mod tidy
sudo go run main.py
```
Use `sudo` to avoid `go: could not create module cache` exception. `run` command will have no output, but the process can be stopped with Ctrl+C combination. If you had no exceptions, Go server is started

When everything is launched, you can launch a server and test an app:

```sh
export FLASK_APP=main.py
flask run --debug -p 5000
```

## Functional
After you launched a server, you can visit a [local server](http://127.0.0.1:5000/) and test the app. Enter a url of a site where you want an app to find email and press "Submit". Wait for 20sec: application is searching for all possible adresses. Then you will be provided with JSON-like page of search results. That's all!