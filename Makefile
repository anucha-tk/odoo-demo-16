start:
	docker compose up -d
stop:
	docker compose stop
down:
	docker compose down

# restart without clean volumns
restart:
	make stop; 
	make start;
logs:
	docker compose logs -f