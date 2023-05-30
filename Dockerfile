# syntax=docker/dockerfile:1
FROM python:3.9-alpine

WORKDIR /var/www/app/
COPY app/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app .
EXPOSE 5000
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]