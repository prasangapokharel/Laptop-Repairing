-- Device Management Tables
-- Normalized structure for brands, models, types, and devices

CREATE TABLE IF NOT EXISTS device_types (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_device_types_name ON device_types(name);

CREATE TABLE IF NOT EXISTS brands (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_brands_name ON brands(name);

CREATE TABLE IF NOT EXISTS models (
    id BIGSERIAL PRIMARY KEY,
    brand_id BIGINT NOT NULL REFERENCES brands(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    device_type_id BIGINT NOT NULL REFERENCES device_types(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(brand_id, name, device_type_id)
);

CREATE INDEX idx_models_brand ON models(brand_id);
CREATE INDEX idx_models_type ON models(device_type_id);
CREATE INDEX idx_models_name ON models(name);

CREATE TABLE IF NOT EXISTS devices (
    id BIGSERIAL PRIMARY KEY,
    brand_id BIGINT NOT NULL REFERENCES brands(id) ON DELETE RESTRICT,
    model_id BIGINT NOT NULL REFERENCES models(id) ON DELETE RESTRICT,
    device_type_id BIGINT NOT NULL REFERENCES device_types(id) ON DELETE RESTRICT,
    serial_number VARCHAR(100) UNIQUE,
    owner_id BIGINT REFERENCES users(id) ON DELETE SET NULL,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_devices_brand ON devices(brand_id);
CREATE INDEX idx_devices_model ON devices(model_id);
CREATE INDEX idx_devices_type ON devices(device_type_id);
CREATE INDEX idx_devices_owner ON devices(owner_id);
CREATE INDEX idx_devices_serial ON devices(serial_number);

