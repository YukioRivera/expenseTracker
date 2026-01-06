# Schema Spec (Draft)

Purpose: define the canonical database schema for the expense tracker, including field types, nullability, and constraints. This is a logical spec (DB-agnostic) and can be mapped to a concrete database later.

## Global Rules
- Required fields must be present; missing required fields should be rejected and logged during ingestion.
- Optional fields may be NULL.
- Amounts are stored as signed integer cents (negative = spend, positive = refund/return/payment).
- `source_month_year` is derived from `transaction_date` and is not stored.
- `possible_duplicate_key` is stored for review only (no auto-dedupe).

## Enums
`transaction_type`:
- purchase
- payment
- refund
- transfer
- fee
- cash_withdrawal
- interest
- other

## Tables

### banks
Purpose: canonical list of banks/institutions.

Fields:
- bank_id (PK, integer)
- bank_code (string, required, unique)  
  Example values: BOA, Chase
- bank_name (string, required)

Constraints:
- unique(bank_code)

### accounts
Purpose: bank accounts tied to institutions.

Fields:
- account_id (PK, integer)
- bank_id (FK → banks.bank_id, required)
- account_last4 (string, required)
- display_name (string, optional)

Constraints:
- unique(bank_id, account_last4)

### merchants
Purpose: canonical merchant/payee list for later normalization.

Fields:
- merchant_id (PK, integer)
- merchant_name (string, required, unique)

### categories
Purpose: canonical category list.

Fields:
- category_id (PK, integer)
- category_name (string, required, unique)
- parent_id (FK → categories.category_id, optional)

### transactions
Purpose: canonical transaction facts (the main table).

Required fields:
- transaction_id (PK, integer)
- account_id (FK → accounts.account_id)
- transaction_date (date)
- amount_cents (integer, signed)
- description (string)
- transaction_type (enum)
- source_filename (string)
- source_row_id (integer)
- possible_duplicate_key (string)

Optional fields:
- posted_date (date)
- category_id (FK → categories.category_id)
- merchant_id (FK → merchants.merchant_id)
- raw_type (string)
- memo (string)
- address (string)
- reference_number (string)
- raw_metadata (string, optional JSON-like text blob)

Constraints:
- unique(source_filename, source_row_id)

Notes:
- `account_id` implies `source_bank` and `account_last4` via the accounts table.
- `possible_duplicate_key` should be a stable grouping key such as:
  bank_code + account_last4 + transaction_date + amount_cents + normalized_description.
  It is for review only and should not be enforced as unique.

## Ingestion Mapping (Summary)
- BOA raw format (Posted Date, Reference Number, Payee, Address, Amount) maps to:
  transaction_date = Posted Date
  description = Payee
  address = Address
  reference_number = Reference Number
  amount_cents = Amount
- Chase activity format maps to:
  transaction_date = Transaction Date
  posted_date = Post Date
  description = Description
  category = Category
  raw_type = Type
  amount_cents = Amount
  memo = Memo

## Validation Rules (Minimum)
- Required fields present and non-empty.
- amount_cents parses to integer.
- transaction_date parses to a valid date.
- account_id must resolve from (bank_code, account_last4) derived from filename or context.
