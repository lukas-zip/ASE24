FROM node:14-alpine

WORKDIR /app

COPY . .

RUN npm install

RUN npm install axios

RUN npm run build

EXPOSE 3000

# Serve the app
CMD ["npm", "start"]
