pip install flask, python-dotenv

pip freeze > requirements.txt

environment: 
- FLASK_APP=microblog.py
- FLASK_ENV='development'
- FLASK_DEBUG=1

docker exec -it webapp_flask_1 bash

Build new docker image:
docker build -f ./Base_docker/Dockerfile .
then tag it
docker tag <docker images> smarkelov/flask
then push
docker push smarkelov/flask
