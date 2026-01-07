BEGIN;

CREATE INDEX idx_transactions_date ON transactions (transaction_date);
CREATE INDEX idx_transactions_account ON transactions (account_id);
CREATE INDEX idx_transactions_dupkey ON transactions (possible_duplicate_key);

COMMIT;
