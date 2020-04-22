NAME=youtubereloadservice\:v2
ENVDIR=venv
WARN_COLOR=\x1b[35;01m
NO_COLOR=\x1b[0m
VIDEOS_DIR=videos
PROGRAM_NAME="main.py"

all: install run
run:
	-@mkdir -p $(VIDEOS_DIR)
	python $(PROGRAM_NAME)
clean:
	find . -name '*.pyc' -exec rm -f {} \;

fclean: clean
	rm -rf $(VIDEOS_DIR)
	rm -rf creds/credentials.pickle

venv:
	python3 -m venv venv --clear
	@echo "Для перехода в виртуальное окружение введите $(WARN_COLOR)\"source venv/bin/activate\"$(NO_COLOR)"

install:
	pip install --upgrade pip > /dev/null
	pip install --upgrade cython > /dev/null
	pip install -r requirements.txt > /dev/null

docker:
	docker build -t $(NAME) .
	docker run --env SERVER_MODE=DEV $(NAME)

docker-rm:
	docker image rm -f $(NAME)

.PHONY: venv clean-all install