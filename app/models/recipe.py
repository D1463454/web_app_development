import sqlite3

class RecipeModel:
    def __init__(self, db_path="database/app.db"):
        self.db_path = db_path

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 讓結果像字典一樣可透過欄位名取值
        return conn

    def create(self, name, ingredients, steps, image_url=None):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO recipe (name, ingredients, steps, image_url)
            VALUES (?, ?, ?, ?)
            """,
            (name, ingredients, steps, image_url)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    def get_all(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM recipe ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_by_id(self, recipe_id):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM recipe WHERE id = ?", (recipe_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return dict(row)
        return None

    def search_by_keyword(self, keyword):
        """根據名稱或食材搜尋食譜"""
        conn = self._get_connection()
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
        conn.close()
        return [dict(row) for row in rows]
        
    def recommend_by_ingredients(self, ingredients_list):
        """根據現有食材推薦食譜 (簡易實作：逐一比對食材關鍵字)"""
        if not ingredients_list:
            return []
            
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # 建立 OR 條件
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
        conn.close()
        return [dict(row) for row in rows]

    def update(self, recipe_id, name, ingredients, steps, image_url=None):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE recipe 
            SET name = ?, ingredients = ?, steps = ?, image_url = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (name, ingredients, steps, image_url, recipe_id)
        )
        conn.commit()
        rowcount = cursor.rowcount
        conn.close()
        return rowcount > 0

    def delete(self, recipe_id):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM recipe WHERE id = ?", (recipe_id,))
        conn.commit()
        rowcount = cursor.rowcount
        conn.close()
        return rowcount > 0

# 全域單例使用
recipe_model = RecipeModel()
