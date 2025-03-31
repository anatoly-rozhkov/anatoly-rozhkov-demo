poetry-python:
	source $(poetry env info --path)/bin/activate
start:
	docker compose up
stop:
	docker compose down
image-clean:
	docker image rm line_provider_app
inside-line:
	docker exec -it line_provider_app /bin/sh
format:
	black --config black.toml .
	isort .