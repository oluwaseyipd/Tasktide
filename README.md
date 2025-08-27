# Tasktide

A simple and efficient **Task Management API** built with **Django** and **Django REST Framework**. Tasktide allows users to **create, read, update, and delete (CRUD)** tasks with authentication and token-based access.

## Features

- 🔑 User registration and login with token authentication
- ✅ Create, retrieve, update, and delete tasks
- 📌 Mark tasks as completed
- 🔍 Filter tasks by status (completed/pending)
- 🌐 Deployed and accessible online

## Technology Stack

- **Backend Framework:** Django
- **API:** Django REST Framework
- **Database:** PostgreSQL
- **Authentication:** Token-based (DRF authtoken)
- **Deployment:** Render

## Getting Started

Follow these steps to run Tasktide locally.

### Prerequisites

- Python 3.11+
- pip
- git

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/oluwaseyipd/Tasktide.git
cd Tasktide
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the project root:

```env
DATABASE_URL="postgres://user:password@host:port/database_name"
SECRET_KEY="your-secret-key"
DEBUG=True
```

5. **Run migrations**

```bash
python manage.py migrate
```

6. **Start the development server**

```bash
python manage.py runserver
```

The API will now be accessible at: **http://127.0.0.1:8000/**

## API Endpoints

All endpoints are prefixed with `/api/`

### Authentication

#### Register a new user

- **URL:** `/api/users/register/`
- **Method:** `POST`
- **Request Body:**

```json
{
  "username": "testinguser",
  "password": "usertesting123",
  "confirm_password":"usertesting123"
}
```

- **Response:**

```json
{
  "username": "testinguser",
  "password": "usertesting123"
}
```

#### Login (Get Token)

- **URL:** `/api/users/login/`
- **Method:** `POST`
- **Request Body:**

```json
{
  "username": "testinguser",
  "password": "usertesting123"
}
```

- **Response:**

```json
{
  "token": "3a1f7e4c9d1a23..."
}
```

Use this token in **Postman/clients**:

```
Authorization: Token <your-token>
```

### Tasks

#### List all tasks / Create new task

- **URL:** `/api/tasks/`
- **Methods:** `GET`, `POST`

**POST Request Body:**

```json
{
  "title": "Document Tasktide",
  "description": "Write the README.md file."
}
```

**Response:**

```json
{
  "id": 1,
  "title": "Document Tasktide",
  "description": "Write the README.md file.",
  "completed": false,
  "created_at": "2025-08-26T10:00:00Z"
}
```

#### Retrieve, Update, or Delete a Task

- **URL:** `/api/tasks/<id>/`
- **Methods:** `GET`, `PUT`, `PATCH`, `DELETE`

**PATCH Request Body (mark as completed):**

```json
{
  "completed": true
}
```

**DELETE Response:** `204 No Content`

## Deployment

Tasktide is deployed on **Render** and accessible at: **https://tasktide-5bx6.onrender.com**

## Contributing

Contributions are welcome! 🚀

1. Fork the repo
2. Create a new branch (`git checkout -b feature-name`)
3. Commit changes (`git commit -m 'Add new feature'`)
4. Push to branch (`git push origin feature-name`)
5. Open a Pull Request

## License

This project is licensed under the **MIT License**.