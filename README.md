
# KudoSphere - Kudos App Backend

## Overview

The **Kudos App** backend is a Django REST Framework (DRF) based service that allows team members to send and receive kudos within an organization. It supports authentication, user management, kudos exchange, and provides API endpoints for integration with the frontend.

---

## Requirements

- Python (3.10+ recommended)
- Virtual Environment Tool (e.g., `venv` or `virtualenv`)
- Git
- VS Code (or any code editor)

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd backend
```

### 2. Create and Activate Virtual Environment (Optional)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create SuperUser - for accessing admin panel (Optional)

```bash
python manage.py createsuperuser
```

### 5. Load Initial Fixtures (Optional)

```bash
python manage.py generate_fixtures
```

### 6. Start the Development Server

```bash
python manage.py runserver
```

Your backend server should now be live at `http://localhost:8000/`.

---

## Core Features

- JWT Authentication using DRF Simple JWT
- Kudos: Give and receive kudos between users
- User Management: Profile data including username, organization, etc.
- Kudos Summary API
- Admin Panel for managing users and kudos

---

## API Endpoints

> ⚠️ **Note:** All endpoints listed below **require JWT authentication** using the `Authorization: Bearer <token>` header, **except** for `/api/auth/login/`, which is used to obtain the token.

```http
Authorization: Bearer your_jwt_token_here
```

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/login/` | POST | Login with JWT Token |
| `/api/me/` | GET | Current User |
| `/api/users/` | GET | Get all users (same organization) |
| `/api/kudos/give/` | POST | Give kudos to a user |
| `/api/kudos/summary/` | GET | View kudos given and received |
| `/api/kudos/remaining/` | GET | View remaining kudos count |

---

## Frontend Repository

To access and set up the frontend, please refer to the [Kudos Frontend Repository](https://github.com/iamvishalaggarwal/kudos_frontend).
