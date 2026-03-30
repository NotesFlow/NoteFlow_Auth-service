# NoteFlow Auth Service

Microserviciul de autentificare pentru proiectul **NoteFlow**.

Acest serviciu gestionează:
- înregistrarea utilizatorilor
- autentificarea utilizatorilor
- generarea de token-uri JWT
- validarea utilizatorului curent autentificat

## Funcționalități implementate

- `POST /register`
- `POST /login`
- `GET /me`
- `GET /health`
- `GET /health/db`

## Tehnologii folosite

- Python 3.10
- FastAPI
- SQLAlchemy
- PostgreSQL
- PyJWT
- pwdlib cu Argon2
- Docker

## Structura proiectului

```text
app/
├── core/
│   ├── config.py
│   └── security.py
├── db/
│   ├── base.py
│   └── session.py
├── dependencies/
│   ├── __init__.py
│   └── auth.py
├── models/
│   ├── __init__.py
│   └── user.py
├── routers/
│   ├── __init__.py
│   └── auth.py
├── schemas/
│   ├── __init__.py
│   └── auth.py
└── main.py
```

## Variabile de mediu

Creează un fișier `.env` pornind de la `.env.example`.

Exemplu:

```env
AUTH_SERVICE_PORT=8001
APP_NAME=NoteFlow Auth Service
APP_VERSION=0.1.0
DEBUG=false

DATABASE_HOST=127.0.0.1
DATABASE_PORT=5433
DATABASE_NAME=noteflow
DATABASE_USER=noteflow_user
DATABASE_PASSWORD=noteflow_pass

JWT_SECRET_KEY=change_this_to_a_long_random_secret_key_32_chars_min
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Instalare locală

### 1. Creează și activează mediul virtual

Pe Linux / WSL:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Pe Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Instalează dependențele

```bash
pip install -r requirements.txt
```

### 3. Pornește serviciul

```bash
uvicorn app.main:app --reload --port 8001
```

Serviciul va fi disponibil la:

```text
http://127.0.0.1:8001
```

Swagger UI:

```text
http://127.0.0.1:8001/docs
```

## Pornirea bazei de date

Serviciul are nevoie de PostgreSQL pornit.

Dacă folosești repository-ul de infrastructură:

```bash
docker compose -f docker-compose.dev.yml up -d
```

Asigură-te că valorile din `.env` corespund cu cele folosite de PostgreSQL.

## Endpoint-uri

### `GET /health`

Verifică dacă serviciul rulează.

Răspuns exemplu:

```json
{
  "status": "ok",
  "service": "NoteFlow Auth Service",
  "version": "0.1.0"
}
```

### `GET /health/db`

Verifică dacă serviciul se poate conecta la baza de date.

Răspuns exemplu:

```json
{
  "status": "ok",
  "database": "connected"
}
```

### `POST /register`

Creează un utilizator nou.

Body exemplu:

```json
{
  "username": "albert",
  "email": "albert@example.com",
  "password": "parola123"
}
```

Răspuns exemplu:

```json
{
  "id": 1,
  "username": "albert",
  "email": "albert@example.com"
}
```

### `POST /login`

Autentifică utilizatorul și returnează un token JWT.

Body exemplu:

```json
{
  "username": "albert",
  "password": "parola123"
}
```

Răspuns exemplu:

```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer"
}
```

### `GET /me`

Returnează utilizatorul autentificat curent.

Header necesar:

```text
Authorization: Bearer <access_token>
```

Răspuns exemplu:

```json
{
  "id": 1,
  "username": "albert",
  "email": "albert@example.com",
  "created_at": "2026-03-31T12:00:00"
}
```

## Testare rapidă

### 1. Register

```bash
curl -X POST "http://127.0.0.1:8001/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "albert",
    "email": "albert@example.com",
    "password": "parola123"
  }'
```

### 2. Login

```bash
curl -X POST "http://127.0.0.1:8001/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "albert",
    "password": "parola123"
  }'
```

### 3. Get current user

```bash
curl -X GET "http://127.0.0.1:8001/me" \
  -H "Authorization: Bearer TOKENUL_TAU"
```

## Rulare cu Docker

### Build imagine

```bash
docker build -t noteflow-auth-service .
```

### Rulare container

```bash
docker run --rm -p 8001:8001 --env-file .env noteflow-auth-service
```

## Observații

- parola este stocată hash-uită, nu în clar
- autentificarea se face cu JWT
- tabela `users` este creată automat la pornirea aplicației
- pentru producție, `JWT_SECRET_KEY` trebuie schimbat cu o valoare sigură și lungă
- pentru moment, serviciul este gândit ca MVP pentru proiectul NoteFlow

## Status curent

Acest serviciu acoperă MVP-ul pentru autentificare:
- înregistrare utilizator
- login
- identificare utilizator curent

Pașii următori, în afara acestui repo, sunt integrarea în `docker-compose`, conectarea prin gateway și folosirea lui de către celelalte microservicii.
