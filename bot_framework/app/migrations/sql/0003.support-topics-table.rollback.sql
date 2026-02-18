-- Rollback 0003: Restore support columns to users, drop support_topics table

ALTER TABLE users ADD COLUMN IF NOT EXISTS support_chat_id INTEGER;
ALTER TABLE users ADD COLUMN IF NOT EXISTS support_topic_id INTEGER;

UPDATE users u
SET support_chat_id = st.chat_id,
    support_topic_id = st.topic_id
FROM support_topics st
WHERE u.id = st.user_id;

DROP TABLE IF EXISTS support_topics;

ALTER TABLE users DROP COLUMN IF EXISTS phone_number;
