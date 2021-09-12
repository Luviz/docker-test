FROM node:14-alpine
WORKDIR /app

COPY ./package.json .

RUN npm install

ENV port=80
ENV server=0.0.0.0

EXPOSE 80

COPY . .

CMD [ "npm", "start" ]