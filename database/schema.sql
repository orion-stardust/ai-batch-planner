CREATE TABLE IF NOT EXISTS trainer (
    trainer_id INTEGER PRIMARY KEY AUTOINCREMENT,

    full_name TEXT NOT NULL,

    email TEXT NOT NULL UNIQUE,
aasxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    phone TEXT NOT NULL UNIQUE,

    skills TEXT NOT NULL,

    qualifications TEXT,

    experience INTEGER NOT NULL CHECK (experience >= 0),

    date_of_joining TEXT,

    previous_experience REAL NOT NULL DEFAULT 0.0 CHECK (previous_experience >= 0),

    status TEXT NOT NULL DEFAULT 'Active' CHECK(status IN ('Active','Inactive')),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    created_by TEXT,

    updated_by TEXT
);

CREATE TABLE IF NOT EXISTS Course (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    course_name TEXT NOT NULL UNIQUE,

    technology_stack TEXT NOT NULL,

    duration_hours INTEGER NOT NULL
        CHECK(duration_hours > 0),

    description TEXT,

    status TEXT NOT NULL DEFAULT 'Active'
        CHECK(status IN ('Active', 'Inactive')),

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    created_by TEXT,

    updated_by TEXT
);

CREATE INDEX IF NOT EXISTS idx_course_status
ON Course(status);

CREATE INDEX IF NOT EXISTS idx_course_technology_stack
ON Course(technology_stack);

CREATE TABLE IF NOT EXISTS trainer_availablity (
    availability_id INTEGER PRIMARY KEY AUTOINCREMENT,
    trainer_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    status INTEGER NOT NULL CHECK(status IN (0, 1)),
    availability_type TEXT NOT NULL CHECK(availability_type IN ('Available', 'Unavailable')),
    duration_type TEXT NOT NULL CHECK(duration_type IN ('Full Day', 'Half Day', 'Specific Slot')),
    time_slot TEXT,
    start_time TEXT,
    end_time TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    FOREIGN KEY (trainer_id) REFERENCES trainer(trainer_id) ON DELETE CASCADE,
    UNIQUE(trainer_id, date)
);

CREATE TABLE IF NOT EXISTS calendar_event (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL UNIQUE,
    event_type TEXT NOT NULL CHECK(event_type IN ('Public Holiday', 'Company Meeting')),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT
);
