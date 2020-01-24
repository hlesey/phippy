FROM python:3.7-alpine

LABEL \
  app="docker-cursantX" \
  layer="frontend" \
  git-url="https://github.com/hlesey/phippy.git"

WORKDIR /app
COPY app/ .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=app

CMD ["python", "-m", "flask", "run", "--host", "0.0.0.0"]
