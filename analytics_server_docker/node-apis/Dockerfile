FROM node:8

# Create app directory
WORKDIR /home/node

COPY apis.zip .

RUN echo "deb http://archive.debian.org/debian stretch main" > /etc/apt/sources.list

RUN apt-get update && apt-get install unzip

RUN unzip apis.zip && rm apis.zip

RUN npm install
