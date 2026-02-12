# guisamp_api

API centralizada para autenticação e gerenciamento de usuários, pensada para servir múltiplos projetos pessoais de portfólio. Permite login via senha e integração futura com provedores como Google e GitHub.

## Expansão futura de projetos pessoais

## ✨ Funcionalidades

- Registro e login de usuários com JWT
- Suporte a múltiplos provedores de autenticação (senha, Google, GitHub, etc.)
- Endpoints protegidos por Bearer Token
- Estrutura modular para fácil expansão

## 🚀 Tecnologias

- Python 3.11+
- FastAPI
- SQLModel
- Docker & Docker Compose

## 🛠️ Como rodar

### Local (venv)

```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

### Docker

```bash
docker compose -f infra/Docker-Compose.yaml up --build
```

## ⚙️ Variáveis de ambiente

Crie um arquivo `.env` na raiz com, por exemplo:

```
DATABASE_URL=sqlite:///./db.sqlite3
JWT_SECRET=umasecretforte
JWT_ALGORITHM=HS256
JWT_EXPIRES_IN=3600
```

## 🔑 Autenticação

- `POST /auth/register` — Cria novo usuário
- `POST /auth/login` — Retorna access token
- Para acessar rotas protegidas, envie:
  - Header: `Authorization: Bearer <token>`

### Exemplo de uso (login)

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "seu@email.com", "password": "suasenha"}'
```

## 📁 Estrutura de pastas

- `auth/` — autenticação, schemas, serviços e rotas
- `config/` — configurações (banco, segurança)
- `infra/` — Dockerfile e compose
- `routes/` — rotas gerais da API
- `scripts/` — scripts utilitários

## 🗺️ Roadmap

- [ ] Integração com Google OAuth
- [ ] Integração com GitHub OAuth
- [ ] Rate limiting
- [ ] Logs estruturados

## 🤝 Contribuindo

Pull requests são bem-vindos! Sinta-se à vontade para propor melhorias ou abrir issues.

## 📄 Licença

Uso pessoal e educacional.
