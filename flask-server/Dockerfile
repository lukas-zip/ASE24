FROM python:3.11

WORKDIR /flask-server

COPY ./requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "server.py"]

