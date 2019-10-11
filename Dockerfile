FROM python:3.6-alpine
ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache bash su-exec libpq
RUN addgroup -S web -g 666 && adduser -S -G web -u 666 web

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev

RUN mkdir -p /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt
RUN apk del --no-cache .build-deps

COPY cms /app/cms
RUN chown -R web:web /app
WORKDIR /app/cms

EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["runserver"]