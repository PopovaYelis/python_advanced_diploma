FROM python:3.12-slim

RUN  apt-get update && apt-get install -y python3-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /client

COPY /client/static /client/static

WORKDIR /server

COPY /server/requirements.txt /server/requirements.txt

RUN pip install --no-cache-dir -r /server/requirements.txt

COPY server .


CMD ["sh", "-c", "python init_db.py && exec uvicorn main:app --host 0.0.0.0 --port 8000 --log-level info"]