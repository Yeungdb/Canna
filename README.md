# Canna

## Getting set up

* Clone and CD in: `git clone git@github.com:Yeungdb/Canna.git && cd Canna`
* Install deps: `pip install Flask Flask-Login Flask-Assets pyScss psycopg2 requests urllib3 twilio wit jsmin`
* Create DB and set up structure: `createdb Canna && psql -h localhost -d Canna -a -q -f $PWD/resources/Canna.sql`
* Start it up: `python Spark.py`

You can reset the whole DB using `dropdb Canna && createdb Canna`

## Dev notes

- When any number needs to be an Integer we need to ensure strings can be coerced to int (right now SPACE and + characters cause errors)
- Strings need to be able to handle all Unicode characters (I tried to use – [ndash] character and it raised UnicodeEncodeError)
