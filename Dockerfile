FROM python:3.7-slim-buster

COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

RUN useradd --create-home user
WORKDIR /home/user
USER user

COPY *.py ./

COPY config.yaml .

COPY ca.crt client.crt client.key ./

CMD ./main.py
