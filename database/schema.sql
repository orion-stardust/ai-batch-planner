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