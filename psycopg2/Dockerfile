FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev && \
    pip3 install --upgrade pip

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 8085

ENTRYPOINT ["python3"]

CMD ["application.py"]