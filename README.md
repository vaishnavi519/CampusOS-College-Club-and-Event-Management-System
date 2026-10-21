<div align="center">

# CampusOS

### Campus Club & Event Management System

A full-stack web application for managing campus clubs, events, registrations, attendance, and notifications through role-based dashboards.

**Built with React · Vite · Django REST Framework · MySQL**

</div>

---

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Key Features](#key-features)
- [User Roles](#user-roles)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [API Overview](#api-overview)
- [Security and Configuration](#security-and-configuration)
- [Future Improvements](#future-improvements)
- [Project Repository](#project-repository)

## Overview

CampusOS is a centralized platform designed to simplify how college clubs and events are managed. It brings student-facing activities and administrative workflows into one application, reducing reliance on scattered spreadsheets, paper forms, and chat messages.

Students can discover clubs and events, register for events, track their registrations, and receive notifications. Club administrators can manage their events and review registrations and attendance. Faculty coordinators and system administrators have role-specific access to supported management workflows.

## Problem Statement

Campus clubs often coordinate events using multiple disconnected tools. This can make it difficult to keep participant records accurate, review registrations, track attendance, and communicate updates consistently.

CampusOS aims to provide one organized workflow for:

- Club and event information
- Role-based access to management features
- Event registration and cancellation
- Registration and attendance tracking
- In-app notifications
- Centralized backend data and APIs

## Key Features

### Student

- Browse available clubs and events.
- View event details.
- Register for events and view personal registrations.
- View club membership information and application status where available.
- Receive and review in-app notifications.
- Access a role-specific dashboard and profile.

### Club Administration

- Access club-management features permitted for the administrator's club.
- View events and event registrations.
- Review attendee information.
- Record and review attendance.
- Follow registration and attendance status through the application.

### Faculty Coordination and System Administration

- Role-specific access to the management workflows implemented in the application.
- Support for oversight and administrative tasks according to assigned permissions.

### Authentication and Access Control

- Login and registration workflows.
- JWT-based API authentication.
- Role-aware frontend routes and backend permissions.
- Password handling through the backend authentication implementation.

## User Roles

| Role | Intended Use |
|---|---|
| `STUDENT` | Discover clubs and events, register, and view personal information and notifications. |
| `CLUB_ADMIN` | Manage permitted club activities, registrations, and attendance. |
| `FACULTY_COORDINATOR` | Access faculty coordination workflows. |
| `SYSTEM_ADMIN` | Access platform administration workflows. |

Available actions depend on the user's role and the permissions enforced by the backend.

## Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | React, Vite, JavaScript, HTML, CSS |
| API Client | Axios |
| Backend | Python, Django, Django REST Framework |
| Database | MySQL |
| Authentication | JWT-based authentication |
| Testing | Django tests and standalone Python test scripts |
| Version Control | Git and GitHub |

## Project Structure

```text
CampusOS/
├── backend/
│   ├── accounts/
│   ├── attendance/
│   ├── campusos/
│   ├── clubs/
│   ├── events/
│   ├── notifications/
│   ├── recommendations/
│   ├── registrations/
│   ├── reports/
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   ├── .env
│   └── package.json
├── test_cases/
│   ├── test_campusos.py
│   ├── test_case_10.py
│   ├── test_login.py
│   ├── test_event_registration.py
│   └── ...
├── manage.py
├── models_existing.py
└── README.md
```

The project structure may change as development continues. Keep Django's app-level `tests.py` files in their original installed-app folders so Django's default test discovery can find them.

## Getting Started

### Prerequisites

Install the following before running the application:

- Python compatible with the project's installed Django dependencies
- Node.js and npm
- MySQL Server
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/vaishnavi519/CampusOS-College-Club-and-Event-Management-System.git
cd CampusOS-College-Club-and-Event-Management-System
```

### 2. Configure the Database and Environment

Configure the database connection using the settings defined in the backend. Make sure MySQL is running and the configured database exists.

If the project uses environment variables locally, create the required environment file(s) based on the project's settings.

**Never commit passwords, secret keys, access tokens, or production credentials.**

### 3. Set Up the Python Environment

From the project root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the backend dependencies using the dependency file provided by the project. If `backend/requirements.txt` exists, run:

```powershell
pip install -r .\backend\requirements.txt
```

If the requirements file is located elsewhere, use its actual path.

### 4. Apply Database Migrations

From the project root:

```powershell
$env:PYTHONPATH = "$PWD\backend"
python manage.py migrate
```

If the project uses a different database setup or migration workflow, follow the configuration in the repository.

## Running the Application

Run the backend and frontend in separate terminals.

### Terminal 1 — Django Backend

Open PowerShell and run:

```powershell
cd C:\Users\Lenovo\Desktop\CampusOS
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = "$PWD\backend"
python manage.py runserver
```

The development API server should be available at:

`http://127.0.0.1:8000/`

### Terminal 2 — React Frontend

Open a second PowerShell terminal:

```powershell
cd C:\Users\Lenovo\Desktop\CampusOS\frontend
npm install
npm run dev
```

Open the local URL printed by Vite, usually:

`http://localhost:5173/`

### Frontend API Configuration

The frontend API URL is configured in `frontend/.env`:

```env
VITE_API_URL=http://127.0.0.1:8000/api
```

Restart the Vite development server after changing frontend environment variables.

## Testing

CampusOS contains Django app tests and standalone test scripts in `test_cases/`.

### Run Django Tests

From the project root, with the virtual environment activated:

```powershell
$env:PYTHONPATH = "$PWD\backend"
python manage.py test
```

Django's automatic test discovery depends on tests being located in discoverable app and module paths. Keep the original app-level `tests.py` files in place.

### Run an Individual Standalone Test

Examples:

```powershell
python .\test_cases\test_login.py
python .\test_cases\test_event_registration.py
python .\test_cases\test_case_10.py
```

Some standalone scripts may require the frontend and backend to be running, a browser driver, or test credentials.

Run scripts individually and review their actual output. Report a test as passing only when it completes successfully.

## API Overview

The backend exposes REST endpoints under `/api/`. Examples of routes used by the application include:

| Area | Endpoint | Purpose |
|---|---|---|
| Authentication | `POST /api/auth/login` | Authenticate a user |
| Authentication | `POST /api/auth/register` | Register a user |
| Clubs | `GET /api/clubs` | List clubs |
| Events | `GET /api/events` | List events |
| Registrations | `GET /api/my-registrations` | View the current user's registrations |
| Event Registration | `POST /api/events/{event_id}/register` | Register for an event |
| Event Registrations | `GET /api/events/{event_id}/registrations` | View event registrations, subject to permissions |
| Attendance | `GET /api/events/{event_id}/attendance` | View attendance, subject to permissions |
| Notifications | `GET /api/notifications` | List the current user's notifications |

Requests that require authentication must include a valid access token.

The backend's URL configuration is the source of truth for the complete endpoint list and supported HTTP methods.

## Security and Configuration

- Keep local environment files and secrets out of Git.
- Do not place real user passwords or access tokens in the README.
- Use non-production test accounts for demonstrations.
- Do not expose the development server directly to the public internet.
- Backend permissions must enforce access control; frontend route guards alone are not sufficient.
- Review error messages and logs before sharing screenshots publicly.

## Future Improvements

Potential next steps include:

- Expand automated integration and end-to-end test coverage.
- Improve API error handling and validation.
- Add more reporting and export options where required.
- Improve accessibility and responsive layouts.
- Add continuous integration checks for formatting, tests, and build validation.
- Document deployment configuration and environment variables.

---

## Project Repository

**GitHub:** [CampusOS — Campus Club & Event Management System](https://github.com/vaishnavi519/CampusOS-College-Club-and-Event-Management-System)

---

<div align="center">

*CampusOS — bringing campus clubs, events, registrations, and attendance into one organized platform.*

</div>
