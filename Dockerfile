FROM ubuntu:latest

ADD api.py loadings.py requirements.txt cv_lr.pickle cv_rf.pickle cv_svc.pickle rf.pickle svc.pickle lr.pickle /fichiers/
WORKDIR fichiers
RUN apt-get update && apt-get install python3-pip -y && pip3 install -r requirements.txt
EXPOSE 8000
CMD uvicorn api:api --host '0.0.0.0' --port 8000
