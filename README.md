# Telegram Psychology Bot

Бот для ведения дневника настроений 📊 на Python + PostgreSQL.

## 🚀 Деплой на Render
1. Форкни/залей проект на GitHub.
2. Создай **Postgres Database** на Render (Free plan).
3. Скопируй `DATABASE_URL` (external).
4. Создай **Worker Service** на Render:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
5. Добавь переменные окружения:
   - `BOT_TOKEN` = токен от @BotFather
   - `DATABASE_URL` = Postgres URL

## ✅ Функции
- `/start` — приветствие
- Запись настроения (1–10)
- История последних 10 настроений
