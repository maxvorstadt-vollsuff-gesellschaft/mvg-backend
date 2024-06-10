IMAGE_NAME=ghcr.io/linuseing/edited-rs-backend:latest

build:
	docker buildx build --platform linux/amd64,linux/arm64 -t $(IMAGE_NAME) . --push
