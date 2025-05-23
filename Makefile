setup:
	python3 -m venv .venv
	source .venv/bin/activate && \
	python3 -m pip install --upgrade pip
	pip install -r requirements.txt
	
check:
	ruff format
	ruff check

build:
	podman build -t localhost/gabi-mcp-server:latest .
