FROM ubuntu:16.04
MAINTAINER Sergi Blanco-Cuaresma <marblestation@users.noreply.github.com>
USER root


RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
                                                build-essential \
                                                python \
                                                python-dev \
                                                python-distribute \
                                                python-pip
COPY ./Service/ /app
RUN pip install -r /app/requirements.txt

EXPOSE 5000
WORKDIR /app
CMD python app.py
