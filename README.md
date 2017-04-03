# Canna

## Getting set up

* Clone and CD in: `git clone git@github.com:Yeungdb/Canna.git && cd Canna`
* Install deps: `pip install Flask Flask-Login psycopg2`
* Set environment variable: `export CANNAKEY = 'YOURKEY'`
* Create DB and set up structure: `createdb Canna && psql -h localhost -d Canna -a -q -f PATH_TO_REPO/Canna.sql`
* Start it up: `python DispensaryPage.py`
