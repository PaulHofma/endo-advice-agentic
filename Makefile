.PHONY: up down db backend frontend

up: db
	@make -j2 backend frontend

down:
	docker-compose down

db:
	docker-compose up -d
	@echo "Waiting for Postgres..."
	@until docker exec endo-advice-db pg_isready -U endo -d endo_advice -q 2>/dev/null; do sleep 1; done
	@echo "Postgres is ready."

backend:
	cd backend && ./gradlew bootRun

frontend:
	cd frontend && npm run dev
