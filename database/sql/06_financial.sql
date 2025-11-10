-- Financial Tracking Tables
-- Income and expense management for office activities

CREATE TABLE IF NOT EXISTS income (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT REFERENCES orders(id) ON DELETE SET NULL,
    amount DECIMAL(10, 2) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    created_by BIGINT REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_income_order ON income(order_id);
CREATE INDEX idx_income_created ON income(created_at);
CREATE INDEX idx_income_category ON income(category);

CREATE TABLE IF NOT EXISTS expenses (
    id BIGSERIAL PRIMARY KEY,
    amount DECIMAL(10, 2) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    created_by BIGINT REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_expenses_created ON expenses(created_at);
CREATE INDEX idx_expenses_category ON expenses(category);
CREATE INDEX idx_expenses_created_by ON expenses(created_by);

