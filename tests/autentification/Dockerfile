FROM python:3
RUN apt-get update && apt-get install python3-pip -y  && pip3 install requests && pip3 install pybase64  && pip3 install jsonlib-python3
ADD autentification.py /my_server/autentification.py
WORKDIR /my_server/
ENV LOG  1
CMD python3 autentification.py