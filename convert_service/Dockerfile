FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y ffmpeg

COPY . .

CMD ["python", "worker.py"]