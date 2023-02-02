# Fly.io

## Prerequisites

Install `flyctl`:

```bash
curl -L https://fly.io/install.sh | sh
```

## Create PostGIS

- <https://community.fly.io/t/deploying-postgis/3530>
- <https://fly.io/docs/reference/postgres-on-nomad/>

```bash
flyctl postgres create 
# follow the instructions, use name optimap-db, region Frankfurt

flyctl image show --app optimap-db
```

Note the username, password, connection string etc. in a secure place and manually set `DATABASE_URL` for the other app.
Note that you need to change connection type to `postgis`, i.e., start with `postgis://`.

Create database and enable PostGIS

```bash
flyctl postgres connect -a optimap-db

# in postgres=# 
CREATE DATABASE optimap;
```

## Deploy app via Dockerfile

Use Dockerfile instead of [Django on Fly](https://fly.io/docs/django/) because of GIS dependencies.

- <https://fly.io/docs/languages-and-frameworks/dockerfile/>

```bash
fly launch --dockerfile Dockerfile
# on first run, overwrite Dockerfile and then roll back needed changes, otherwise error
```

Now say YES when asked if you want to create a Postgres DB.

> We recommend using the database_url (`pip install dj-database-url`) to parse the DATABASE_URL from os.environ['DATABASE_URL']
>
> For detailed documentation, see <https://fly.dev/docs/django/>

Why not - changed configuration style to use `dj-database-uri`.

THIS DOES STILL NOT WORK because the database connection is not available when the migrations are run.

Cannot set database connection because the app does not exist at this point...

Trying:

```bash
flyctl launch --dockerfile Dockerfile -e DATABASE_URL=postgis://...:5432/optimap?sslmode=disable
```

Does not work.

Trying to put the `DATABASE_URL` without encryption into `fly.toml` at least for the first start...

Seems to work, <https://optimap.fly.dev/> shows the app!

Now removing the env from the `fly.toml` file and adding the secret:

```bash
flyctl secrets set DATABASE_URL=postgis://postgres:z...@optimap-db.internal:5432?sslmode=disable

flyctl secrets list
```

## Get IPs and certificate

- <https://fly.io/docs/flyctl/ips/#usage>
- <https://fly.io/docs/app-guides/custom-domains-with-fly/>

```bash
fly ips allocate-v4
fly ips allocate-v6
```

```bash
$ fly ips list

VERSION IP                      TYPE    REGION  CREATED AT 
v4      37.16.20.137            public  global  36m11s ago
v6      2a09:8280:1::a:acfd     public  global  36m4s ago
```

Configure `A` and `AAAA` records at domain provider. Then continue with

```bash
flyctl certs create optimap.science
flyctl certs create www.optimap.science
```

Check IP config:

```bash
traceroute optimap.fly.dev
traceroute optimap.science
```

Looks good!

## Secrets and passwords

Check that `SECRET_KEY` environment variable is set, otherwise set it to something... secret:

```bash
flyctl secrets list
flyctl secrets set SECRET_KEY="..."
```

Configure **login email** password (other values are set in `fly.toml`):

```bash
flyctl secrets set OPTIMAP_EMAIL_HOST_PASSWORD="..."
```

Configure the **superusers' email** (users registering with this emailaddress will become Django superusers):

```bash
flyctl secrets set OPTIMAP_SUPERUSER_EMAILS="..."
```

## Deploy

```bash
flyctl deploy
```

<https://optimap.fly.dev/>

and

<https://optimap.science/>

## Update allowed hosts and configure CSRF

- <https://learndjango.com/tutorials/deploy-django-postgresql-flyio>
- See <https://github.com/ifgi/optimetaPortal/issues/42> for links and issue description around CSRF

Add to `tly.toml`:

```toml
  CSRF_TRUSTED_ORIGINS = "https://optimap.science"
```

Then `flyctl deploy`.

## Connect to database

```bash
fly proxy 15432:5432 -a optimap-db
```

Connect to database locally at port `15432`, e.g., with pgAdmin.

## Future

- Database backups, see <https://www.joseferben.com/posts/django-on-flyio/>
- Health check endpoint, see <https://www.joseferben.com/posts/django-on-flyio/>
