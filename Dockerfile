# docker build . -t docker-django-1
# docker run -p 127.0.0.1:8000:8000 docker-django-1

From python:3.6

ENV DOCKERHOME=/home/app

RUN mkdir -p $DOCKERHOME

WORKDIR $DOCKERHOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1 

COPY . $DOCKERHOME

RUN pip install -r requirements.txt

EXPOSE 8000

WORKDIR $DOCKERHOME/myapp

RUN python manage.py migrate

CMD python manage.py runserver 0.0.0.0:8000