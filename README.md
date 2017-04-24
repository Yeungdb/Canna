# Canna

## Development

### Setup

* You'll need Python and [ngrok](https://ngrok.com/)
* Clone and CD in: `git clone git@github.com:Yeungdb/Canna.git && cd Canna`
* Install deps: `pip install Flask Flask-Login Flask-Assets pyScss psycopg2 requests urllib3 twilio wit jsmin`
* Create DB and set up structure: `createdb Canna && psql -h localhost -d Canna -a -q -f $PWD/resources/Canna.sql`
* Set up environment variables (see below)
* Start up the application: `ngrok http 5000 > /dev/null & python Spark.py`

The application is now available at `http://localhost:5000/`

### Notes

#### Environment variables

This repo includes an `example-env` file. Create your own `.env` file and use the examples to fill it in. You'll need access to our external services to get some values.

#### Ngrok setup

When you start the server using the above command it will create a background `ngrok` process, allowing your localhost to be accesible publicly. This is neccesary for external services to communicate with your application when developing locally. 

Since the address is different every time, the application will print the current ngrok address. Use this address in any external services to communicate with your app.

#### Reset database

You can reset the whole DB using `dropdb Canna && createdb Canna`
