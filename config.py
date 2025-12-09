# Настройки для бота
import os

class Config:
    # Где будет лежать база данных с цитатами
    DB_PATH = "data/quotes.db"
    
    # Получаем токен бота
    @classmethod
    def get_token(cls):
        # Токен получаем из переменной окружения
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not token:
            raise ValueError("Токен не найден! Создайте бота через @BotFather")
        return token
