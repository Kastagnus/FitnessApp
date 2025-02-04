# 🏋️ Fitness App

## 📌 Overview

A Django REST Framework (DRF) project containerized with Docker, designed to provide backend API for managing resources efficiently. This project is built with Django, Django REST Framework, and PostgreSQL.

## ✨ Features

### 👤 User Management

- 📝 User registration
- 🔑 Token generation (JWT-based authentication)
- 🔐 Authentication with token
- 🚪 Logout (blacklisting refresh token)
- 🔄 Password change
- 🏠 User profile management

### 💪 Workouts

- 📜 Script for populating the database with workouts (`workouts/populate.py`)
  ```sh
  docker-compose exec container_name python workouts/populate.py
  ```
- ⚡ CRUD operations for workout plans

### 🎯 Tracking

- 🏆 Users can set a goal
- ⚖️ Two types of goals: `lose_weight` and `gain_muscle`
- 🎯 User sets a target value (KG) and initial value (KG)
- 📊 Users can enter weight updates, and progress is calculated automatically
- ✅ If the target is reached, the goal status is automatically updated to `completed`

### 🏃 Workout Mode

- 🛠️ CRUD operations for workout modes
- 🎮 Users can create a session in live mode by choosing a workout plan
- 🔄 Session returns ability to update every workout set (e.g., actual reps, duration, etc.)
- 📡 Automatic status updates based on session progress

## 🛠 Tech Stack

- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Containerization**: Docker

## 📋 Prerequisites

Ensure you have the following installed:

- 🐳 Docker & Docker Compose
- 🛠 Git
- 🐍 Python 3.9+

## 🚀 Installation & Setup

### 📂 Clone the Repository

```sh
git clone https://github.com/Kastagnus/FitnessApp.git
cd fitnessapp
```

### 🔑 Environment Variables

Create a `.env` file in the root directory with the following variables:
- Change YOUR_DB_NAME / YOUR_DB_USER / YOUR_DB_PASSWORD with your credentials
```
DEBUG=1
SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(50))')
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=YOUR_DB_NAME
DB_USER=YOUR_DB_USER
DB_PASSWORD=YOUR_DB_PASSWORD
DB_HOST=db
DB_PORT=5432
```

## 🏗 Running with Docker

To start the project with Docker, run:

```sh
docker-compose up --build
```

This will:

- 🏗 Build the necessary containers
- 🚀 Start the Django API and PostgreSQL services

Below find commands for final setup. (use "web" instead of "your-container-name" if you do not make changes into docker-compose.yaml file) 

To run migrations inside the container:

```sh
docker-compose exec -it your-container-name python manage.py migrate
```

To create a superuser:

```sh
docker-compose exec -it your-container-name python manage.py createsuperuser
```

To populate the workout database:

```sh
docker-compose exec your_container_name python workouts/populate.py
```

## 📖 API Documentation

All API endpoints are documented in Swagger UI. Access them at:

```sh
http://localhost:8000/api/docs/
```

This provides a user-friendly interface to test and interact with the API.
## Swagger Guide
- Register new user or generate token with created superuser
- On top right corner open Authorize and enter "Bearer your-access-token"
- Once you are authorised you can:
  - Change password
  - Update user profile
  - create workout plan (UPDATE/DELETE/RETRIEVE)
  - create fitness Goal tracking (UPDATE/DELETE/RETRIEVE)
  - create workout session and dynamically update data of every set on each exercise. (UPDATE/DELETE/RETRIEVE)


