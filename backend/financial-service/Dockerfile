FROM python:3.10.0

WORKDIR /app

RUN apt-get update && apt-get install -y curl
RUN curl -sL https://github.com/stripe/stripe-cli/releases/download/v1.8.0/stripe_1.8.0_linux_x86_64.tar.gz | tar xz -C /usr/local/bin stripe

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /financial-service/app

ENV FLASK_ENV=development

EXPOSE 8005

CMD ["python3", "run.py", "--host=0.0.0.0"]
