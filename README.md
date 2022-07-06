[![OPTIMETA Logo](https://projects.tib.eu/fileadmin/_processed_/e/8/csm_Optimeta_Logo_web_98c26141b1.png)](https://projects.tib.eu/optimeta/en/)

# OPTIMETA Portal

Geospatial discovery of research articles based on open metadata

## Run with Docker

```bash
docker-compose up
```

Now open browser at <http://127.0.0.1:8000/publications/map/> for the map and <http://127.0.0.1:8000/publications/api/> for the API.

## Development version

```bash
# once onle: create virtual environment
# mkvirtualenv optimetaPortal
workon optimetaPortal

pip install -r requirements.txt

# create and start local DB
docker run --name optimetaPortalDB -p 5432:5432 -e POSTGRES_USER=optimeta -e POSTGRES_PASSWORD=optimeta -e POSTGRES_DB=optimetaPortal -d postgres:14
# stop and restart it with
# docker stop optimetaPortalDB
# docker start optimetaPortalDB

# run migrations
python manage.py makemigrations
#python manage.py migrate

# start app
python manage.py runserver
```

Now open browser at <http://127.0.0.1:8000/publications/map/> for the map and <http://127.0.0.1:8000/publications/api/> for the API.


## Tests



## License

