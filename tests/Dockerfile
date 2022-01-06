FROM ubuntu:latest

COPY tests_dc.py /fichiers/
WORKDIR fichiers
RUN apt-get update && apt-get install python3-pip -y && pip3 install requests
CMD python3 /fichiers/tests_dc.py >> /fichiers/monvol/resultats.log
