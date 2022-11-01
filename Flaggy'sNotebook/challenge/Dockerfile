FROM python:3.8-slim-buster

WORKDIR .

COPY . .

EXPOSE 5000

RUN pip3 install -r requirements.txt

CMD [ "python", "run.py"]
