FROM python:3.6

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/

RUN apt-get update && apt-get install -y --no-install-recommends \
        nginx \
        supervisor \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get autoremove -y --purge

COPY ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt && \
    pip install gunicorn && \
    rm /etc/nginx/sites-enabled/default && \
    echo "daemon off;" >> /etc/nginx/nginx.conf

ADD . /code/

RUN DATABASE_URL=none python manage.py collectstatic --noinput

COPY conf/supervisor.conf /etc/supervisor/conf.d/supervisor.conf
COPY conf/nginx.conf /etc/nginx/conf.d/openlobby-server.conf
COPY conf/entrypoint.sh ./

WORKDIR /code

EXPOSE 8010

ENTRYPOINT ["./entrypoint.sh"]
