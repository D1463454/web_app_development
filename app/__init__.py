import sqlite3
import os

def init_db():
    """
    初始化資料庫。根據 schema.sql 建立資料表。
    """
    db_path = "instance/database.db"
    schema_path = "database/schema.sql"
    
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
            
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.executescript(schema_sql)
        conn.commit()
        print("資料庫初始化成功！")
    except Exception as e:
        print(f"資料庫初始化失敗: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()
