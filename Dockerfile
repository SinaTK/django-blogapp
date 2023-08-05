FROM python:latest

LABEL name="Django-Blog"
LABEL version="1.0"

WORKDIR /code

COPY requirments.txt /code/

RUN pip install -U pip
RUN pip install -r requirments.txt

COPY . /code/



CMD ["gunicorn", "blogapp.wsgi", "8003"]
