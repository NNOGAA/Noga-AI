"""
Database Initialization Script for Railway Deployment
Runs automatically on startup - safe for production
"""

import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def table_exists(cursor, table_name):
    """Check if table exists in database"""
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    return cursor.fetchone() is not None

def init_database():
    """Initialize database tables if they don't exist"""

    print("🔄 Checking database connection...")

    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT", 3306)),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        cursor = conn.cursor()
        print("✅ Connected to database")

        # Check if table already exists
        if table_exists(cursor, "ocr_table"):
            print("✅ Table 'ocr_table' already exists - skipping creation")
            cursor.close()
            conn.close()
            return True

        print("🔨 Creating table 'ocr_table'...")

        # Create table (without DROP - safe for production)
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS ocr_table (
            sessionid VARCHAR(255) PRIMARY KEY,
            status VARCHAR(50) NOT NULL DEFAULT 'pending',
            ingredients TEXT DEFAULT NULL,
            nutrition_info TEXT DEFAULT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_status (status),
            INDEX idx_created_at (created_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """

        cursor.execute(create_table_sql)
        conn.commit()

        print("✅ Table 'ocr_table' created successfully")

        cursor.close()
        conn.close()

        print("🎉 Database initialization complete!")
        return True

    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
        print("⚠️  API will continue but database operations may fail")
        return False

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    init_database()
