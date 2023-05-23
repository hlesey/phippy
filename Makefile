
# CI

test:
	@echo "Running phippy tests..."
	pytest --maxfail=1 -vv api/tests

lint: ## Lint python code
	@echo "Linting python code..."
	flake8 --ignore=E501,W503,F541,E203 api/src/ ui/src/
	black --line-length 120 --check api/src/ ui/src/
	isort -c api/src/ ui/src/

format: ## Format python code
	@echo "Fixing imports..."
	@isort --line-length 132 --profile "black" .
	@echo "Fixing format..."
	@black --line-length 132 .

security: ## Check python code for security issues
	@echo "Check python code for security issues..."
	bandit -ll -r api/src/ ui/src/

# Development

dev.run:
	docker-compose up

dev.fix-code-style:
	isort api/src/ ui/src/
	black --line-length 120 api/src/ ui/src/

dev.setup:
	[ -d venv ] || mkdir venv
	[ -f venv/bin/activate ] || python3 -m venv venv
	./venv/bin/pip install -r requirements.txt -r api/requirements.txt -r ui/requirements.txt

dev.clean:
	[ ! -d venv ] || rm -rf venv
	rm -rf 
