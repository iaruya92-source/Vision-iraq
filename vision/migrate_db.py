#!/usr/bin/env python3
"""Migration script for Vision Platform DB schema update."""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'instance', 'vision.db')

def column_exists(cursor, table, column):
    cursor.execute(f"PRAGMA table_info({table})")
    return any(row[1] == column for row in cursor.fetchall())

def migrate():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Users table columns
    user_cols = [
        ("user_type", "TEXT DEFAULT 'user'"),
        ("user_title", "TEXT"),
        ("subscription_status", "TEXT DEFAULT 'trial'"),
        ("subscription_expiry", "TIMESTAMP"),
        ("trial_end", "TIMESTAMP"),
        ("subscription_price", "INTEGER DEFAULT 0"),
        ("is_premium", "INTEGER DEFAULT 0"),
        ("posting_scope", "TEXT DEFAULT 'full_platform'"),
        ("grace_period_end", "TIMESTAMP"),
        ("show_in_all", "INTEGER DEFAULT 0"),
        ("is_active_account", "INTEGER DEFAULT 1"),
    ]
    for col, dtype in user_cols:
        if not column_exists(cursor, "users", col):
            cursor.execute(f"ALTER TABLE users ADD COLUMN {col} {dtype}")
            print(f"Added column '{col}' to 'users'")
        else:
            print(f"Column '{col}' already exists in 'users'")

    # Listings table columns
    listing_cols = [
        ("status", "TEXT DEFAULT 'active'"),
        ("price", "INTEGER DEFAULT 0"),
        ("plan_type", "TEXT"),
        ("car_type", "VARCHAR(50)"),
        ("car_year", "INTEGER"),
        ("car_mileage", "INTEGER"),
        ("car_fuel", "VARCHAR(20)"),
        ("car_transmission", "VARCHAR(20)"),
        ("cooling_type", "VARCHAR(50)"),
        ("cooling_capacity", "VARCHAR(50)"),
        ("cooling_brand", "VARCHAR(100)"),
        ("cooling_service_type", "VARCHAR(50)"),
        ("appliance_type", "VARCHAR(50)"),
        ("appliance_brand", "VARCHAR(100)"),
        ("appliance_condition", "VARCHAR(20)"),
        ("appliance_warranty", "VARCHAR(100)"),
        ("featured_until", "DATETIME"),
        ("featured_price_paid", "FLOAT DEFAULT 0"),
        ("featured_by_admin", "BOOLEAN DEFAULT 0"),
    ]

    # Categories table columns
    category_cols = [
        ("subscription_price", "INTEGER DEFAULT 0"),
        ("is_premium", "INTEGER DEFAULT 0"),
    ]
    for col, dtype in listing_cols:
        if not column_exists(cursor, "listings", col):
            cursor.execute(f"ALTER TABLE listings ADD COLUMN {col} {dtype}")
            print(f"Added column '{col}' to 'listings'")
        else:
            print(f"Column '{col}' already exists in 'listings'")

    for col, dtype in category_cols:
        if not column_exists(cursor, "categories", col):
            cursor.execute(f"ALTER TABLE categories ADD COLUMN {col} {dtype}")
            print(f"Added column '{col}' to 'categories'")
        else:
            print(f"Column '{col}' already exists in 'categories'")

    conn.commit()
    conn.close()
    print("Migration completed successfully.")

if __name__ == "__main__":
    migrate()
