## Makefile
## https://www.gnu.org/software/make/manual/make.html
## man:make

.DEFAULT_GOAL := run
.PHONY: $(MAKECMDGOALS)

virtualenv_dir := ./venv
image_name := chucknorris_webapp

clear:
	rm -rf $(virtualenv_dir) || true
	find . -type d -name __pycache__ -exec rm -rf {} \; || true
	find . -type d -name "*.egg-info" -exec rm -rf {} \; || true
	rm -rf build || true
	rm -rf dist || true

bootstrap-venv:
	#rm -rf $(virtualenv_dir)
	if [ ! -d "$(virtualenv_dir)" ]; then \
		python3 -m virtualenv -ppython3 --no-site-packages $(virtualenv_dir); \
	fi

venv: bootstrap-venv
	@( \
		. $(virtualenv_dir)/bin/activate; \
		python3 -m pip install -e .[tests] ; \
	)

tests: venv
	@( \
		. $(virtualenv_dir)/bin/activate; \
		python3 -m pylint --exit-zero --jobs=0 src/ tests/; \
		python3 -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics; \
		python3 -m flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics; \
		pytest; \
	)

build:
	@( \
		eval $(shell minikube docker-env) ; \
		docker build --pull --tag=$(image_name) . ; \
		docker build --pull --tag=$(image_name)-nginx nginx/ ; \
		eval $(shell minikube docker-env -u) ; \
	)

terraform: build
	@( \
		cd terraform ; \
		terraform init ; \
		terraform validate ; \
		terraform apply -lock-timeout=30s -auto-approve -var "image_name=$(image_name)" -var "gunicorn_log_level=debug"; \
	)

terraform-destroy:
	@( \
		cd terraform ; \
  	terraform destroy -lock-timeout=30s -auto-approve ; \
	)

deploy: terraform
	echo "deploy: $(image_name)"
