# Heroes and Villains API

A RESTful API built with **FastAPI** to manage a universe of heroes and villains, their powers, and the relationships between them.

![FastAPI](https://img.shields.io/badge/FastAPI-0.104.0-green?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)
![Railway](https://img.shields.io/badge/Deployed%20on-Railway-purple?logo=railway)

---

The API is publicly deployed on Railway:

> 🌍 **Base URL:** [`https://heroes-and-villains-api-production.up.railway.app/`](https://heroes-and-villains-api-production.up.railway.app/)

You can explore the full interactive documentation at:

- **Swagger UI**: [`https://heroes-and-villains-api-production.up.railway.app/docs`](https://heroes-and-villains-api-production.up.railway.app/docs)

> ⚠️ Endpoints that modify data (`POST`, `DELETE`, etc.) are protected with OAuth2 + JWT authentication.

---

## 🚀 Features

### 🦸 Characters

- Create new heroes and villains *(JWT required)*
- Get all characters or a specific one
- Update character data *(JWT required)*
- Delete characters *(JWT required)*

### 💥 Powers

- Add new powers *(JWT required)*
- View all powers or specific one
- Update power attributes *(JWT required)*
- Delete powers *(JWT required)*

### 🔗 Character Powers

- Assign powers to characters *(JWT required)*
- Get powers by character
- Remove power from character *(JWT required)*

### 🔐 Authentication

- Secure login with `OAuth2PasswordBearer`
- JWT tokens for protected routes

---

## 🧱 Tech Stack

- **FastAPI** — High-performance Python web framework
- **SQLModel** — SQLAlchemy + Pydantic in one
- **PostgreSQL** — Cloud database hosted on Railway
- **Uvicorn** — ASGI server
- **Railway** — Deployment platform for API and database
- **Alembic** — Database migrations

---

## 🛠 Local Development

Clone the repository and install dependencies:

```bash
pip install -r requirements.txt
```

Set your environment variables in a .env file:

```bash
DATABASE_URL=your_postgresql_url
SECRET_KEY=your_secret_key
```
Run the API:

```bash
uvicorn app.main:app --reload
```

---

## 📬 Contact

Made with ❤️ by Juan Aichino

