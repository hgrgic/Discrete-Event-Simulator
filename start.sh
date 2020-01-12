#!/bin/bash
app="ing.des.test"

docker stop ing.des.test
docker rm ing.des.test
docker rmi ing.des.test

docker build -t ${app} .

docker-compose up -d ing.des.test

#https://www.digitalocean.com/community/tutorials/how-to-build-and-deploy-a-flask-application-using-docker-on-ubuntu-18-04#step-4-—-updating-the-application