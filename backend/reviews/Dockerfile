FROM python:3.10.0

WORKDIR /reviews

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /reviews

EXPOSE 8003

CMD ["python3", "run.py", "--host=0.0.0.0"]