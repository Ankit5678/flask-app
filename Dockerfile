FROM alpine:3.13
RUN apk add --no-cache py3-pip \
    && pip3 install --upgrade pip
WORKDIR /app
COPY . /app
RUN pip3 --no-cache-dir install -r requirements.txt
EXPOSE 30001
ENTRYPOINT  ["python3"]
CMD ["first.py"]