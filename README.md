# Task Manager API

A RESTful Task Manager API built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**.

## Features

* Create tasks
* Get all tasks
* Get a task by ID
* Update tasks
* Delete tasks
* PostgreSQL database
* SQLAlchemy ORM
* Pydantic request and response validation
* Environment variables for database credentials
* Automatic interactive API documentation with Swagger UI

## Tech Stack

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Pydantic
* Uvicorn
* Git & GitHub

## Project Structure

```text
task-manager-api/
├── .env
├── .gitignore
├── database.py
├── main.py
├── models.py
├── schemas.py
└── README.md
```

### File Responsibilities

* `main.py` — FastAPI application and API routes
* `database.py` — PostgreSQL connection and SQLAlchemy session
* `models.py` — SQLAlchemy database models
* `schemas.py` — Pydantic request and response schemas
* `.env` — Database configuration and credentials
* `.gitignore` — Files that should not be uploaded to Git

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
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv
```

### 4. Configure the database

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/task_manager
```

Replace the username, password, and database name with your PostgreSQL configuration.

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

| Method | Endpoint           | Description                  |
| ------ | ------------------ | ---------------------------- |
| GET    | `/`                | Test the API                 |
| GET    | `/db-test`         | Test the database connection |
| GET    | `/tasks`           | Get all tasks                |
| POST   | `/tasks`           | Create a task                |
| GET    | `/tasks/{task_id}` | Get a specific task          |
| PUT    | `/tasks/{task_id}` | Update a task                |
| DELETE | `/tasks/{task_id}` | Delete a task                |

## Example

### Create a task

```json
{
  "title": "Learn Docker",
  "completed": false
}
```

### Response

```json
{
  "id": 1,
  "title": "Learn Docker",
  "completed": false
}
```

## Security

Database credentials are stored in `.env` and are excluded from Git using `.gitignore`.

**Never commit your `.env` file or database passwords to GitHub.**
