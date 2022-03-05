
IMG = ghcr.io/hlesey/phippy-ui
TAG = $$(cat src/__version__.py | cut -d '=' -f2 | sed 's/[", ]//g')


# Build

build:
	docker build -t $(IMG):$(TAG) .

push: 
	docker push $(IMG):$(TAG)
