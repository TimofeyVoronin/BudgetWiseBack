# Makefile

.PHONY: start migrate wait-db

# 1) Собрать и запустить все сервисы в фоне, дождаться готовности БД, затем выполнить миграции
start: 
	docker compose up --build -d

	@echo "⏳ Ждём, пока Postgres станет доступен…"
	# вариант 1: через pg_isready (на контейнере db в стандартном постгрес-образе)
	until docker compose exec db pg_isready -U $$POSTGRES_USER >/dev/null 2>&1; do \
		printf "."; \
		sleep 1; \
	done; \
	echo " OK!"

	@echo "🧩 Накатываем миграции"
	docker compose exec django python manage.py migrate

# 2) Если сервисы уже подняты и нужно только миграции
migrate:
	docker compose exec django python manage.py migrate
