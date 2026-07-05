<div align="center">

# 🛒 UMarket

### Sistema de Mercado Autônomo

*Projeto acadêmico — Desenvolvimento Web · UDESC · Tecnologia em Análise e Desenvolvimento de Sistemas*

[![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-black?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-336791?logo=postgresql&logoColor=white)](https://supabase.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Poetry](https://img.shields.io/badge/Poetry-dependency%20management-60A5FA?logo=poetry&logoColor=white)](https://python-poetry.org/)
[![Deploy](https://img.shields.io/badge/Deploy-Render-46E3B7?logo=render&logoColor=white)](https://render.com/)

**[🔗 Acessar aplicação em produção](https://umarket-web.onrender.com)**

</div>

---

## 📖 Sobre o projeto

O **UMarket** simula o modelo de negócio de um **mercado autônomo**: um ponto de venda que funciona sem atendimento presencial, onde o cliente consulta produtos, monta o carrinho e finaliza a compra pela própria plataforma.

O sistema foi desenvolvido com **duas frentes de uso**:

| Perfil | O que faz |
|---|---|
| 🧑‍💼 **Cliente** | Cria conta, navega pelo catálogo, monta o carrinho, escolhe o PDV de retirada e finaliza a compra |
| 🛠️ **Administrador** | Gerencia produtos, controla estoque por unidade, acompanha vendas e usuários |

> ⚠️ Nota de deploy: a aplicação roda no plano gratuito da Render, que hiberna após 15 minutos sem uso. A primeira requisição depois disso pode levar de 30 a 60 segundos para responder — é esperado, não é bug.

---

## 📑 Índice

- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias)
- [Estrutura do projeto](#-estrutura-do-projeto)
- [Rodando localmente](#-rodando-localmente)
- [Deploy](#-deploy)
- [Guia de uso — Área do Cliente](#-guia-de-uso--área-do-cliente)
- [Guia de uso — Área Administrativa](#-guia-de-uso--área-administrativa)
- [Modelagem do banco de dados](#-modelagem-do-banco-de-dados)
- [Autores](#-autores)

---

## ✅ Funcionalidades

**Cliente**
- Cadastro e login (RF01, RF02)
- Catálogo com busca e filtro por categoria (RF03, RF04)
- Carrinho de compras em sessão (RF05, RF06)
- Checkout com escolha de PDV e forma de pagamento (RF07)
- Baixa automática de estoque ao finalizar a compra (RF18)
- Histórico de pedidos e edição de perfil (RF08, RF09)

**Administrador**
- CRUD de produtos, com imagem por URL ou placeholder colorido por categoria (RF10–RF13)
- Controle de estoque por ponto de venda (RF14)
- Gerenciamento de categorias (RF15)
- Consulta de pedidos por PDV (RF16)
- Gerenciamento de permissões de usuários (RF17)
- Dashboard com métricas gerais (produtos, usuários, vendas, faturamento)

---

## 🧰 Tecnologias

| Camada | Ferramenta |
|---|---|
| Backend | Python 3.13 + Flask |
| Templates | Jinja2 + Bootstrap 5 |
| ORM | SQLAlchemy (Flask-SQLAlchemy) |
| Autenticação | Flask-Login |
| Banco de dados | PostgreSQL (hospedado no Supabase) |
| Gerenciador de dependências | Poetry |
| Servidor de produção | Gunicorn |
| Hospedagem | Render |

---

## 📁 Estrutura do projeto

```
Umarket/
├── migrations/                  # Scripts SQL versionados (rodar em ordem)
│   ├── 001_alter_usuarios_auth.sql
│   ├── 002_fix_sequences.sql
│   └── 003_add_imagem_produtos.sql
├── scripts/
│   └── seed_senhas.py           # Define senha padrão para usuários de teste
├── src/umarket/
│   ├── app.py                   # Application factory (cria a instância Flask)
│   ├── config.py                # Configurações lidas do .env
│   ├── extensions.py            # db, login_manager
│   ├── models/                  # Usuario, Produto, Pdv, Estoque, Venda, VendaProduto
│   ├── routes/                  # auth, cliente, admin (blueprints)
│   ├── services/                # Regras de negócio (carrinho, finalização de venda)
│   ├── static/                  # CSS e JS
│   └── templates/               # HTML (cliente/ e admin/)
├── tests/                       # Testes automatizados
├── pyproject.toml
└── .env                         # Variáveis de ambiente (não versionado)
```

---

## 💻 Rodando localmente

### Pré-requisitos
- Python 3.13+
- [Poetry](https://python-poetry.org/docs/#installation)
- Uma instância PostgreSQL acessível (o projeto usa o [Supabase](https://supabase.com/), gratuito)

### 1. Clone e instale as dependências
```bash
git clone <url-do-repositorio>
cd Umarket
poetry install
```

### 2. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto:
```dotenv
DATABASE_URL=postgresql://postgres.<seu-project-ref>:<senha>@<host-do-pooler>:5432/postgres
SECRET_KEY=uma-chave-secreta-qualquer
FLASK_ENV=development
```
> 💡 Use sempre a string do **Session Pooler** (Project Settings → Database → Connection String no painel do Supabase), copiada exatamente como aparece lá — não reconstrua manualmente.

### 3. Aplique o schema e as migrations, nesta ordem
```bash
psql "<sua DATABASE_URL>" -f backup.sql
psql "<sua DATABASE_URL>" -f migrations/001_alter_usuarios_auth.sql
psql "<sua DATABASE_URL>" -f migrations/002_fix_sequences.sql
psql "<sua DATABASE_URL>" -f migrations/003_add_imagem_produtos.sql
```

### 4. Gere as senhas dos usuários de seed
```bash
poetry run python scripts/seed_senhas.py
```
Isso define a senha `123456` para todos os usuários de teste e confirma **nathan@umarket.com** como administrador.

### 5. Rode a aplicação
```bash
poetry run python src/umarket/app.py
```
Acesse `http://localhost:5000`.

---

## 🚀 Deploy

A aplicação está hospedada na **[Render](https://render.com/)**, no plano gratuito. Resumo da configuração:

| Campo | Valor |
|---|---|
| **Build Command** | `pip install --upgrade pip && pip install poetry && poetry config virtualenvs.in-project true && poetry install --no-interaction --no-ansi` |
| **Start Command** | `poetry run gunicorn "umarket.app:create_app()" --bind 0.0.0.0:$PORT` |
| **Variáveis de ambiente** | `DATABASE_URL`, `SECRET_KEY`, `FLASK_ENV=production` |

Todo `git push` para a branch principal gera um redeploy automático. Em caso de erro persistente, use **"Clear build cache & deploy"** no painel da Render antes de investigar o código.

---

## 🧑‍💼 Guia de uso — Área do Cliente

| Aba | O que fazer nela |
|---|---|
| **Início** | Vitrine com produtos em destaque e atalho para o catálogo |
| **Catálogo** | Buscar produtos por nome ou filtrar por categoria; adicionar direto ao carrinho |
| **Carrinho** 🛒 | Ajustar quantidades, remover itens e ver o total antes de finalizar |
| **Checkout** | Escolher o PDV de retirada e a forma de pagamento — é aqui que o estoque é validado e debitado |
| **Meus Pedidos** | Histórico de compras já finalizadas, com o detalhamento de cada item |
| **Perfil** | Atualizar nome e trocar a senha |

> É necessário estar logado para finalizar uma compra e ver o histórico. Cadastro e login ficam nos botões no canto superior direito.

## 🛠️ Guia de uso — Área Administrativa

Acesse pelo link **Admin** na navbar (aparece só para usuários com permissão de administrador) ou diretamente em `/admin/login`.

| Aba | O que fazer nela |
|---|---|
| **Dashboard** | Visão geral: total de produtos, usuários, vendas e faturamento acumulado |
| **Produtos** | Cadastrar, editar e excluir produtos — inclusive definir uma URL de imagem |
| **Estoque** | Ajustar a quantidade atual e a capacidade de cada produto, por PDV |
| **Categorias** | Renomear categorias em lote (atualiza todos os produtos daquela categoria de uma vez) |
| **Usuários** | Consultar clientes cadastrados e conceder ou remover permissão de administrador |
| **Pedidos** | Consultar todas as vendas realizadas, com filtro por PDV |

> O primeiro usuário administrador é criado automaticamente pelo script `scripts/seed_senhas.py` (`nathan@umarket.com`). Para promover outro usuário, use a aba **Usuários**.

---

## 🗃️ Modelagem do banco de dados

O banco é composto por 6 entidades principais: **usuarios**, **produtos**, **pdv**, **estoque**, **vendas** e **vendas_produtos**, com relacionamentos 1:N entre usuário↔venda, PDV↔venda, PDV↔estoque e venda↔itens de venda. O diagrama conceitual e o dicionário de dados completos estão na documentação acadêmica do projeto.

---

## 👥 Autores

- **Gabriel Otávio de Barros**
- **Nathan Carlos da Silva**

Projeto desenvolvido para a disciplina de Desenvolvimento Web — UDESC, 2026.