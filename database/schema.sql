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