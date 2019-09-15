FROM alpine:3.1

# Update
RUN apk add --update python py-pip

# Install app dependencies
#RUN pip install -r ./requirements.txt

# Bundle app source
COPY ./main/* /main/
COPY ./ServerInitializer.py /ServerInitializer.py
COPY ./index.html /index.html


CMD ["python", "ServerInitializer.py"]