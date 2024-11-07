IMAGE_NAME=ghcr.io/linuseing/edited-rs-backend:latest

build:
	docker buildx build --platform linux/amd64,linux/arm64 -t $(IMAGE_NAME) . --push

run-dev:
	. .env
	docker compose up -d
	poetry run uvicorn src.main:app --reload

ts-client:
	rm -rf ts-client
	rm -f openapi.yaml
	rm -f openapi.json
	poetry run python tools/generate_spec.py
	openapi-generator-cli generate -i openapi.yaml -g typescript-axios -o ts-client -c openapi-config.json
