FROM python:3.12-slim

ENV DOCKER=1

WORKDIR "/app"

COPY ConfigurationFile.py .
COPY AlbumList.py .
COPY BlueSky.py .
COPY app.py .
COPY requirements.txt .
COPY google-api.json .

RUN pip install -r requirements.txt

CMD ["python", "-u", "app.py"]