IMG = ghcr.io/hlesey/phippy-api
TAG = $$(cat src/__version__.py | cut -d '=' -f2 | sed 's/[", ]//g')

# Build
build:
	docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t $(IMG):$(TAG) .
# Push
push: 
	docker push $(IMG):$(TAG)

# Build and Push
build-and-push:
	docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t $(IMG):$(TAG) --push .