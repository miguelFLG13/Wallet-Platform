build:
	docker-compose build

up:
	docker-compose up -d

up-non-daemon:
	docker-compose up

start:
	docker-compose start

stop:
	docker-compose stop

restar:
	docker-compose stop && docker-compose start

shell-nginx:
	docker exec -ti nginx bash

shell-web:
	docker exec -ti web bash

log-nginx:
	docker-compose logs nginx

log-web:
	docker-compose logs web

run-tests:
	docker exec web python manage.py test --settings=wallet_platform.settings.test --pattern="*_tests.py"
