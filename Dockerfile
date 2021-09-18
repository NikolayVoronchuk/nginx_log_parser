FROM ubuntu

RUN apt-get update
RUN apt-get install -y python3
WORKDIR /log-parser
COPY . .
USER root
RUN mkdir /var/log/chunkfred/
RUN chmod -R 777 /var/log/chunkfred/

ENTRYPOINT ["python3", "/log-parser/main.py"]



