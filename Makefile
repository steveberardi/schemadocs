example: venv/bin/activate
	./venv/bin/python -m schemadocs.cli build ./example/schema ./example/docs

validate: venv/bin/activate
	./venv/bin/python -m schemadocs.cli validate ./example/schema

venv/bin/activate: requirements.txt
	python -m venv venv
	./venv/bin/pip install -r requirements.txt

clean:
	rm -rf __pycache__
	rm -rf venv

.PHONY: clean example
