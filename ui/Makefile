
IMG = ghcr.io/hlesey/phippy-ui
TAG = $$(cat src/__version__.py | cut -d '=' -f2 | sed 's/[", ]//g')

build: lint
	docker build -t $(IMG):$(TAG) .

push: 
	docker push $(IMG):$(TAG)

lint:
	flake8 --ignore=E501,W503 src/

dev_setup:
	[ -d venv ] || mkdir venv
	[ -f venv/bin/activate ] || python3 -m venv venv
	./venv/bin/pip install -r requirements.txt
