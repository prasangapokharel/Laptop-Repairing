-- Seed Data for Initial Setup
-- Basic roles and device types for production initialization

-- Insert default roles
INSERT INTO roles (name, description) VALUES
    ('Admin', 'System administrator with full access'),
    ('Technician', 'Repair technician who handles device repairs'),
    ('Reception', 'Reception staff who handles customer service'),
    ('Accountant', 'Accountant who manages financial transactions'),
    ('Customer', 'Customer who uses the service')
ON CONFLICT (name) DO NOTHING;

-- Insert default device types
INSERT INTO device_types (name, description) VALUES
    ('Laptop', 'Laptop computers'),
    ('Desktop', 'Desktop computers'),
    ('Tablet', 'Tablet devices'),
    ('Smartphone', 'Smartphone devices')
ON CONFLICT (name) DO NOTHING;

-- Insert common brands
INSERT INTO brands (name) VALUES
    ('Apple'),
    ('Dell'),
    ('HP'),
    ('Lenovo'),
    ('Asus'),
    ('Acer'),
    ('Samsung'),
    ('Microsoft'),
    ('Toshiba'),
    ('Sony')
ON CONFLICT (name) DO NOTHING;

