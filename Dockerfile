FROM python:3.9.0b4-alpine3.12
COPY mentorBIreport-healthcheck.py /bin/app.py
COPY crontab /var/spool/cron/crontabs/root
RUN pip3 install requests
RUN chmod +x /bin/app.py
CMD crond -l 2 -f