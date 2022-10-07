# For more information, please refer to https://aka.ms/vscode-docker-python
FROM ubuntu:20.04

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# install Python 3 and PIP
RUN apt-get update && \
    apt-get install -y -qq software-properties-common && \
    apt-get install -y -qq python-is-python3 && \
    apt-get install -y -qq python3-pip

# install GDAL from UbuntuGIS
RUN apt-get update && \
    add-apt-repository ppa:ubuntugis/ppa && \
    apt-get install -y -qq gdal-bin libgdal-dev python3-gdal

# install app dependencies
WORKDIR /tmp
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

# mount files at runtime!
WORKDIR /optimetaPortal

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000" ]
# TODO switch to gunicorn for production
