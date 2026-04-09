import os
import psycopg2
from flask import Flask, render_template_string
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Простой HTML шаблон прямо в коде (для простоты)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>Test Stand</title></head>
<body>
    <h1>🚀 Автоматический тестовый стенд</h1>
    <p>Окружение: <strong>{{ env }}</strong></p>
    <p>Статус БД: <strong>{{ db_status }}</strong></p>
    {% if db_version %}
        <p>Версия PostgreSQL: {{ db_version }}</p>
    {% endif %}
    <hr>
    <p>✅ Стенд работает успешно!</p>
</body>
</html>
'''

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        database=os.getenv('DB_NAME', 'testdb'),
        user=os.getenv('DB_USER', 'user'),
        password=os.getenv('DB_PASSWORD', 'password')
    )

@app.route('/')
def index():
    db_status = "❌ Не подключена"
    db_version = None
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT version();')
        db_version = cur.fetchone()[0][:50] + "..."
        cur.close()
        conn.close()
        db_status = "✅ Подключена"
    except Exception as e:
        db_status = f"❌ Ошибка: {str(e)[:50]}"
    
    return render_template_string(
        HTML_TEMPLATE,
        env=os.getenv('ENV', 'unknown'),
        db_status=db_status,
        db_version=db_version
    )

@app.route('/health')
def health():
    return "OK", 200

@app.route('/db-check')
def db_check():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT 1')
        cur.close()
        conn.close()
        return {"status": "connected", "database": os.getenv('DB_NAME')}, 200
    except Exception as e:
        return {"status": "error", "error": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
