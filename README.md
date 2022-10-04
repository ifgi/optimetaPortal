e[![OPTIMETA Logo](https://projects.tib.eu/fileadmin/_processed_/e/8/csm_Optimeta_Logo_web_98c26141b1.png)](https://projects.tib.eu/optimeta/en/)

# OPTIMETA Portal

Geospatial discovery of research articles based on open metadata.
The OPTIMETA Portal is part of the OPTIMETA project (<https://projects.tib.eu/optimeta>) and relies on the spatial and temporal metadata collected for scientific papers with the OPTIMETA Geo Plugin for Open Journal Systems ([OJS](https://pkp.sfu.ca/ojs/)) published at <https://github.com/TIBHannover/optimetaGeo>.

## Run with Docker

```bash
docker-compose up
```

Now open a browser at <http://127.0.0.1:8000/publications/map/> for the map and <http://127.0.0.1:8000/publications/api/> for the API.

## Development

### Run locally

Create a `.env` file based on `.env.example` in the same directory where `settings.py` resides and fill in the configuration settings as needed.

```bash
# once onle: create virtual environment
# mkvirtualenv optimetaPortal
workon optimetaPortal

pip install -r requirements.txt

# create and start local DB (once)
docker run --name optimetaPortalDB -p 5432:5432 -e POSTGRES_USER=optimeta -e POSTGRES_PASSWORD=optimeta -e POSTGRES_DB=optimetaPortal -d postgis/postgis:14-3.3
# stop and restart it with
# docker stop optimetaPortalDB
# docker start optimetaPortalDB

# run migrations
python manage.py makemigrations
python manage.py migrate

# start app
python manage.py runserver
```

Now open a browser at <http://127.0.0.1:8000/publications/map/> for the map and <http://127.0.0.1:8000/publications/api/> for the API.

### Debug with VS Code

Select the Python interpreter created above (`optimetaPortal` environment), see instructions at <https://code.visualstudio.com/docs/python/tutorial-django>.

Configuration for debugging with VS Code:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Django Run",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/manage.py",
            "args": [
                "runserver"
            ],
            "django": true,
            "justMyCode": true
        }
    ]
}
```

### Debug email sending

Add `EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend` to the `.env` file to have emails printed to the console instead of sent via SMTP.

### Run tests

See <https://docs.djangoproject.com/en/4.1/topics/testing/overview/> for testing Django apps.

UI tests are based on [Helium](https://github.com/mherrmann/selenium-python-helium) (because [Pylenium](https://github.com/ElSnoMan/pyleniumio) would need pytest in addition).

```bash
pip install -r requirements-dev.txt
```

```bash
python manage.py test tests

# show deprecation warnings
python -Wa manage.py test

# running UI tests needs either compose configuration or a manage.py runserver in a seperate shell
docker-compose up
# TODO insert test data
python -Wa manage.py test tests-ui
```

### Develop tests

For developing the UI tests, you can remove the `headless=True` in the statements for starting the browsers so you can "watch along" and inspect the HTML when a breakpoint is hit as the tests are executed.

### Debug tests with VS Code

A configuration to debug the test code and also print deprecation warnings:

```json
{
    "name": "Python: Django Test",
    "type": "python",
    "request": "launch",
    "pythonArgs": [
        "-Wa"
    ],
    "program": "${workspaceFolder}/manage.py",
    "args": [
        "test",
        "tests"
    ],
    "django": true,
    "justMyCode": true
}
```

Change the argument `tests` to `tests-ui` to run the UI tests.

See also documentation at <https://code.visualstudio.com/docs/python/tutorial-django>.

## License

This software is published under the GNU General Public License v3.0 (see file `LICENSE`).
