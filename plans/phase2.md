# Phase 2: Database Schema + Ingestion Plan

## Goals
- Translate the Phase 1 canonical model into a normalized database schema.
- Define keys, relationships, and constraints.
- Document field mappings from each input format.

## Schema Outline (Normalized)
### banks
- Purpose: Canonical list of banks/institutions.
- Key fields: bank_id (PK), bank_name/code (unique).

### accounts
- Purpose: Accounts tied to banks.
- Key fields: account_id (PK), bank_id (FK), account_last4, display_name (optional).
- Constraints: unique on (bank_id, account_last4).

### merchants
- Purpose: Canonical merchant/payee list.
- Key fields: merchant_id (PK), merchant_name (unique).

### categories
- Purpose: Canonical category list.
- Key fields: category_id (PK), category_name (unique), parent_id (optional).

### transactions
- Purpose: Canonical transaction facts.
- Key fields: transaction_id (PK), account_id (FK), merchant_id (FK, nullable), category_id (FK, nullable).
- Core fields: transaction_date, posted_date (nullable), amount_cents, description, transaction_type, raw_type (nullable).
- Lineage: source_filename, source_row_id, source_month_year (derived), raw_metadata (optional).
- Constraints: unique on (source_filename, source_row_id).

## Field Types & Rules (High-Level)
- Dates: store as datetime.
- Amount: integer cents (signed).
- Text fields: unbounded text (SQLite TEXT).
- Enums: transaction_type limited to the defined list.
- Nulls: allow null when a source format lacks the data.

## Mapping Plan (Per Format)
### BOA (monthly)
- Map TransactionDate → transaction_date
- Description → description
- Category → category (lookup/insert into categories)
- Type → raw_type + transaction_type mapping
- Amount → amount_cents (signed)
- Filename → source_filename, source_bank, account_last4

### Chase (activity)
- Transaction Date → transaction_date
- Post Date → posted_date
- Description → description
- Category → category (lookup/insert into categories)
- Type → raw_type + transaction_type mapping
- Amount → amount_cents (signed)
- Memo → raw_metadata (or memo field)
- Filename → source_filename, source_bank, account_last4

### Chase (monthly split)
- Posted Date → transaction_date + posted_date (if no separate transaction date)
- Payee → description/merchant candidate
- Address → location (optional)
- Reference Number → reference_number (optional)
- Amount → amount_cents (signed)
- Type → derive transaction_type from payee/keywords (no raw Type field)
- Filename → source_filename, source_bank, account_last4

## Canonical Lookups
- merchants: insert new merchant names as needed; map from description/payee normalization.
- categories: insert new categories as needed; default to "Uncategorized" when missing.

## Ingestion Checklist (No Code)
- Define the create-table plan based on the schema outline.
- Decide how to normalize merchant names (initially simple; refine later).
- Decide whether to store raw_metadata as a JSON-like text blob.
- Validate that all inputs can map without losing required fields.

## Phase 2 Done Checklist
- Schema outline agreed and documented.
- Field types and nullability defined.
- Mapping rules for all input formats documented.
- Uniqueness + FK relationships defined.
