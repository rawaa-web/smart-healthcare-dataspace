# S2: Flower client — ONE image, run three times as hospitals A, B, C.
# Built from the REPO ROOT so it can copy the shared ml/ package:
#   docker build -f services/fl-client/Dockerfile -t fl-client:dev .
# The hospital CSV is mounted read-only at /data/data.csv at runtime.
FROM python:3.11-slim

WORKDIR /app

COPY services/fl-client/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ml/ ml/
COPY services/fl-client/client.py .

ENV HOSPITAL_ID=a \
    SERVER_ADDRESS=flower-server:8080 \
    DATA_PATH=/data/data.csv

CMD ["python", "client.py"]
