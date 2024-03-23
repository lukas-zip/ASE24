FROM python:3.10.0

WORKDIR /user-service

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /user-service

EXPOSE 8001

CMD ["python3", "run.py", "--host=0.0.0.0"]
