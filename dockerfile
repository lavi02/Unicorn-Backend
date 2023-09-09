FROM python:3.8 as builder

# Setup working directory
WORKDIR /app
COPY . .

# Build
EXPOSE 8000
RUN pip3 install -r requirements.txt