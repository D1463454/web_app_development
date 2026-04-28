from flask import Flask
from app.routes.recipes import recipe_bp
from dotenv import load_dotenv
import os

# 載入環境變數
load_dotenv()

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.secret_key = os.environ.get('SECRET_KEY', 'default_dev_secret')

# 註冊 Blueprints
app.register_blueprint(recipe_bp)

if __name__ == '__main__':
    app.run(debug=True)
