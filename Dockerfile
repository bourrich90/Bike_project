FROM ubuntu:latest

ADD files/requirements.txt files/apibike.py files/Bikes.py files/decisiontreemodel.pkl files/randomforestModel.pkl files/ridgeModel.pkl files/lineareModel.pkl ./

RUN  set -xe\
&& apt-get update -y && apt-get install -y  python3-pip  && python3 -m pip  install  --upgrade pip && python3 -m  pip install -r requirements.txt

EXPOSE 8000

CMD uvicorn apibike:app --host 0.0.0.0
