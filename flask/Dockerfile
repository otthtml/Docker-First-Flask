FROM alpine:latest

RUN apk add --no-cache python3-dev && \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip3 install --upgrade pip

WORKDIR /app

COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 8085

ENTRYPOINT ["python3"]
CMD ["application.py"]
