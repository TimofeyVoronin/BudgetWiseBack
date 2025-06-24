FROM python:3.12
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt
RUN apt-get update && apt-get install -y netcat