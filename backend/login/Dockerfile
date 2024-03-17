FROM python:3.10
WORKDIR /api
COPY ./requirements.txt /api/requirements.txt
COPY . /api
CMD ['uvicord','main:app', '--host','0.0.0.0','--port','8000']