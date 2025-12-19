import os
from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

print("=" * 60)
print("ПРОВЕРКА ПОДКЛЮЧЕНИЯ БОТА К TELEGRAM")
print("=" * 60)

if not TOKEN:
    print("❌ Токен не найден! Проверьте файл .env")
else:
    print(f"✅ Токен найден: {TOKEN[:15]}...")
    
    try:
        bot = Bot(token=TOKEN)
        
        me = bot.get_me()
        
        print(f"✅ Бот подключен успешно!")
        print(f"   Имя бота: {me.first_name}")
        print(f"   Юзернейм: @{me.username}")
        print(f"   ID бота: {me.id}")
        
        updates = bot.get_updates(timeout=5)
        if updates:
            print(f"\n✅ Бот получает сообщения! Последних обновлений: {len(updates)}")
            for update in updates[-3:]:
                if update.message:
                    print(f"   - От {update.message.from_user.username}: {update.message.text}")
        else:
            print("\nℹ️ Сообщений пока нет. Напишите боту в Telegram /start")
            
    except TelegramError as e:
        print(f"❌ Ошибка подключения к Telegram: {e}")
        print("\nВозможные причины:")
        print("1. Неверный токен (пересоздайте через @BotFather)")
        print("2. Проблемы с интернетом (проверьте соединение)")
        print("3. Бот заблокирован")
        
    except Exception as e:
        print(f"❌ Неизвестная ошибка: {e}")

print("=" * 60)
