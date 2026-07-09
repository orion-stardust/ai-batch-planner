# Trainer Management Module Documentation

This document provides the complete Developer, User, and Technical documentation for the Trainer Management module, in accordance with the Phase 3 specifications.

---

## 1. Developer Documentation

### Module Overview
The Trainer Management module provides an interface and backend API for training administrators to register, view, update, search, filter, and delete trainer profiles. It forms the core of the batch planning ecosystem by mapping available trainer skill sets to planned courses.

### Folder Structure
```
ai-batch-planner/
│
├── database/
│   ├── batch_planner.db       # SQLite Database file
│   └── schema.sql             # DB Schema Definition
│
├── models/
│   └── trainer.py             # Data access layer, raw SQL queries
│
├── routes/
│   └── trainer_routes.py      # HTTP route endpoints (Controller layer)
│
├── services/
│   └── trainer_service.py     # Business logic & validation layer
│
├── templates/
│   ├── base.html              # Base layout template
│   ├── trainers.html          # Trainer List page
│   ├── trainer_details.html   # Trainer Details page
│   ├── trainer_form.html      # Add Trainer form
│   ├── edit_trainer.html      # Edit Trainer form
│   └── trainer_availability.html # Quick Availability Update form
│
└── app.py                     # Application entrypoint
```

### Route Descriptions
All routes are registered under the `/` blueprint prefix.

| Route | Method | Description |
|---|---|---|
| `/trainers` | `GET` | Renders list of all trainers. |
| `/trainers` | `POST` | Saves a newly created trainer profile. |
| `/trainers/new` | `GET` | Displays the Add Trainer form. |
| `/trainers/<id>` | `GET` | Renders detailed information of a single trainer. |
| `/trainers/<id>/edit` | `GET` | Displays the Edit Trainer form pre-populated with current values. |
| `/trainers/<id>/edit` | `POST` | Updates the trainer's attributes. |
| `/trainers/<id>/delete` | `POST` | Deletes the trainer profile. |
| `/trainers/search` | `GET` | Searches trainers using `keyword` query parameter. |
| `/trainers/filter` | `GET` | Filters trainers using `availability` and/or `status` parameters. |
| `/trainers/<id>/availability`| `GET` | Renders a simplified availability status update form. |
| `/trainers/<id>/availability`| `POST` | Saves availability updates specifically. |

### Service Descriptions (`services/trainer_service.py`)
- `_validate_trainer(...)`: Centralized validation rule checker for fields, phone digit lengths, and numerical constraints.
- `create_trainer(...)`: Validates and inserts a new trainer. Catches SQLite unique constraint errors to report user-friendly duplicates message.
- `update_trainer(...)`: Validates and updates trainer details.
- `delete_trainer(...)`: Deletes trainer record.
- `search_trainers(keyword)`: Searches for matching trainers.
- `filter_trainers(availability, status)`: Runs database queries filtering by criteria.
- `update_trainer_availability(trainer_id, availability)`: Updates availability state specifically.

### Model Descriptions (`models/trainer.py`)
- Exposes raw database CRUD functions using SQLite parameterized prepared statements:
  - `get_all_trainers()`
  - `get_trainer_by_id(trainer_id)`
  - `get_trainer_availability(trainer_id)`
  - `update_trainer(...)`
  - `update_trainer_availability(...)`
  - `delete_trainer(trainer_id)`
  - `search_trainers(keyword)`
  - `filter_trainers(availability, status)`

---

## 2. User Documentation

### Add Trainer
1. Click **Add Trainer** on the top menu/navigation link.
2. Fill out the fields:
   - **Full Name**: (e.g. `Jane Doe`)
   - **Email**: Unique email address (e.g. `jane.doe@example.com`)
   - **Phone**: Unique phone number (must contain between 7 to 15 digits)
   - **Skills**: List of technologies (e.g. `Python, SQL, Flask`)
   - **Experience**: Non-negative integer representing years of experience (e.g. `4`)
   - **Status**: Select `Active` or `Inactive`
   - **Availability**: Select `Available` or `Unavailable`
3. Click **Save Trainer**. You will see a success flash message.

### Edit Trainer
1. In the **Trainer Management** table list page, locate the trainer.
2. Click **Edit** in the Action column.
3. Modify the desired fields and click **Update Trainer**.

### View Trainer Details
1. Locate the trainer in the list.
2. Click **Details** in the Action column.
3. Review all information (including account creation/update timestamps).

### Delete Trainer
1. Click **Delete** next to the trainer in the list table.
2. Confirm the action when prompted by the browser confirmation dialog.

### Search and Filter
- **Search**: Enter text in the search input and click **Search**. The list will return trainers whose Name, Email, Phone, or Skills contain the keyword.
- **Filter**: Choose an option from the Availability and/or Status dropdown filters and click **Filter**.

---

## 3. Technical Documentation

### Database Structure
The SQLite database stores records in the `trainer` table:

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `trainer_id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | Auto-generated ID. |
| `full_name` | `TEXT` | `NOT NULL` | Trainer name. |
| `email` | `TEXT` | `NOT NULL UNIQUE` | Trainer email. |
| `phone` | `TEXT` | `NOT NULL UNIQUE` | Trainer phone. |
| `skills` | `TEXT` | `NOT NULL` | List of skills. |
| `experience` | `INTEGER` | `NOT NULL CHECK(experience >= 0)` | Experience in years. |
| `status` | `TEXT` | `NOT NULL CHECK(status IN ('Active','Inactive'))` | Employment status. |
| `availability`| `TEXT` | `NOT NULL CHECK(availability IN ('Available','Unavailable'))` | Availability status. |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Profile creation time. |
| `updated_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Profile last modified time. |

### Data Flow Architecture
The Trainer module employs a layered architecture:
```
[Browser View / HTML Form]
           │ (HTTP Requests: GET/POST)
           ▼
 [Controller Routes] (routes/trainer_routes.py)
           │ (Calls services with parsed fields)
           ▼
[Business Services] (services/trainer_service.py)
           │ (Validates input; handles exceptions)
           ▼
 [Database Models] (models/trainer.py)
           │ (Executes parameterized SQL queries)
           ▼
  [SQLite Database] (database/batch_planner.db)
```

### Module Dependencies
- **Runtime Environment**: Python 3.x
- **Web Framework**: Flask
- **Database Engine**: SQLite 3
- **CSS**: Vanilla Custom CSS
