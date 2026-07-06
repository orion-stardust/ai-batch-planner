
# 🤖 AI Batch Planner

> **AI-powered Training Institute Management Platform**

AI Batch Planner is a full-stack Training Institute Management System built with **Flask**, **SQLite3**, **HTML**, **CSS**, **JavaScript**, and **OpenAI API**. It helps training institutes manage trainers, students, courses, batches, attendance, assessments, reviews, scheduling, reporting, and AI-assisted planning.

---

# Table of Contents

1. Overview
2. Features
3. Technology Stack
4. Architecture
5. Project Structure
6. Folder Responsibilities
7. Request Flow
8. Getting Started
9. Roadmap
10. Future Enhancements
11. Contributing
12. License

---

# Features

## Administration
- Dashboard
- Authentication (Planned)
- Role-based Access (Planned)

## Trainer Management
- Add/Edit/Delete Trainer
- Skills
- Experience
- Availability
- Leave Management
- Workload

## Course Management
- Course CRUD
- Duration
- Technology Stack
- Batch Mapping

## Student Management
- Student CRUD
- Enrollment
- Batch Assignment
- Progress Tracking

## Batch Management
- Create Batch
- Assign Course
- Assign Trainer
- Schedule Start/End Dates
- Batch Status

## Attendance
- Daily Attendance
- Monthly Reports

## Assessments
- Marks
- Performance

## Reviews
- Student Reviews
- Trainer Reviews
- Batch Feedback

## Reports
- Trainer Utilization
- Batch Report
- Attendance Report
- Course Report

## AI
- Trainer Recommendation
- Batch Planning
- Availability Prediction
- Natural Language Queries
- AI Schedule Explanation

---

# Technology Stack

| Layer | Technology |
|---|---|
| Backend | Flask |
| Database | SQLite3 |
| Frontend | HTML + CSS + JavaScript |
| AI | OpenAI API |
| Version Control | Git |

---

# Architecture

```
Browser
    │
HTML/CSS/JavaScript
    │
Routes (Controllers)
    │
Services (Business Logic)
    ├──────────────┐
    ▼              ▼
Models         AI Modules
    │              │
SQLite       OpenAI API
```

---

# Project Structure

```text
ai-batch-planner/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── database/
│   ├── batch_planner.db
│   ├── db.py
│   └── schema.sql
│
├── models/
│   ├── trainer.py
│   ├── course.py
│   ├── student.py
│   ├── batch.py
│   ├── attendance.py
│   ├── assessment.py
│   └── review.py
│
├── routes/
│   ├── trainer_routes.py
│   ├── course_routes.py
│   ├── student_routes.py
│   ├── batch_routes.py
│   ├── attendance_routes.py
│   ├── assessment_routes.py
│   ├── review_routes.py
│   └── dashboard_routes.py
│
├── services/
│   ├── trainer_service.py
│   ├── course_service.py
│   ├── student_service.py
│   ├── batch_service.py
│   ├── attendance_service.py
│   ├── assessment_service.py
│   ├── review_service.py
│   ├── scheduling_service.py
│   └── report_service.py
│
├── ai/
│   ├── openai_client.py
│   ├── trainer_recommender.py
│   ├── batch_planner.py
│   ├── availability_predictor.py
│   ├── prompt_loader.py
│   └── prompts/
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   ├── trainers.html
│   ├── trainer_form.html
│   ├── courses.html
│   ├── course_form.html
│   ├── students.html
│   ├── student_form.html
│   ├── batches.html
│   ├── batch_form.html
│   ├── attendance.html
│   ├── assessments.html
│   ├── reviews.html
│   ├── reports.html
│   ├── login.html
│   └── 404.html
│
├── static/
│   ├── css/
│   │   ├── style.css
│   │   ├── dashboard.css
│   │   ├── forms.css
│   │   └── tables.css
│   ├── js/
│   │   ├── dashboard.js
│   │   ├── trainer.js
│   │   ├── course.js
│   │   ├── student.js
│   │   ├── batch.js
│   │   ├── attendance.js
│   │   ├── assessment.js
│   │   ├── review.js
│   │   └── common.js
│   ├── images/
│   └── icons/
│
├── docs/
├── data/
└── tests/
```

---

# Folder Responsibilities

## app.py
Starts Flask, loads configuration, registers Blueprints.

## database/
Only database initialization, schema and SQLite connection.

## models/
**Only data access.**
- SQL
- CRUD
- Queries

Never:
- HTML
- AI
- Business rules

## routes/
Receives browser requests.
- GET/POST
- Read form data
- Call services
- Return HTML/JSON

Never:
- SQL
- Scheduling
- AI prompts

## services/
Business logic.
- Validation
- Scheduling
- Availability
- Trainer allocation
- Reports
- Coordinates Models and AI

## ai/
Everything related to OpenAI.
- Prompt templates
- Client
- Recommendations
- Predictions

## templates/
All Jinja2 HTML templates.
Contains pages such as:
- dashboard.html
- trainers.html
- courses.html
- students.html
- batches.html
- attendance.html
- assessments.html
- reviews.html
- reports.html

## static/css
Stylesheets.

## static/js
Client-side JavaScript.
- Form validation
- Fetch API
- Dynamic UI

## docs
Architecture, API, ER diagrams.

## data
Sample Excel/CSV/JSON files.

## tests
Unit and integration tests.

---

# Request Flow

```
Browser
   ↓
Routes
   ↓
Services
   ↓
Models
   ↓
SQLite
```

AI requests:

```
Browser
 ↓
Routes
 ↓
Services
 ↓
AI
 ↓
OpenAI
```

---

# Getting Started

```bash
git clone https://github.com/<your-username>/ai-batch-planner.git
cd ai-batch-planner

python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt

python app.py
```

Visit http://127.0.0.1:5000

---

# Roadmap

- Phase 1: CRUD modules
- Phase 2: Scheduling & Reports
- Phase 3: AI Planning & Recommendations
- Phase 4: Notifications & Deployment

---

# Future Enhancements

- PostgreSQL
- Docker
- REST API
- Mobile App
- Multi-campus
- Calendar Integration
- Email Notifications

---

# Contributing

Fork the repository, create a feature branch, commit changes, and submit a Pull Request.

---

# License

MIT License

---

# Author

**Ezad, Buvanesh & Sankar**
