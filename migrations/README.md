# Migrations

This folder contains SQL scripts to rebuild the current schema.

## Apply

Run these in order:

1) 001_create_schema.sql
2) 002_create_indexes.sql

Example (psql):
psql -U <user> -d <database> -f migrations\001_create_schema.sql
psql -U <user> -d <database> -f migrations\002_create_indexes.sql

Notes:
- These scripts assume an empty database.
- If tables already exist, drop them first or create a fresh database.
