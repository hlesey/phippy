FROM python:3.6-alpine3.7

LABEL \
  app="docker-cursantX" \
  layer="frontend" \
  git-url="https://github.com/victorvarza/phippy.git"

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80
CMD [ "python", "phippy.py" ]
