FROM python:3.5
MAINTAINER Abriko <abriko@live.ie>

RUN git clone https://github.com/lukas2511/dehydrated /app/dehydrated
WORKDIR /app/dehydrated
RUN mkdir hooks
COPY hook.py hooks/alidns/hook.py
COPY requirements.txt hooks/alidns/requirements.txt
COPY app.sh app.sh

RUN pip install -r hooks/alidns/requirements.txt
RUN chmod 755 dehydrated
RUN chmod 755 hooks/alidns/hook.py
RUN chmod 755 app.sh

WORKDIR /app/letsencrypt.sh
ENTRYPOINT ["/app/dehydrated/app.sh"]
CMD ["-h"]