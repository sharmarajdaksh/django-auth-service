FROM python:3.9.0-buster

WORKDIR /usr/app

RUN apt-get update && apt-get install libpq-dev -y

COPY requirements.txt requirements.txt

RUN python3 -m pip install -r requirements.txt

COPY ./ ./

RUN chmod +x start.sh

CMD ["/bin/bash", "start.sh"]
