# Dockerfile

FROM python:3.8

RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

COPY . /app
EXPOSE 80

CMD ["uvicorn", "main:app", "--port", "80", "--workers", "2"]
