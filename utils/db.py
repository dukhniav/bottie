import sqlite3


class DB:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                balance REAL
            )
        """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER,
                symbol TEXT,
                quantity INTEGER,
                price REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_id) REFERENCES accounts (id)
            )
        """
        )
        self.conn.commit()

    def create_account(self, name, balance):
        self.cursor.execute(
            """
            INSERT INTO accounts (name, balance)
            VALUES (?, ?)
        """,
            (name, balance),
        )
        account_id = self.cursor.lastrowid
        self.conn.commit()
        return account_id

    def get_accounts(self):
        self.cursor.execute(
            """
            SELECT id, name, balance
            FROM accounts
        """
        )
        accounts = self.cursor.fetchall()
        return accounts

    def create_trade(self, account_id, symbol, quantity, price):
        self.cursor.execute(
            """
            INSERT INTO trades (account_id, symbol, quantity, price)
            VALUES (?, ?, ?, ?)
        """,
            (account_id, symbol, quantity, price),
        )
        trade_id = self.cursor.lastrowid
        self.conn.commit()
        return trade_id

    def get_trades(self, account_id):
        self.cursor.execute(
            """
            SELECT id, symbol, quantity, price, timestamp
            FROM trades
            WHERE account_id = ?
        """,
            (account_id,),
        )
        trades = self.cursor.fetchall()
        return trades

    def close(self):
        if self.conn:
            self.conn.close()
