FROM 324257953347.dkr.ecr.us-east-1.amazonaws.com/sdc-alpine:3.13
RUN apk add --no-cache python3-dev py3-pip build-base \
    && pip3 install --upgrade pip
WORKDIR /app
COPY . /app
RUN pip3 --no-cache-dir install -r requirements.txt
EXPOSE 30001
ENTRYPOINT  ["python3"]
CMD ["application.py"]

# FROM ubuntu:14.04

# RUN apt-get update -y

# RUN apt-get install -y python-setuptools

# RUN easy_install pip

# ADD requirements.txt /src/requirements.txt
# RUN cd /src; pip install -r requirements.txt

# ADD . /src

# EXPOSE  30001

# CMD ["python", "/src/application.py"]