# FROM python:3.7
FROM smarkelov/flask

# COPY ./requirements.txt /code/

WORKDIR /code/

# RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /code/app
COPY ./webapp.py /code/
