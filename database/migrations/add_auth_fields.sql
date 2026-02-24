-- Migration: Add authentication fields to users table
-- Date: 2026-02-20

-- Add password hash column
ALTER TABLE users ADD COLUMN password_hash TEXT;

-- Add OAuth provider column
ALTER TABLE users ADD COLUMN oauth_provider TEXT CHECK (oauth_provider IN ('google', 'github', 'email', NULL));

-- Add OAuth provider user ID column
ALTER TABLE users ADD COLUMN oauth_provider_id TEXT;

-- Add last login timestamp
ALTER TABLE users ADD COLUMN last_login DATETIME;

-- Add is_active column for account status
ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT 1;

-- Add email_verified column for OAuth users
ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT 0;

-- Create index on oauth provider + provider ID for OAuth lookups
CREATE INDEX IF NOT EXISTS idx_users_oauth ON users(oauth_provider, oauth_provider_id);

-- Create index on email for login lookups
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Log migration completion
INSERT INTO audit_log (module, action, entity_type, entity_id, metadata)
VALUES ('system', 'migration', 'users_table', 'add_auth_fields', '{"version": "1.0"}');
