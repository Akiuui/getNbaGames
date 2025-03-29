FROM python:3.9-slim

RUN apt update && apt install -y python3-pip && apt clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

COPY src /app/src
WORKDIR /app/src

ENV PYTHONPATH="/app/src"

EXPOSE 8008

CMD ["waitress-serve", "--host=0.0.0.0", "--port=8008", "app:app"]