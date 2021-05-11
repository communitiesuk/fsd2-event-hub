CREATE TABLE IF NOT EXISTS events (
    seq INTEGER PRIMARY KEY,
    type TEXT NOT NULL,
    data JSON NOT NULL
);
CREATE INDEX idx_type
ON events (type);
