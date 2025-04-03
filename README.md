# FastAPI Blog Application with MySQL

A complete blog application built with FastAPI following MVC architecture, featuring user authentication, post management, and MySQL database integration.

## Features

- User authentication (signup/login with JWT tokens)
- Create, read, and delete blog posts
- MySQL database integration with SQLAlchemy ORM
- Request validation and payload size limits
- Response caching for improved performance
- Comprehensive error handling
- Pydantic data validation

## Prerequisites

- Python 3.9+
- MySQL server
- Redis (for caching)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/taiwo2/FastAPI-blog.git
cd fastapi-mysql-blog

python -m venv venv
source venv/bin/activate  # On macOS/Linux

brew services start mysql

pip install fastapi uvicorn sqlalchemy pymysql python-jose[cryptography] passlib redis python-multipart pydantic[email]

pip install -r requirements.txt