#!/usr/bin/env python3
"""Seed script for Vision Platform."""
import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), 'instance', 'vision.db')

def seed():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Seed admin user
    cursor.execute("SELECT id FROM users WHERE phone = ?", ("07833779833",))
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO users (phone, password, full_name, user_type, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, ("07833779833", "admin123", "Administrator", "admin", datetime.utcnow()))
        print("Admin user created: phone=07833779833, password=admin123")
    else:
        print("Admin user already exists")

    # Seed default categories if empty
    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        defaults = [
            ("عقارات", "realestate", "building", 1, 0),
            ("سيارات", "vehicles", "car", 1, 0),
            ("إلكترونيات", "electronics", "tv", 1, 0),
            ("أثاث", "furniture", "couch", 1, 0),
            ("وظائف", "jobs", "briefcase", 1, 0),
            ("خدمات", "services", "wrench", 1, 0),
            ("حيوانات", "animals", "paw", 1, 0),
            ("متفرقات", "others", "box", 1, 0),
        ]
        cursor.executemany("""
            INSERT INTO categories (name, slug, icon, is_active, subscription_price)
            VALUES (?, ?, ?, ?, ?)
        """, defaults)
        print(f"Seeded {len(defaults)} default categories")
    else:
        print("Categories already seeded")

    conn.commit()
    conn.close()
    print("Seeding completed.")

if __name__ == "__main__":
    seed()
