FROM python:3.10-slim

RUN apt update && apt install -y sqlite3

WORKDIR /workspace

ENV PYTHONPATH=/workspace
RUN mkdir -p /workspace/data
