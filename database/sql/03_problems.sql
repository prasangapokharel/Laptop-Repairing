-- Problem Definitions and Cost Settings
-- Device type based problem definitions with cost configurations

CREATE TABLE IF NOT EXISTS problems (
    id BIGSERIAL PRIMARY KEY,
    device_type_id BIGINT NOT NULL REFERENCES device_types(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(device_type_id, name)
);

CREATE INDEX idx_problems_type ON problems(device_type_id);
CREATE INDEX idx_problems_name ON problems(name);

CREATE TABLE IF NOT EXISTS cost_settings (
    id BIGSERIAL PRIMARY KEY,
    problem_id BIGINT NOT NULL REFERENCES problems(id) ON DELETE CASCADE,
    base_cost DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    min_cost DECIMAL(10, 2),
    max_cost DECIMAL(10, 2),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_cost_settings_problem ON cost_settings(problem_id);
CREATE INDEX idx_cost_settings_active ON cost_settings(is_active);

