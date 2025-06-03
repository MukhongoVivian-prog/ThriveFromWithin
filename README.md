# Thrive From Within 🌱  
A Django-based mental health and wellness platform for organizations, therapists, and employees.

---

## 🚀 Project Overview

**Thrive From Within** is a modular mental health and employee wellness platform built with Django REST Framework.  
It offers personalized dashboards, virtual support tools, journaling, therapist interaction, learning resources, and global wellness benefit comparisons.

---

## 🧱 Project Architecture

| App Name          | Responsibility                                                                 |
|-------------------|--------------------------------------------------------------------------------|
| `core`            | User authentication (JWT), role management (Admin, Employee, Therapist, Manager) |
| `mental_health`   | Mood tracking, therapy session logging, therapist notes                         |
| `learning`        | Mental health courses and progress tracking                                    |
| `saferoom`        | Anonymous group support room (safe communication)                              |
| `wellness`        | Breathing, meditation, motivational quotes, private journaling                 |
| `benefits`        | Compare wellness programs across global companies                              |
| `community`       | (Optional) User discussion, shared experiences, mental health forums           |

---

## 🧑‍💼 Roles & Permissions

| Role            | Permissions Summary                                                                 |
|-----------------|--------------------------------------------------------------------------------------|
| `Admin`         | Full access — can manage all users, data, and dashboards                            |
| `CompanyManager`| View reports, track employee wellness, schedule programs                            |
| `Employee`      | Access wellness tools, journal, request therapy sessions                            |
| `Therapist`     | Manage client sessions, submit reports, chat anonymously                           |

Implemented via `IsAdminUser`, `IsCompanyManager`, `IsEmployee`, and `IsTherapist` custom permissions.

---

## 🔐 Authentication

- JWT-based authentication (`/api/core/login/`, `/api/core/register/`)
- Token contains user role info.
- Swagger Auth supported.

---

## 📘 API Endpoints Summary

### Core (`/api/core/`)
- `POST /register/` — Register a user
- `POST /login/` — Get JWT token
- `GET /profile/` — View your profile

### Mental Health (`/api/mental-health/`)
- `GET/POST /mood-checkins/` — Track emotional state
- `GET/POST /therapy-sessions/` — Log and manage therapy
- `GET/POST /therapist-notes/` — Therapist reports

### Learning (`/api/learning/`)
- `GET/POST /courses/` — Add/view courses
- `POST /enrollments/` — Enroll in course
- `GET /progress/` — See learning progress

### Saferoom (`/api/saferoom/`)
- `GET/POST /safe-messages/` — Anonymous messages
- `GET /safe-threads/` — Topic-based rooms

### Wellness (`/api/wellness/`)
- `GET/POST /meditations/` — Audio guides
- `GET/POST /breathing-exercises/` — Guided breathing
- `GET/POST /quotes/` — Motivational quotes
- `GET/POST /journal-entries/` — Private employee journaling

### Benefits (`/api/benefits/`)
- `GET/POST /companies/` — Company profiles
- `GET/POST /benefits/` — Wellness packages
- `GET /compare/` — Cross-company benefit comparison

---

## 📦 Tech Stack

- **Backend:** Django, Django REST Framework
- **Auth:** JWT (djangorestframework-simplejwt)
- **Docs:** Swagger UI (drf-yasg)
- **Filtering/Search:** django-filter
- **Database:** SQLite (can swap with PostgreSQL or MySQL)

---

## ⚙️ Setup Instructions

```bash
# Clone repository
git clone https://github.com/yourusername/thrive-from-within.git
cd thrive-from-within

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Start server
python manage.py runserver

#  Features Implemented
#### Modular apps
#### JWT auth & role-based access
#### Employee journaling
#### Therapist management
#### Anonymous peer chat
#### Wellness exercises
#### Course enrollment & tracking
#### Global benefit comparison
#### Swagger API docs

# Folder Structure
thrive/
│
├── core/               # Authentication and roles
├── mental_health/      # Mood tracking, therapy sessions
├── learning/           # Courses, progress, enrollment
├── saferoom/           # Anonymous support
├── wellness/           # Journals, meditations, breathing
├── benefits/           # Company benefits and comparisons
├── community/          # Optional (forums, discussions)
├── thrive/             # Project settings
├── requirements.txt
├── manage.py
└── README.md

# 🧑‍💻 Contributing
Want to help improve mental health through tech? Contributions are welcome — just fork and PR.
# 📜 License
MIT License. Free to use and modify with credit.

