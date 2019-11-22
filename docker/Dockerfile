FROM python:3.6-alpine3.7

LABEL \
  app="docker-cursantX" \
  layer="frontend" \
  git-url="https://github.com/hlesey/phippy.git"

ENV ETCD_HOST='etcd'
ENV ETCD_PORT=2379

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80
CMD [ "python", "phippy.py" ]
