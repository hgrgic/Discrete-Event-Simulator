#!/bin/bash
app="ing.des.test"

docker stop docker.test.hg
docker rm docker.test.hg
docker rmi docker.test.hg

docker build -t ${app} .

docker-compose up -d ing.des.test

#https://www.digitalocean.com/community/tutorials/how-to-build-and-deploy-a-flask-application-using-docker-on-ubuntu-18-04#step-4-—-updating-the-application