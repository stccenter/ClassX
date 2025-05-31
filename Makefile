up:
	docker compose  up -d

down:
	docker compose  down

reset:
	docker compose  down  && docker compose up -d

build:
	docker compose build
