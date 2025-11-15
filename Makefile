.PHONY: help build up down logs shell test lint format check

# Cores para output
GREEN  := \033[0;32m
YELLOW := \033[0;33m
NC     := \033[0m # No Color

help: ## Mostra esta ajuda
	@echo "$(GREEN)Comandos disponíveis:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2}'

build: ## Constrói as imagens Docker
	docker-compose build

up: ## Inicia os containers
	docker-compose up

down: ## Para os containers
	docker-compose down

logs: ## Mostra logs dos containers
	docker-compose logs -f

shell: ## Abre shell no container web
	docker-compose exec web bash

migrate: ## Aplica migrações do banco
	docker-compose run --rm web python manage.py migrate

makemigrations: ## Cria novas migrações
	docker-compose run --rm web python manage.py makemigrations

createsuperuser: ## Cria superusuário
	docker-compose run --rm web python manage.py createsuperuser

test: ## Roda testes
	docker-compose run --rm web python manage.py test

lint: ## Roda pylint em todo o código
	pylint --rcfile=.pylintrc config/ shortener/

format: ## Formata código com black e isort
	black --line-length=100 .
	isort --profile=black --line-length=100 .

check: ## Roda todas as verificações
	@echo "$(GREEN)Rodando pre-commit em todos os arquivos...$(NC)"
	pre-commit run --all-files

clean: ## Remove arquivos temporários
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete

reset: ## Reset completo (cuidado!)
	docker-compose down -v
	docker-compose build --no-cache
	docker-compose up
```

---

## 📚 PASSO 8: Atualizar `.gitignore`

Adicione ao final do `.gitignore`:
```
# Mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pylint
.pylintrc.d/

# Coverage
.coverage
htmlcov/
