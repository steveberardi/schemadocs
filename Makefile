example: venv/bin/activate
	./venv/bin/python schemadocs/main.py build ./example/schema ./example/docs

venv/bin/activate: requirements.txt
	python -m venv venv
	./venv/bin/pip install -r requirements.txt

clean:
	rm -rf __pycache__
	rm -rf venv

.PHONY: clean example
