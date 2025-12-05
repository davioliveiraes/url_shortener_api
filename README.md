# 🔗 URL Shortener API

> REST API profissional para encurtamento de URLs com Django REST Framework, PostgreSQL e Docker.

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14.0-red.svg)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/Tests-53%20passing-brightgreen.svg)](https://github.com/davioliveiraes/url-shortener-api)

---

## Vídeo de uso da API!

**[▶️ Assistir demonstração completa no YouTube (10 minutos)](https://www.youtube.com/watch?v=HmWwuJSEhFU)**

*O vídeo demonstra: criação de URLs, tracking de cliques, QR Codes, estatísticas, validações, interface admin e testes automatizados.*

---

## Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Arquitetura](#arquitetura)
- [Instalação](#instalação)
- [Uso](#uso)
- [API Endpoints](#api-endpoints)
- [Testes](#testes)
- [Demo Online](#demo-online)
- [Documentação](#documentação)
- [Contribuindo](#contribuindo)

---

## Sobre o Projeto

API RESTful completa para encurtamento de URLs, desenvolvida com as melhores práticas de engenharia de software. O projeto demonstra habilidades em desenvolvimento backend, arquitetura de APIs, containerização e qualidade de código.

### Destaques

- ✅ **53 testes automatizados** com 100% de sucesso
- ✅ **Cobertura completa** de models, serializers e views
- ✅ **Código limpo** seguindo PEP 8 e boas práticas
- ✅ **Dockerizado** para fácil deployment
- ✅ **Documentação completa** com Postman
- ✅ **Interface Admin** customizada

---

## Funcionalidades

### Core Features

- 🔗 **Encurtamento de URLs** com código auto-gerado ou customizado
- 📊 **Tracking de Cliques** (total e únicos por IP)
- ⏰ **URLs com Expiração** (data/hora customizável)
- 🔢 **Limite de Cliques** (máximo de acessos configurável)
- 🎨 **QR Code Automático** gerado para cada URL
- 🔍 **Busca e Filtros** avançados
- 📈 **Estatísticas Detalhadas** por URL
- ✅ **Ativar/Desativar URLs** dinamicamente

### Segurança e Validações

- ✅ Validação de formato de URL
- ✅ Código curto alfanumérico (mínimo 3 caracteres)
- ✅ Unicidade de códigos curtos
- ✅ Validação de datas de expiração
- ✅ Proteção contra valores inválidos

---

## Tecnologias

### Backend
- **Python 3.13** - Linguagem principal
- **Django 4.2.7** - Framework web
- **Django REST Framework 3.14.0** - API REST
- **PostgreSQL 16** - Banco de dados
- **psycopg3** - Driver PostgreSQL

### DevOps & Tools
- **Docker & Docker Compose** - Containerização
- **Git** - Controle de versão

### Qualidade de Código
- **pylint** - Linter
- **black** - Formatação automática
- **isort** - Organização de imports
- **pre-commit** - Git hooks

### Bibliotecas Adicionais
- **qrcode** - Geração de QR Codes
- **Pillow** - Processamento de imagens

---

## Arquitetura
```
┌─────────────┐
│   Cliente   │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│   Django REST API   │
│  ┌───────────────┐  │
│  │   ViewSets    │  │
│  │  Serializers  │  │
│  │    Models     │  │
│  └───────┬───────┘  │
└──────────┼──────────┘
           │
           ▼
    ┌──────────────┐
    │  PostgreSQL  │
    └──────────────┘
```

### Padrões de Projeto

- **MVT** (Model-View-Template) - Arquitetura Django
- **Repository Pattern** - Camada de abstração de dados
- **Serializer Pattern** - Validação e transformação de dados
- **ViewSet Pattern** - Organização de endpoints REST

---

## Instalação

### Pré-requisitos

- Docker 20.10+
- Docker Compose 2.0+
- Git

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/davioliveiraes/url_shortener_api.git
cd url_shortener_api
```

2. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite o .env com suas configurações
```

3. **Suba os containers**
```bash
docker-compose up -d
```

4. **Execute as migrações**
```bash
docker-compose exec web python manage.py migrate
```

5. **Crie um superusuário**
```bash
docker-compose exec web python manage.py createsuperuser
```

6. **Acesse a API**
- API: http://localhost:8000/api/urls/
- Admin: http://localhost:8000/admin/

---

## Uso

### Criar URL Encurtada
```bash
curl -X POST http://localhost:8000/api/urls/ \
  -H "Content-Type: application/json" \
  -d '{
    "original_url": "https://github.com/yourusername"
  }'
```

**Response:**
```json
{
  "id": 1,
  "short_code": "abc123",
  "original_url": "https://github.com/yourusername",
  "short_url": "http://localhost:8000/api/r/abc123/",
  "qr_code": "http://localhost:8000/media/qrcodes/abc123.png",
  "is_active": true,
  "total_clicks": 0,
  "unique_clicks": 0,
  "created_at": "2024-12-01T10:00:00Z"
}
```

### Redirecionar
```bash
curl -L http://localhost:8000/api/r/abc123/
# Redireciona para https://github.com/yourusername
```

### Obter Estatísticas
```bash
curl http://localhost:8000/api/urls/abc123/statistics/
```

**Response:**
```json
{
  "short_code": "abc123",
  "total_clicks": 42,
  "unique_clicks": 28,
  "is_expired": false,
  "has_reached_max_clicks": false,
  "recent_clicks": [
    {
      "ip_address": "192.168.1.1",
      "user_agent": "Mozilla/5.0...",
      "clicked_at": "2024-12-01T15:30:00Z"
    }
  ]
}
```

---

## API Endpoints

### URLs

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/urls/` | Lista todas as URLs |
| POST | `/api/urls/` | Cria nova URL |
| GET | `/api/urls/{code}/` | Detalhes da URL |
| PATCH | `/api/urls/{code}/` | Atualiza URL |
| DELETE | `/api/urls/{code}/` | Deleta URL |

### Actions

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/urls/{code}/activate/` | Ativa URL |
| POST | `/api/urls/{code}/deactivate/` | Desativa URL |
| GET | `/api/urls/{code}/statistics/` | Estatísticas |
| GET | `/api/urls/{code}/qrcode/` | QR Code |

### Redirect

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/r/{code}/` | Redireciona para URL original |

### Filtros e Busca
```bash
# Buscar por palavra-chave
GET /api/urls/?search=github

# Filtrar por status
GET /api/urls/?is_active=true

# Paginação
GET /api/urls/?page=2
```

---

## Testes

### Executar Todos os Testes
```bash
docker-compose exec web python manage.py test shortener.tests
```

**Resultado:**
```
Found 53 test(s).
System check identified no issues (0 silenced).
.....................................................
----------------------------------------------------------------------
Ran 53 tests in 1.310s

OK
```

### Categorias de Testes

- ✅ **Models** (13 testes) - Lógica de negócio
- ✅ **Serializers** (16 testes) - Validações
- ✅ **Views** (15 testes) - Endpoints CRUD
- ✅ **Redirects** (9 testes) - Tracking de cliques

---

## Demo Online

> ⚠️ **Demonstração temporária** para fins de portfólio.

**API em Produção:** https://url-shortener-api-9h2j.onrender.com

### Teste Rápido:
```bash
# Listar URLs
curl https://url-shortener-api-9h2j.onrender.com/api/urls/

# Criar URL encurtada
curl -X POST https://url-shortener-api-9h2j.onrender.com/api/urls/ \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://github.com/davioliveiraes"}'

# Redirecionar (substitua {code})
https://url-shortener-api-9h2j.onrender.com/api/r/{code}/
```

### Django Admin:
- **URL:** https://url-shortener-api-9h2j.onrender.com/admin/
- **User:** admin (senha disponível sob solicitação)

### ⚠️ Nota sobre QR Codes:

Os QR Codes são gerados automaticamente, mas devido ao **storage efêmero do Render** (limitação do plano gratuito), as imagens não persistem entre deploys.

**Para produção real:** AWS S3 ou Cloudinary
**Para visualizar QR Codes:** Rode localmente com Docker

📸 **Screenshots completos** disponíveis em [`docs/screenshots/`](docs/screenshots/)

### Características do Deploy:
- ✅ PostgreSQL 16 em produção
- ✅ Gunicorn + WhiteNoise
- ✅ SSL/HTTPS automático
- ✅ CI/CD via GitHub
- ✅ 53 testes (100% passing)

### Endpoints Principais:

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/urls/` | Lista URLs |
| POST | `/api/urls/` | Cria URL |
| GET | `/api/urls/{code}/` | Detalhes |
| GET | `/api/urls/{code}/statistics/` | Estatísticas |
| GET | `/api/urls/{code}/qrcode/` | QR Code* |
| GET | `/api/r/{code}/` | Redireciona |

> *QR Codes funcionam via download. Para persistência, configure storage externo.

---

## Documentação

### Postman Collection

Importe a coleção completa do Postman:

1. Abra o Postman
2. Import → `docs/postman_collection.json`
3. Import environment → `docs/postman_environment.json`
4. Configure a variável `base_url` para `http://localhost:8000`

### Exemplos de Uso

Veja exemplos detalhados em [`docs/EXAMPLES.md`](docs/EXAMPLES.md)

---

## Contribuindo

Contribuições são bem-vindas!

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---


## Autor

**Davi Oliveira**

- GitHub: [@davioliveira](https://github.com/davioliveiraes)
- LinkedIn: [Davi Oliveira](https://linkedin.com/in/davioliveiraes)
- YouTube: [Davi Oliveira](https://www.youtube.com/@davioliveiraES)

---

## Mostre seu Apoio

Se este projeto foi útil, considere dar uma ⭐!

---
