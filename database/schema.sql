<<<<<<< HEAD
CREATE TABLE IF NOT EXISTS trainer (
    trainer_id INTEGER PRIMARY KEY AUTOINCREMENT,

    full_name TEXT NOT NULL,

    email TEXT NOT NULL UNIQUE,

    phone TEXT NOT NULL UNIQUE,

    skills TEXT NOT NULL,

    experience INTEGER NOT NULL CHECK (experience >= 0),

    status TEXT NOT NULL CHECK(status IN ('Active','Inactive')),

    availability TEXT NOT NULL CHECK(availability IN ('Available','Unavailable')),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
=======
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
>>>>>>> e8568112bbd6275753fba240fe45b17c67c21592
