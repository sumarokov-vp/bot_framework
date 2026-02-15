-- depends: 0001.initial-schema

-- Базовые языки
INSERT INTO languages (code, name, native_name) VALUES
    ('en', 'English', 'English'),
    ('ru', 'Russian', 'Русский')
ON CONFLICT (code) DO NOTHING;

-- Роли загружаются через RoleLoader из roles.json
