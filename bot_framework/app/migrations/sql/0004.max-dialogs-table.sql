-- Migration 0004: Max dialogs table
-- Maps user_id to chat_id for Max platform,
-- because in Max personal dialog chat_id differs from user_id

CREATE TABLE IF NOT EXISTS max_dialogs (
    user_id BIGINT PRIMARY KEY,
    chat_id BIGINT NOT NULL
);
