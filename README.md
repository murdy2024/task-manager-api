# Task Manager API

A RESTful Task Manager API built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**, featuring user authentication and authorization with JWT.

## Features

* User registration
* Secure password hashing
* User login with JWT authentication
* OAuth2 Bearer token authentication
* Create tasks
* Get all tasks belonging to the authenticated user
* Get a task by ID
* Update tasks
* Delete tasks
* User-specific task ownership
* PostgreSQL database
* SQLAlchemy ORM
* Pydantic request and response validation
* Environment variables for sensitive configuration
* Automatic interactive API documentation with Swagger UI

## Tech Stack

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Pydantic
* PyJWT
* pwdlib
* OAuth2
* Uvicorn
* python-dotenv
* Git & GitHub

## Project Structure

```text
task-manager-api/
│
├── .env
├── .gitignore
├── auth.py
├── database.py
├── jwt_token.py
├── main.py
├── models.py
├── schemas.py
└── README.md
```

### File Responsibilities

* `main.py` — FastAPI application, routes, authentication, and authorization
* `database.py` — PostgreSQL connection and SQLAlchemy session
* `models.py` — SQLAlchemy database models and relationships
* `schemas.py` — Pydantic request and response schemas
* `auth.py` — Password hashing and password verification
* `jwt_token.py` — JWT access token creation
* `.env` — Database credentials and secret configuration
* `.gitignore` — Files that should not be uploaded to Git

## Authentication

The API uses **JWT Bearer tokens** for authentication.

### Registration

Create a new account using:

```http
POST /register
```

Example request:

```json
{
  "username": "john",
  "email": "john@example.com",
  "password": "mypassword"
}
```

### Login

Login using:

```http
POST /login
```

The login endpoint uses OAuth2 form data:

```text
username=john
password=mypassword
```

A successful login returns:

```json
{
  "access_token": "your-jwt-token",
  "token_type": "bearer"
}
```

Use this token to authenticate requests to protected task endpoints.

## Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>

cd task-manager-api
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv pyjwt pwdlib
```

### 4. Configure the database

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/task_manager
SECRET_KEY=your-secret-key
```

Replace the values with your PostgreSQL configuration and a secure secret key.

**Never commit your `.env` file to GitHub.**

### 5. Run the API

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint           | Authentication | Description                        |
| ------ | ------------------ | -------------- | ---------------------------------- |
| GET    | `/`                | No             | Test the API                       |
| GET    | `/db-test`         | No             | Test the database connection       |
| POST   | `/register`        | No             | Register a new user                |
| POST   | `/login`           | No             | Login and receive a JWT            |
| GET    | `/tasks`           | Yes            | Get the authenticated user's tasks |
| POST   | `/tasks`           | Yes            | Create a task                      |
| GET    | `/tasks/{task_id}` | Yes            | Get a specific task                |
| PUT    | `/tasks/{task_id}` | Yes            | Update a task                      |
| DELETE | `/tasks/{task_id}` | Yes            | Delete a task                      |

## Example

### Create a task

After authenticating, send:

```json
{
  "title": "Learn Docker",
  "completed": false
}
```

Example response:

```json
{
  "id": 1,
  "title": "Learn Docker",
  "completed": false
}
```

Tasks belong to the user who created them. Authenticated users can only access, update, and delete their own tasks.

## Security

* Passwords are hashed before being stored in the database.
* Password hashes are never returned through the API.
* JWT tokens are used to authenticate protected endpoints.
* Users can only access their own tasks.
* Database credentials and the JWT secret are stored in `.env`.
* `.env` is excluded from Git using `.gitignore`.

**Never commit your `.env` file, database password, or JWT secret to GitHub.**
