# BECT Blog

## Description
BECT Blog is a platform for sharing ideas, experiences and insights. Registered users can write, edit and delete their own posts, upload a profile picture, and reset a forgotten password by email. The application is available at [fabiothon.ch](https://fabiothon.ch), where all posts can be read online.

The application is built with FastAPI and serves server-rendered Jinja2 pages (Tailwind CSS) alongside a JSON REST API under `/api`. Data is stored in PostgreSQL through async SQLAlchemy. Users log in with JWT tokens, profile pictures are stored in AWS S3, and the app runs in Docker on Google Cloud Run.

## Application Overview
### Application in light mode
<img width="3544" height="2213" alt="light_mode" src="https://github.com/user-attachments/assets/43322e2f-3ae5-4c16-8c57-afc72c3c0891" />

### Application in dark mode
<img width="3544" height="2213" alt="dark_mode" src="https://github.com/user-attachments/assets/a59093f4-c1b0-4e20-91b4-8ffeffc696e1" />

## Repository Structure
```
BECT_Blog/
├── main.py           # App, page routes, middleware, error handlers
├── config.py         # Sets environment
├── database.py       # Async engine, session, get_db
├── models.py         # User, Post, PasswordResetToken
├── schemas.py        # Pydantic request/response models
├── auth.py           # Password hashing, JWT, current user
├── image_utils.py    # Image processing, S3 upload/delete
├── email_utils.py    # Password reset email
├── routers/          # /api/users, /api/posts
├── templates/        # Jinja2 pages and email template
├── static/           # CSS, JS, icons
├── tests/            # pytest suite
├── Dockerfile
└── requirements.txt
```

## Installation
```bash
pip install -r requirements.txt -r requirements-dev.txt
tailwindcss -i static/css/input.css -o static/css/output.css --minify
```
Create a `.env` file with at least `DATABASE_URL`, `SECRET_KEY` and `S3_BUCKET_NAME`. For the optional S3, mail and app settings, see `config.py`. The database schema is not created automatically.

## Usage
```bash
fastapi dev main.py
python -m pytest

docker build -t bectblog .
docker run -p 8080:8080 --env-file .env bectblog
```

