FROM python:3.10.0

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /orders/app

ENV FLASK_ENV=development

EXPOSE 8080

CMD ["python3", "run.py", "--host=0.0.0.0"]
