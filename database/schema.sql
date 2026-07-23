CREATE TABLE IF NOT EXISTS trainer (
    trainer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
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

CREATE TABLE IF NOT EXISTS student (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT NOT NULL UNIQUE,
    qualification TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT
);

CREATE TABLE IF NOT EXISTS Course (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT NOT NULL UNIQUE,
    technology_stack TEXT NOT NULL,
    duration_hours INTEGER NOT NULL CHECK(duration_hours > 0),
    description TEXT,
    status TEXT NOT NULL DEFAULT 'Active' CHECK(status IN ('Active', 'Inactive')),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT
);

CREATE INDEX IF NOT EXISTS idx_course_status ON Course(status);
CREATE INDEX IF NOT EXISTS idx_course_technology_stack ON Course(technology_stack);

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

CREATE TABLE IF NOT EXISTS batch (
    batch_id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_code TEXT NOT NULL UNIQUE,
    batch_name TEXT NOT NULL,
    course_id INTEGER NOT NULL,
    trainer_id INTEGER,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    slot_type TEXT NOT NULL CHECK(slot_type IN (
        'Weekday Morning (9:30 AM - 11:30 AM)',
        'Weekday Midday (11:45 AM - 1:45 PM)',
        'Weekday Afternoon (2:45 PM - 4:45 PM)',
        'Weekday Evening (5:00 PM - 7:00 PM)',
        'Weekend Full Day (10:00 AM - 4:00 PM)',
        'Custom'
    )),
    start_time TEXT,
    end_time TEXT,
    mode TEXT NOT NULL DEFAULT 'Offline' CHECK(mode IN ('Online', 'Offline', 'Hybrid')),
    location TEXT,
    max_capacity INTEGER NOT NULL DEFAULT 30 CHECK(max_capacity > 0),
    enrolled_count INTEGER NOT NULL DEFAULT 0 CHECK(enrolled_count >= 0),
    status TEXT NOT NULL DEFAULT 'Upcoming' CHECK(status IN ('Upcoming', 'In Progress', 'Completed', 'On Hold', 'Cancelled')),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    FOREIGN KEY (course_id) REFERENCES Course(id) ON DELETE RESTRICT,
    FOREIGN KEY (trainer_id) REFERENCES trainer(trainer_id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_batch_status ON batch(status);
CREATE INDEX IF NOT EXISTS idx_batch_course ON batch(course_id);
CREATE INDEX IF NOT EXISTS idx_batch_trainer ON batch(trainer_id);
CREATE INDEX IF NOT EXISTS idx_batch_dates ON batch(start_date, end_date);

CREATE TABLE IF NOT EXISTS student_register (
    register_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    batch_id INTEGER,
    enrollment_date TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('registered', 'registed', 'assigned', 'discontinued', 'break', 'completed', 'hold')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT DEFAULT 'Admin',
    updated_by TEXT DEFAULT 'Admin',
    FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES Course(id) ON DELETE CASCADE,
    FOREIGN KEY (batch_id) REFERENCES batch(batch_id) ON DELETE SET NULL
);
