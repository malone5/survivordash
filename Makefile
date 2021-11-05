up:
	docker-compose --env-file env up --build -d

down:
	docker-compose down

shell:
	docker exec -ti pipeline bash