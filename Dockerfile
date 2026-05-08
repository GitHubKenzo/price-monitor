FROM python:3.10-slim

WORKDIR /app

COPY scraper/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY scraper/ ./scraper/
COPY data/ ./data/

ENV TZ=Asia/Tokyo

CMD ["python", "scraper/main.py"]
