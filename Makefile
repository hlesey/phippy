
REGISTRY=ghcr.io/hlesey
REPO_NAME=phippy
VERSION=$$(cat app/__version__.py | cut -d '=' -f2 | tr -d '"')

build:
	docker build -t ${REGISTRY}/${REPO_NAME}:${VERSION} .

push: 
	docker push ${REGISTRY}/${REPO_NAME}:${VERSION}

run:
	docker-compose up

dev_setup:
	[ -d venv ] || mkdir venv
	[ -f venv/bin/activate ] || python3 -m venv venv
	./venv/bin/pip install -r requirements.txt
