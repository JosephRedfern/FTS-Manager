FROM python:3.6.3-jessie

WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install -y libsasl2-dev libldap2-dev libssl-dev nginx supervisor cron

COPY requirements.txt ./
COPY docker/fts-manager.conf /etc/nginx/sites-available/default
COPY docker/supervisor.conf /etc/supervisor/conf.d/
COPY docker/uwsgi.ini ./
COPY docker/uwsgi_params ./
COPY FTSManager/ ./FTSManager

RUN echo "daemon off;" >> /etc/nginx/nginx.conf 
RUN ln -s /etc/nginx/sites-available/fts-manager.conf /etc/nginx/sites-enabled/fts-manager.conf 

RUN pip install --no-cache-dir -r requirements.txt

RUN python FTSManager/manage.py collectstatic
RUN python FTSManager/manage.py installtasks

EXPOSE 80

CMD [ "supervisord", "-n", "-c", "/etc/supervisor/conf.d/supervisor.conf"]
