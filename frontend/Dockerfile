FROM node:17-alpine
WORKDIR /app
COPY package*.json /app
COPY . /api
CMD ['uvicord','main:app', '--host','0.0.0.0','--port','8000']