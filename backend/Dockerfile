FROM python:3.10.0

WORKDIR /app

COPY ./requirements.txt .

RUN pip3 install boto3

RUN pip3 install flask

RUN pip3 install logging

RUN pip3 install json

RUN pip3 install localstack

#RUN pip3 install -r requirements.txt

#COPY . .

CMD ["python3", "myfirstflask.py"]