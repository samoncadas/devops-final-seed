FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

EXPOSE 5000

ENV DB_PATH=/data/tasks.db

CMD ["python", "src/app.py"]
