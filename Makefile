install:
		pip install --upgrade pip &&\
			pip install -r requirements.txt

test:
		#python3 -m pytest -vv --cov=main --cov=greeting tests

format:
		black *.py packages/coingecko/*.py

lint:
		pylint --disable=R,C main.py
venv:
		python3 -m venv ~/.venv | echo "Activate virtual env with 'source ~/.venv/bin/activate'"

credentials:
		./scripts/create_credentials.sh

run:
		./scripts/create_credentials.sh | echo "Fill empty fields in './scripts/create_credentials.sh'" | ./scripts/run.sh

all: install format lint test