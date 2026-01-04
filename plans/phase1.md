# Phase 1: Canonical Data Model (Plan)

## Inputs Inventory
- Banks: Bank of America (BOA), Chase
- Formats:
  - BOA (monthly): `TransactionDate, Description, Category, Type, Amount`
  - Chase (activity): `Transaction Date, Post Date, Description, Category, Type, Amount, Memo`
  - Chase (monthly split): `Posted Date, Reference Number, Payee, Address, Amount`

## Core Decisions
- Signed amounts are canonical: negative = charge/spend, positive = refund/return/payment.
- Store amounts as integer cents (for exact arithmetic).
- Transaction date is canonical; posted date is secondary.
- Include both pending and posted transactions; no status field required.
- Transfers use category `Transfers`.
- Payments remain in the dataset (filter out as needed for spend-only views).
- Currency: USD only for now.
- Uniqueness: primary key auto id; unique constraint on `source_filename + source_row_id`.
- Required fields are required in the canonical model; if a source lacks them, set null and flag for cleanup.

## Canonical Field List
### Required
- transaction_date
- amount_signed
- description/payee
- source_bank
- account_last4
- transaction_type

### Also Included (user-specified)
- category
- merchant/payee
- posted_date
- source_month_year (derived)
- location (if available or parsed)

### Traceability & Lineage
- raw_type (original bank Type value)
- source_filename
- source_row_id

### Optional / Future
- memo
- address
- reference_number
- raw_metadata (unmapped source fields)

## Enum: transaction_type
- purchase
- payment
- refund
- transfer
- fee
- cash_withdrawal
- interest
- other

## Type Mapping Plan (Raw -> Canonical)
- Sale → purchase
- Payment → payment
- Fee → fee
- Refund → refund
- Return → refund
- Adjustment → other (review later)

## Filename Parsing Rules
- Extract `source_bank` and `account_last4` from filename patterns.
- Examples:
  - `BOA_2024_April_1371.csv` → bank=BOA, account_last4=1371
  - `2024_Chase1664_Activity20240101_20241126_20241127.CSV` → bank=Chase, account_last4=1664
- `source_month_year` is derived from filename or transaction_date.

## Data Dictionary (Template)
For each field: name, required/optional, type, definition, source, derivation, allowed values, null handling, edge cases, example (redacted).

## Synthetic Scenarios (Minimum)
- Refund / return (positive amount)
- Payment (positive amount)
- Transfer (category = Transfers)
- Missing category (set to Uncategorized)
- Format C without Type (requires parsing from Payee/Address)

## Phase 1 Done Checklist
- All supported formats map into the canonical fields.
- Each field has a documented definition and source rule.
- Type mapping rules are documented (including Adjustment).
- Filename parsing rules are documented and tested against known patterns.
