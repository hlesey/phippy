IMG = hlesey/proxy
TAG = 1.0

all: push

build:
	docker build --pull --build-arg IMAGE_ARG=$(IMG):$(TAG) -t $(IMG):$(TAG) .
	docker tag $(IMG):$(TAG) $(IMG):latest

push: build
	docker push $(IMG):$(TAG)
	docker push $(IMG):latest
	@echo Pushed $(IMG) with :latest and :$(TAG) tags

test:
	go test *.go

