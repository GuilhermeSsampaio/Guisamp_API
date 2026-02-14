# 🚀 GuiSamp API - Plataforma Multi-Projetos

> **API centralizada com arquitetura modular para portfólio profissional**

Plataforma robusta que combina autenticação unificada com múltiplos projetos independentes. Cada projeto possui seu próprio frontend **React PWA**, demonstrando full-stack development e boas práticas de arquitetura.

## 🏗️ Arquitetura

```
📁 auth/           → Sistema de autenticação compartilhado (JWT + OAuth)
📁 projects/       → Projetos modulares independentes
  └── cookAi/      → Assistente culinário com IA
📁 config/         → Configurações e middlewares centralizados
📁 infra/         → Docker, CI/CD e infraestrutura
```

## 🎯 Projetos Implementados

### 🍳 CookAI - Assistente Culinário Inteligente

- **Web Scraping** automatizado de receitas
- **Integração com Google Gemini AI** para processamento
- **CRUD completo** com autorização por usuário
- **PWA React** responsivo e offline-first
- **Busca semântica** e categorização inteligente

## ✨ Funcionalidades Técnicas

### 🔐 Sistema de Autenticação

- JWT com refresh tokens
- OAuth2 (Google integrado)
- Middleware de autorização customizado
- Proteção CORS configurável

### 🛠️ Arquitetura Clean Code

- **Repository Pattern** para acesso a dados
- **Dependency Injection** com FastAPI
- **Type Safety** completo com Pydantic/SQLModel
- **Separation of Concerns** rigorosa

### 🔄 DevOps & Qualidade

- Containerização completa (Docker + Compose)
- Environment-based configuration
- Estrutura preparada para CI/CD
- **Testes automatizados** com pytest (100 testes)

## 🚀 Stack Tecnológico

**Backend:**

- **FastAPI** (Python 3.11+) - API moderna e performática
- **SQLModel** - ORM type-safe com Pydantic
- **PostgreSQL** - Banco de dados robusto
- **Google Gemini AI** - Processamento de linguagem natural

**Frontend (por projeto):**

- **React + Vite**
- **PWA** (Progressive Web App)
- **Bootstrap CSS** - Styling moderno

**DevOps:**

- **Docker & Docker Compose**
- **Git workflow** com branches organizadas
- **Environment Variables** para configuração

## 🛠️ Instalação e Execução

### 📋 Pré-requisitos

- Python 3.11+
- Docker & Docker Compose
- Git

### 🐳 Docker (Recomendado)

```bash
# Clone o repositório
git clone <url-do-repositório>
cd guisamp_api

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas configurações

# Suba os serviços
docker compose -f infra/Docker-Compose.yaml up --build

# A API estará disponível em http://localhost:8000
```

### 🔧 Desenvolvimento Local

```bash
# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Configure o banco de dados
# Edite o .env para usar SQLite local se preferir

# Execute a aplicação
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 🧪 Testes

```bash

# Rodar todos os testes
pytest tests/ -v

# Apenas testes do módulo CookAi
pytest tests/cookai/ -v

# Apenas testes de autenticação compartilhada
pytest tests/shared/ -v

# Com relatório de cobertura (HTML)
pytest tests/ --cov=auth --cov=projects --cov-report=html

# Modo rápido (sem verbose)
pytest tests/ -q
```

## 📁 Estrutura Detalhada

```
guisamp_api/
├── auth/                    # Sistema de autenticação compartilhado
│   ├── models/             # User, AuthProvider
│   ├── schemas/            # Login, Register, Token schemas
│   ├── services/           # Lógica de autenticação
│   └── routes/             # Endpoints de auth
├── projects/               # Projetos modulares
│   └── cookAi/            # Assistente culinário
│       ├── models/        # Recipe, CookAiUser
│       ├── schemas/       # DTOs de entrada/saída
│       ├── repository/    # CRUD operations
│       ├── helpers/       # Validações e conversores
│       ├── services/      # IA, scraping, web search
│       └── routes/        # Endpoints específicos
├── tests/                 # Testes automatizados
│   ├── conftest.py       # Fixtures globais (SQLite in-memory)
│   ├── shared/           # Testes de auth e security
│   └── cookai/           # Testes de rotas, services e CRUD
├── config/                # Configurações globais
│   ├── db.py             # Setup do banco
│   ├── settings.py       # Environment configs
│   └── middlewares.py    # CORS, logging, etc
└── infra/                # Infrastructure as Code
    ├── Dockerfile
    └── Docker-Compose.yaml
```

## 🎓 Propósito Educacional

Este projeto foi desenvolvido como **portfólio profissional** demonstrando:

- ✅ **Clean Architecture** e **SOLID Principles**
- ✅ **Microservices Pattern** (projetos independentes)
- ✅ **API Design** seguindo REST e OpenAPI
- ✅ **Database Design** com relacionamentos complexos
- ✅ **Security Best Practices** (JWT, OAuth, CORS)
- ✅ **DevOps Practices** (Docker, Environment Config)
- ✅ **AI Integration** prática e funcional
- ✅ **Full-Stack Development** (Backend + Frontend PWA)

## 🤝 Contribuindo

Interessado em colaborar? Veja como:

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-feature`
3. Commit suas mudanças: `git commit -m 'Add: nova feature'`
4. Push para a branch: `git push origin feature/nova-feature`
5. Abra um Pull Request

### 📋 Guidelines

- Siga os padrões de código existentes
- Adicione testes para novas features
- Documente mudanças no README
- Use commits semânticos

## 📞 Contato

**Desenvolvedor:** Guilherme Sampaio

---

⭐ **Se este projeto te ajudou, deixe uma estrela!**

## 📄 Licença

Este projeto está sob licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

_Desenvolvido com ❤️ como demonstração de habilidades técnicas e arquiteturais._
