# Student Management System

A beginner-friendly full-stack student management project built with Django.

## Features

- Login/logout authentication
- Dashboard
- Add student
- View students
- Search students
- Edit student
- Delete student
- Django admin
- Bootstrap frontend
- SQLite database for easy setup

## Tech Stack

- Python
- Django
- HTML
- CSS
- Bootstrap
- SQLite

## Setup

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create admin/login user:

```bash
python manage.py createsuperuser
```

Start server:

```bash
python manage.py runserver
```

Open:

- http://127.0.0.1:8000/login/
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/admin/

## GitHub

Do not upload `.venv/`, `db.sqlite3`, passwords, API keys, or `.env` files.
