up:
	docker-compose --env-file env up --build -d

down:
	docker-compose down

shell:
	docker exec -ti pipeline bash

up-reset:
	docker-compose down
	docker volume rm -f survivordash_db-data
	docker-compose --env-file env up --build -d
