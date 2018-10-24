FROM python:3.7-alpine

RUN mkdir /code
WORKDIR /code
COPY requirements.txt ./

RUN apk add --no-cache nginx supervisor libpq \
    && apk add --no-cache --virtual=.build-deps build-base postgresql-dev libffi-dev \
    && pip install -r requirements.txt \
    && pip install gunicorn \
    && apk del .build-deps
RUN rm /etc/nginx/conf.d/default.conf \
    && echo "daemon off;" >> /etc/nginx/nginx.conf

COPY . ./

RUN DATABASE_URL=none SECRET_KEY=xxx python manage.py collectstatic --noinput

COPY conf/supervisor.conf /etc/supervisor/conf.d/supervisor.conf
COPY conf/nginx.conf /etc/nginx/conf.d/openlobby-server.conf
COPY conf/entrypoint.sh ./

EXPOSE 8010

ENTRYPOINT ["./entrypoint.sh"]
