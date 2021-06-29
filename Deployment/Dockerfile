FROM ravitejamallozala/projects:curr_exc_base
MAINTAINER "Raviteja Mallozala" <m.raviteja1110@gmail.com>
WORKDIR /opt/app
COPY Deployment/curr_excha.conf /etc/nginx/sites-enabled/
COPY Deployment/supervisord.conf /etc/supervisor/supervisord.conf
ADD  requirements.txt  /opt/
RUN pip install -r /opt/requirements.txt
COPY Deployment/wsgi.ini /opt/wsgi.ini
#COPY crontab.txt /opt/crontab.txt
#RUN  crontab /opt/crontab.txt
ADD  ./  /opt/app
WORKDIR /opt/app
RUN python manage.py collectstatic --no-input
RUN python manage.py migrate
RUN chown www-data:www-data  -R /opt
EXPOSE 80
CMD ["/usr/bin/python2.7" , "/usr/bin/supervisord"]
