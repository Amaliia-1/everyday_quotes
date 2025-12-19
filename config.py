import os

class Config:
    DB_PATH = "data/quotes.db"
    
    @classmethod
    def get_token(cls):
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not token:
            raise ValueError("Токен не найден! Создайте бота через @BotFather")
        return token
