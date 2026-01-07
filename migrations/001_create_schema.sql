BEGIN;

CREATE TABLE banks (
  bank_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  bank_code TEXT NOT NULL,
  bank_name TEXT NOT NULL,
  CONSTRAINT uq_bank_code UNIQUE (bank_code)
);

CREATE TABLE accounts (
  account_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  bank_id BIGINT NOT NULL,
  account_last4 TEXT NOT NULL,
  display_name TEXT,
  CONSTRAINT fk_accounts_bank FOREIGN KEY (bank_id) REFERENCES banks(bank_id),
  CONSTRAINT uq_accounts_bank_last4 UNIQUE (bank_id, account_last4)
);

CREATE TABLE merchants (
  merchant_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  merchant_name TEXT NOT NULL,
  CONSTRAINT uq_merchant_name UNIQUE (merchant_name)
);

CREATE TABLE categories (
  category_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  category_name TEXT NOT NULL,
  parent_id BIGINT,
  CONSTRAINT uq_category_name UNIQUE (category_name),
  CONSTRAINT fk_categories_parent FOREIGN KEY (parent_id) REFERENCES categories(category_id)
);

CREATE TABLE transactions (
  transaction_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  account_id BIGINT NOT NULL,
  transaction_date DATE NOT NULL,
  amount_cents INTEGER NOT NULL,
  description TEXT NOT NULL,
  transaction_type TEXT NOT NULL,
  source_filename TEXT NOT NULL,
  source_row_id INTEGER NOT NULL,
  possible_duplicate_key TEXT NOT NULL,

  posted_date DATE,
  category_id BIGINT,
  merchant_id BIGINT,
  raw_type TEXT,
  memo TEXT,
  address TEXT,
  reference_number TEXT,
  raw_metadata TEXT,

  CONSTRAINT fk_transactions_account
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
  CONSTRAINT fk_transactions_category
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
  CONSTRAINT fk_transactions_merchant
    FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id),
  CONSTRAINT uq_transactions_source
    UNIQUE (source_filename, source_row_id),
  CONSTRAINT chk_transactions_type
    CHECK (transaction_type IN (
      'purchase','payment','refund','transfer','fee','cash_withdrawal','interest','other'
    ))
);

COMMIT;
