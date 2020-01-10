FROM tiangolo/uwsgi-nginx-flask:python3.7

# Bundle app source
COPY main ./main/
COPY ./index.html /index.html
COPY ./requirements.txt /requirements.txt

# Update
RUN pip install -U pip

# Install app dependencies
RUN pip install -r /requirements.txt
