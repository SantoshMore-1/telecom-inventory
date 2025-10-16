CREATE TABLE nso_trunks (
    id SERIAL PRIMARY KEY,
    trunk_name VARCHAR(255) NOT NULL,
    channels_count INTEGER NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE nso_dids (
    id SERIAL PRIMARY KEY,
    did_number VARCHAR(50) NOT NULL UNIQUE,
    nso_trunk_id INTEGER REFERENCES nso_trunks(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'active'
);

CREATE TABLE customer_trunks (
    id SERIAL PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    trunk_name VARCHAR(255) NOT NULL,
    channels_count INTEGER NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE customer_dids (
    id SERIAL PRIMARY KEY,
    did_number VARCHAR(50) NOT NULL UNIQUE,
    customer_trunk_id INTEGER REFERENCES customer_trunks(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'active'
);

CREATE TABLE nso_to_vno_mappings (
    id SERIAL PRIMARY KEY,
    nso_trunk_id INTEGER REFERENCES nso_trunks(id) ON DELETE CASCADE,
    customer_trunk_id INTEGER REFERENCES customer_trunks(id) ON DELETE CASCADE,
    mapping_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(nso_trunk_id, customer_trunk_id)
);
