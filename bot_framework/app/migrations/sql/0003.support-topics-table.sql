-- Migration 0003: Support topics table
-- Move support topic tracking from users to dedicated table,
-- add phone_number to users

CREATE TABLE IF NOT EXISTS support_topics (
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    chat_id BIGINT NOT NULL,
    topic_id INTEGER NOT NULL,
    UNIQUE(user_id, chat_id)
);

ALTER TABLE users ADD COLUMN IF NOT EXISTS phone_number VARCHAR(20);

INSERT INTO support_topics (user_id, chat_id, topic_id)
SELECT id, support_chat_id, support_topic_id
FROM users
WHERE support_chat_id IS NOT NULL AND support_topic_id IS NOT NULL;

ALTER TABLE users DROP COLUMN IF EXISTS support_chat_id;
ALTER TABLE users DROP COLUMN IF EXISTS support_topic_id;
