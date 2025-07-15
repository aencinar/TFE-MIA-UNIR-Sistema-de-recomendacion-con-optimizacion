FROM python:3.12.3-slim

RUN apt-get update && \
    apt-get install -y ca-certificates openssl && \
    pip install --no-cache-dir certifi && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /API
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "API.main:app", "--host", "0.0.0.0", "--port", "8080"]
