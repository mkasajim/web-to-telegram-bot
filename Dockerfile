FROM debian:latest


RUN apt update && apt upgrade -y

RUN apt install git curl python3-pip ffmpeg -y

RUN pip3 install -U pip

RUN cd /

RUN git clone https://github.com/mkasajim/web-to-telegram-bot

RUN cd web-to-telegram-bot

WORKDIR /web-to-telegram-bot

RUN pip3 install beautifulsoup4 lxml requests schedule

CMD python3 website-change-tg.py
