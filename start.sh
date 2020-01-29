#!/bin/bash
app="ing.des.test"

docker stop ing.des.test
docker rm ing.des.test
docker rmi ing.des.test

docker build -t ${app} .


docker-compose up -d