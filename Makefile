# Makefile

.PHONY: up migrate down

##  Поднять все сервисы (с пересборкой образов) в фоне
up:
	docker compose up --build

##  Накатить миграции внутри запущенного контейнера Django
migrate:
	docker compose exec django python manage.py migrate

##  Остановить и удалить контейнеры
down:
	docker compose down
