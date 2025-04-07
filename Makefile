LINE-PROVIDER=line_provider
export PYTHONPATH := $(PWD):$(PWD)/$(LINE-PROVIDER)

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
test:
	export PYTHONPATH=$(PWD)/$(LINE-PROVIDER); \
	python -m pytest $(LINE-PROVIDER)/tests/ -vv