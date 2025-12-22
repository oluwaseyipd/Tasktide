# TaskTide API

TaskTide is a modern, production-ready **Task Management API** built with **Django** and **Django REST Framework**. It provides secure, scalable endpoints for managing tasks and users, designed for seamless integration with any frontend (web, mobile, etc.).

---

## Features

- 🔑 **User Registration & Token Authentication**
- ✅ **CRUD Operations** for tasks
- 📌 **Mark tasks as completed**
- 🔍 **Filter, search, and order tasks**
- 🗂️ **Pagination** for scalable data access
- 🚦 **Rate limiting** for security and stability
- 🌍 **CORS support** for frontend integration
- 🛡️ **Production-grade security** (HTTPS, HSTS, secure cookies)
- 📝 **Interactive API documentation** (Swagger/OpenAPI)
- 🛠️ **Admin interface** for data management

---

## Technology Stack

- **Backend:** Django 5.x, Django REST Framework
- **Database:** PostgreSQL (recommended), SQLite/MySQL (dev/fallback)
- **Authentication:** Token-based (DRF authtoken)
- **Deployment:** Render.com (recommended), supports any cloud
- **Documentation:** drf-yasg (Swagger/OpenAPI)
- **Testing:** Automated with DRF’s APIClient

---

## Getting Started

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

The API will be accessible at: **http://127.0.0.1:8000/**

---

## API Documentation

Interactive docs available at:

- **Swagger UI:** `/swagger/`
- **ReDoc:** `/redoc/`

---

## API Endpoints

All endpoints are prefixed with `/api/`.

### Authentication

#### Register a new user

- **POST** `/api/users/register/`
    ```json
    {
      "username": "testinguser",
      "email": "testing@example.com",
      "password": "usertesting123"
    }
    ```
    **Response:**
    ```json
    {
      "user": {
        "username": "testinguser",
        "email": "testing@example.com"
      },
      "token": "26a4df6a68bef633f0ee66a1f7afd677291a41a2"
    }
    ```

#### Login (Get Token)

- **POST** `/api/users/login/`
    ```json
    {
      "username": "testinguser",
      "password": "usertesting123"
    }
    ```
    **Response:**
    ```json
    {
      "token": "3a1f7e4c9d1a23..."
    }
    ```

**Use this token in API requests:**
```
Authorization: Token <your-token>
```

---

### Tasks

#### List all tasks / Create new task

- **GET, POST** `/api/tasks/`
    - **POST Request Body:**
        ```json
        {
          "title": "Document TaskTide",
          "description": "Write the README.md file.",
          "priority": "medium"
        }
        ```
    - **Response:**
        ```json
        {
          "id": 1,
          "title": "Document TaskTide",
          "description": "Write the README.md file.",
          "priority": "medium",
          "completed": false,
          "created_at": "2025-08-26T10:00:00Z"
        }
        ```

#### Retrieve, Update, or Delete a Task

- **GET, PUT, PATCH, DELETE** `/api/tasks/<id>/`
    - **PATCH Request Body (mark as completed):**
        ```json
        {
          "completed": true
        }
        ```
    - **DELETE Response:** `204 No Content`

#### Filtering, Searching, Ordering, Pagination

- **Filter by status:** `/api/tasks/?completed=true`
- **Search by title/description:** `/api/tasks/?search=Document`
- **Order by due date:** `/api/tasks/?ordering=due_date`
- **Paginate:** `/api/tasks/?page=2`

---

## Deployment

TaskTide is production-ready and recommended for deployment on **Render.com**.

- **Managed PostgreSQL**
- **Automatic HTTPS**
- **Easy environment variable management**
- **Git-based CI/CD**

See [Render documentation](https://render.com/docs/deploy-django) for step-by-step deployment.

---

## Testing

Run automated tests with:

```bash
python manage.py test
```

---

## Contributing

Contributions are welcome! 🚀

1. Fork the repo
2. Create a new branch (`git checkout -b feature-name`)
3. Commit changes (`git commit -m 'Add new feature'`)
4. Push to branch (`git push origin feature-name`)
5. Open a Pull Request

---

## License

This project is licensed under the **MIT License**.

---