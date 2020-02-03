#!/bin/bash
app="des"

docker stop des
docker rm des
docker rmi des

docker build -t ${app} .


docker-compose up -d