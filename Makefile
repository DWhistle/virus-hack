.PHONY: venv install run test docker
venv:
	python3 -m venv .venv
install:
	python -m pip install -r requirements.txt
run:
	python main.py
test:
	python -m unittest discover -s tests -p 'test_*.py' -v
docker:
	docker build -t virus-hack:dev .
