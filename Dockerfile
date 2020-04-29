FROM python:3.7

COPY ./requirements.txt /code/

WORKDIR /code/

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /code/app
COPY ./microblog.py /code/
