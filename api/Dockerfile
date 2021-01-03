FROM python:buster

WORKDIR /api
COPY src/ .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=api

CMD ["python", "-m", "flask", "run", "--host", "0.0.0.0"]
