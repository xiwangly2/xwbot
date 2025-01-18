-- Setting UTF-8 encoding for the session
SET client_encoding = 'UTF8';

-- Drop and create the `logs` table
DROP TABLE IF EXISTS logs;
CREATE TABLE logs (
    id BIGSERIAL PRIMARY KEY,
    json JSONB NOT NULL,
    time TIMESTAMP NOT NULL
);

-- Drop and create the `switch` table
DROP TABLE IF EXISTS switch;
CREATE TABLE switch (
    group_id INTEGER PRIMARY KEY,
    switch VARCHAR(255) NOT NULL,
    time TIMESTAMP NOT NULL
);

-- Insert data into the `switch` table
INSERT INTO switch (group_id, switch, time)
VALUES (0, '1', '2023-09-05 11:05:40');
