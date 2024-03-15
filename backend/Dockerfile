FROM python:3.10.0

WORKDIR /app

COPY ./requirements.txt .

RUN pip3 install boto3

RUN pip3 install flask

RUN pip3 install localstack

RUN pip3 install uuid

RUN pip3 install flask-cors

ENV FLASK_RUN_HOST=0.0.0.0

CMD ["python3", "myfirstflask.py"]