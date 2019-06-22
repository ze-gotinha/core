first-run:
	cd docker && ./build-base.sh
	make train
	docker-compose run --rm telegram_bot make config-rocket
	docker-compose up telegram_bot

train:
	docker build . -f docker/coach.Dockerfile -t botcoach:latest
	docker-compose build telegram_bot

console:
	docker-compose run telegram_bot make run-console