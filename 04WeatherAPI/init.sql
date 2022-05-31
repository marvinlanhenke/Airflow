\c dev;

SET TIMEZONE TO 'GMT-2';

CREATE TABLE weather_data(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    region VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    last_updated TIMESTAMP NOT NULL,
    temp_c FLOAT(2) NOT NULL,
    temp_f FLOAT(2) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);