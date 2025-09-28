from dotenv import load_dotenv
import os

load_dotenv()  # загружаем .env

DB_URL = os.getenv("DATABASE_URL")  # <-- тут имя переменной, а не сама строка
print("DEBUG DB_URL =", DB_URL)

