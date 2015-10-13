.PHONY: update \
		dependencies backend-dependencies frontend-dependencies \
		test test-backend test-frontend \
		check check-backend check-frontend \
		db-setup db-migrate db-load-data admin

# -----------------------------------------------------------

update: dependencies db-setup

# -----------------------------------------------------------

dependencies: backend-dependencies frontend-dependencies

backend-dependencies:
	@echo "== Install Python dependencies. =="
	pip install -r requirements.txt --quiet

frontend-dependencies:
	@echo "== Install frontend dependencies. =="
	cd frontend && \
	  npm update && \
	  bower update && \
	  grunt development-build

# -----------------------------------------------------------

test: test-backend test-frontend

test-backend:
	@echo "===== Backend tests ====="
	python manage.py test --traceback

test-frontend:
	@echo "===== Frontend tests ====="
	@echo "(Coming soon...)"

# -----------------------------------------------------------

check: check-backend check-frontend

check-backend:
	@echo "===== Backend linting ====="
	pylint --reports=n --disable=E501,E225,E123,E128 --ignore=migrations,urls.py,wsgi.py practice

check-frontend:
	@echo "===== Frontend linting ====="
	cd frontend && \
	  grunt lint


# -----------------------------------------------------------

db-setup: db-migrate db-load-data

db-migrate:
	@echo "===== Set up database ====="
	python manage.py migrate --noinput

db-load-data:
	python manage.py flush --noinput
	python manage.py create_admin
	python manage.py loaddata practice/fixtures/tasks.xml

admin:
	python manage.py create_admin
