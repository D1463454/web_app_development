import sqlite3
import os

DB_PATH = "instance/database.db"

def get_db_connection():
    """
    建立並回傳 SQLite 資料庫連線。
    自動確保 instance 目錄存在。
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 讓查詢結果可以用欄位名稱取值
    return conn

def create(data):
    """
    新增一筆食譜記錄
    :param data: dict，包含 name, ingredients, steps, image_url
    :return: 新增的紀錄 ID，若發生錯誤則回傳 None
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO recipe (name, ingredients, steps, image_url)
            VALUES (?, ?, ?, ?)
            """,
            (data.get('name'), data.get('ingredients'), data.get('steps'), data.get('image_url'))
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Database error in create: {e}")
        return None
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def get_all():
    """
    取得所有食譜記錄
    :return: list of dict，若發生錯誤則回傳空列表
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM recipe ORDER BY created_at DESC")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        print(f"Database error in get_all: {e}")
        return []
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def get_by_id(recipe_id):
    """
    取得單筆食譜記錄
    :param recipe_id: 食譜的 ID
    :return: dict 或 None
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM recipe WHERE id = ?", (recipe_id,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None
    except sqlite3.Error as e:
        print(f"Database error in get_by_id: {e}")
        return None
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def update(recipe_id, data):
    """
    更新記錄
    :param recipe_id: 要更新的食譜 ID
    :param data: dict，包含 name, ingredients, steps, image_url 等要更新的資料
    :return: True 表示更新成功，False 表示失敗
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE recipe 
            SET name = ?, ingredients = ?, steps = ?, image_url = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (data.get('name'), data.get('ingredients'), data.get('steps'), data.get('image_url'), recipe_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Database error in update: {e}")
        return False
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def delete(recipe_id):
    """
    刪除記錄
    :param recipe_id: 要刪除的食譜 ID
    :return: True 表示刪除成功，False 表示失敗
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM recipe WHERE id = ?", (recipe_id,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Database error in delete: {e}")
        return False
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def search_by_keyword(keyword):
    """
    根據名稱或食材模糊搜尋食譜
    :param keyword: 搜尋字串
    :return: list of dict
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        search_pattern = f"%{keyword}%"
        cursor.execute(
            """
            SELECT * FROM recipe 
            WHERE name LIKE ? OR ingredients LIKE ?
            ORDER BY created_at DESC
            """,
            (search_pattern, search_pattern)
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        print(f"Database error in search_by_keyword: {e}")
        return []
    finally:
        if 'conn' in locals() and conn:
            conn.close()
            
def recommend_by_ingredients(ingredients_list):
    """
    根據現有食材推薦食譜
    :param ingredients_list: 食材關鍵字列表
    :return: list of dict
    """
    if not ingredients_list:
        return []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        conditions = " OR ".join(["ingredients LIKE ?" for _ in ingredients_list])
        params = tuple(f"%{ing}%" for ing in ingredients_list)
        cursor.execute(
            f"""
            SELECT * FROM recipe 
            WHERE {conditions}
            ORDER BY created_at DESC
            """,
            params
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        print(f"Database error in recommend_by_ingredients: {e}")
        return []
    finally:
        if 'conn' in locals() and conn:
            conn.close()
