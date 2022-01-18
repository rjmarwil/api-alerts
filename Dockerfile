FROM python:3.8-slim@sha256:3d3edc52cfae3ed6fb8303559f10184f962a8069194b2dee93baaac66ebedeb5

# Flush output to stdout immediately in order to see python print statements
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY api_alerts.py .

CMD ["python3", "api_alerts.py"]