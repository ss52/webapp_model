pip install flask, python-dotenv

pip freeze > rec.txt

environment: 
- FLASK_APP=microblog.py
- FLASK_ENV='development'
- FLASK_DEBUG=1

docker exec -it webapp_flask_1 bash
