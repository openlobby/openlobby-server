FROM python:3.6

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
RUN pip install gunicorn
ADD . /code/

EXPOSE 8010

CMD ["sh", "-c", "make migrate && gunicorn -w 4 -b 0.0.0.0:8010 --access-logfile - --error-logfile - --capture-output openlobby.wsgi"]
