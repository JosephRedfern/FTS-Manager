FROM python:3.6.3-jessie

WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install -y libsasl2-dev libldap2-dev libssl-dev nginx supervisor

COPY requirements.txt ./
COPY docker/start.sh /start.sh
COPY docker/fts-manager.conf /etc/nginx/sites-available/default
COPY docker/supervisor.conf /etc/supervisor/conf.d/
COPY docker/uwsgi.ini ./
COPY docker/uwsgi_params ./
COPY FTSManager/ ./FTSManager

RUN echo "daemon off;" >> /etc/nginx/nginx.conf 
RUN ln -s /etc/nginx/sites-available/fts-manager.conf /etc/nginx/sites-enabled/fts-manager.conf 

RUN pip install --no-cache-dir -r requirements.txt

RUN ls FTSManager/
RUN python FTSManager/manage.py collectstatic

EXPOSE 80

CMD [ "supervisord", "-n"]
#CMD ["/usr/local/bin/uwsgi", "--ini", "/usr/src/app/uwsgi.ini"]
