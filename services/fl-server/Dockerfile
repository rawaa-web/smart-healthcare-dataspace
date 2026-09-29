# S2: Flower FedAvg server. Aggregation works on NumPy arrays — no torch here.
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .

ENV SERVER_ADDRESS=0.0.0.0:8080 \
    NUM_ROUNDS=5 \
    API_URL=http://api:8000

EXPOSE 8080
CMD ["python", "server.py"]
