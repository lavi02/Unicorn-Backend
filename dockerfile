FROM python:3.8

RUN mkdir /app
WORKDIR /app
COPY ./main.py /app
COPY ./requirements.txt /app
COPY ./src /app

RUN pip install -r requirements.txt
EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80" "--workers" "4"]