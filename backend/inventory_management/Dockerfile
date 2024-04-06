FROM python:3.10.0

WORKDIR /inventory_management

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /inventory_management

EXPOSE 8002

CMD ["python3", "run.py", "--host=0.0.0.0"]
