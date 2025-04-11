# Dockerfile
FROM mcr.microsoft.com/playwright/python:v1.51.0-noble

WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Optional: playwright install here to pre-bundle
RUN playwright install

CMD ["python3", "nutbot.py"]