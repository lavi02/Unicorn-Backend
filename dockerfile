FROM python:3.8 as builder

# Setup working directory
WORKDIR /app
COPY . .

# Build
EXPOSE 8000
RUN pip3 install -r requirements.txt

CMD ["gunicorn", "main:app", " --workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]