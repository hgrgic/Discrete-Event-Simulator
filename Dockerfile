FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7

# Update
#RUN apk add --update add python py-pip
#RUN apk --update add bash nano python

# Bundle app source
COPY ./main/* /main/
COPY ./index.html /index.html
COPY ./requirements.txt /requirements.txt

# Install app dependencies
RUN pip install -r /requirements.txt

#CMD ["python", "/main/WebServerInitializer.py"]