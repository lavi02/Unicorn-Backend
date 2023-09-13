FROM python:3.8 as builder

# Setup working directory
WORKDIR /app
COPY . .

# Build
RUN pip3 install -r requirements.txt