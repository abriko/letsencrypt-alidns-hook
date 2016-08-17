FROM python:3.5
MAINTAINER Abriko <abriko@live.ie>

RUN git clone https://github.com/lukas2511/letsencrypt.sh /app/letsencrypt.sh
RUN mkdir /app/letsencrypt.sh/hooks
ADD hook.py /app/letsencrypt.sh/hooks/alidns/hook.py
ADD requirements.txt /app/letsencrypt.sh/hooks/alidns/requirements.txt
ADD app.sh /app/letsencrypt.sh/app.sh

RUN pip install -r /app/letsencrypt.sh/hooks/alidns/requirements.txt
RUN chmod 755 /app/letsencrypt.sh/letsencrypt.sh
RUN chmod 755 /app/letsencrypt.sh/hooks/alidns/hook.py
RUN chmod 755 /app/letsencrypt.sh/app.sh

WORKDIR /app/letsencrypt.sh
ENTRYPOINT ["/app/letsencrypt.sh/app.sh"]
CMD ["-h"]