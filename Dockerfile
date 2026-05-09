FROM python:3.10-slim

WORKDIR /app

COPY scraper/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./scraper /app/scraper
COPY ./db /app/db

COPY utils.py /app/utils.py
COPY products.json /app/products.json
COPY main.py /app/main.py

CMD ["python", "main.py"]
