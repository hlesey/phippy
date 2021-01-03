FROM python:buster

WORKDIR /ui
COPY src/ .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=ui

CMD ["python", "-m", "flask", "run", "--host", "0.0.0.0"]
