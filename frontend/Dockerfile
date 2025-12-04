# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/


FROM node:24-alpine 

WORKDIR /app
COPY app/package*.json /.
RUN npm install

COPY /app .
EXPOSE 3000
CMD ["npm", "run", "dev"]