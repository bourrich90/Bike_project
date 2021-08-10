FROM python:3
ADD prediction.py requirements.txt ./
RUN  set -xe\
&& apt-get update -y && apt-get install -y  python3-pip  && python3 -m pip  install  --upgrade pip && python3 -m  pip install -r requirements.txt
WORKDIR ./
ENV LOG  1
CMD python3 prediction.py
