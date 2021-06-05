FROM python:3.7

ENV PYTHONUNBUFFERED 1

WORKDIR /app

#RUN mkdir -p /opt/app/my_project

ADD . /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -U pip

RUN pip install -r requirements.txt

RUN chown -R www-data:www-data /app

COPY . /app
