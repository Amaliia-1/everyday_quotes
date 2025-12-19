import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from quotes import (
    get_quote_by_tag,
    get_formatted_tags_list,
    add_new_quote_with_validation,
    search_quotes_count_by_tag
)

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "👋 *Привет! Я бот с цитатами.*\n\n"
        "📚 *Доступные команды:*\n"
        "/start - Начало работы\n"
        "/help - Помощь\n"
        "/quote - Случайная цитата\n"
        "/quote [тег] - Цитата по тегу\n"
        "/tags - Список тегов\n"
        "/add - Добавить цитату\n"
        "/search [тег] - Поиск по тегу\n\n"
        "*Примеры использования:*\n"
        "`/quote` - случайная цитата\n"
        "`/quote Мотивация` - цитата с тегом Мотивация\n"
        "`/search Философия` - найти цитаты по тегу\n"
        "`/add` - добавить новую цитату\n\n"
        "💡 *Совет:* Используйте /help для подробной справки."
    )
    
    await update.message.reply_text(welcome_text, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "📖 *Помощь по использованию бота*\n\n"
        "*Основные команды:*\n"
        "• /start - Начало работы\n"
        "• /help - Эта справка\n"
        "• /quote - Получить случайную цитату\n"
        "• /quote [тег] - Цитата с фильтром по тегу\n"
        "• /tags - Показать все доступные теги\n"
        "• /add - Добавить новую цитату\n"
        "• /search [тег] - Найти цитаты по тегу\n\n"
        "*Как добавить цитату:*\n"
        "1. Напишите /add\n"
        "2. Отправьте цитату в формате:\n"
        "`Текст цитаты | Автор | тег1, тег2, тег3`\n\n"
        "*Пример:*\n"
        "`Всё будет хорошо! | Оптимист | мотивация, философия`\n\n"
        "*Как искать цитаты:*\n"
        "`/search Философия` - покажет сколько цитат с этим тегом\n\n"
        "❓ *Проблемы?* Если что-то не работает, перезапустите бота командой /start"
    )
    
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def quote_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tag = " ".join(context.args) if context.args else None
    
    quote_text = get_quote_by_tag(tag)
    
    if tag:
        message = f"📌 *Цитата с тегом #{tag}:*\n\n{quote_text}"
    else:
        message = f"🎲 *Случайная цитата:*\n\n{quote_text}"
    
    await update.message.reply_text(message, parse_mode="Markdown")


async def tags_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tags_text = get_formatted_tags_list()
    await update.message.reply_text(tags_text, parse_mode="Markdown")


async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    help_text = (
        "📝 *Добавление новой цитаты*\n\n"
        "Отправьте цитату в формате:\n"
        "`Текст цитаты | Автор | тег1, тег2, тег3`\n\n"
        "*Пример 1:*\n"
        "`Жизнь прекрасна! | Оптимист | мотивация, философия`\n\n"
        "*Пример 2:*\n"
        "`Смех - лучшее лекарство | Доктор | юмор, здоровье`\n\n"
        "*Правила:*\n"
        "• Текст цитаты обязателен\n"
        "• Автор обязателен\n"
        "• Хотя бы один тег обязателен\n"
        "• Теги разделяются запятыми\n"
        "• Используйте вертикальную черту | как разделитель"
    )
    
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    if not context.args:
        help_text = (
            "🔍 *Поиск цитат по тегу*\n\n"
            "Используйте команду:\n"
            "`/search [тег]`\n\n"
            "*Примеры:*\n"
            "`/search Мотивация`\n"
            "`/search Любовь`\n\n"
            "Посмотреть все теги: /tags"
        )
        await update.message.reply_text(help_text, parse_mode="Markdown")
        return
    
    tag = " ".join(context.args)
    result = search_quotes_count_by_tag(tag)
    await update.message.reply_text(result)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    text = update.message.text

    if "|" in text:
        try:
            parts = text.split("|")
            
            if len(parts) >= 3:
                quote_text = parts[0].strip()
                author = parts[1].strip()
                tags = parts[2].strip()
                
                result = add_new_quote_with_validation(quote_text, author, tags)
                await update.message.reply_text(result, parse_mode="Markdown")
            else:
                await update.message.reply_text(
                    "❌ *Неверный формат!*\n\n"
                    "Нужно: `Текст | Автор | Теги`\n\n"
                    "Пример:\n"
                    "`Всё будет хорошо! | Оптимист | мотивация, философия`",
                    parse_mode="Markdown"
                )
                
        except Exception as e:
            await update.message.reply_text(
                f"❌ *Ошибка:* {str(e)}\n\n"
                "Попробуйте снова или используйте /help для справки."
            )
    else:
        await update.message.reply_text(
            "🤔*Не понимаю команду*\n\n"
            "Используйте:\n"
            "• /start - для начала работы\n"
            "• /help - для справки\n"
            "• /add - чтобы добавить цитату\n\n"
            "Или отправьте цитату в формате:\n"
            "`Текст | Автор | Теги`",
            parse_mode="Markdown"
        )


def main() -> None:

    if not TOKEN:
        print("ОШИБКА: Токен бота не найден!")
        print("\nЧтобы исправить:")
        print("1. Создайте файл '.env' в папке с проектом")
        print("2. Добавьте в него строку:")
        print("   TELEGRAM_BOT_TOKEN=ваш_токен_здесь")
        print("3. Сохраните файл")
        print("\nКак получить токен:")
        print("1. Откройте Telegram")
        print("2. Найдите @BotFather")
        print("3. Создайте нового бота (/newbot)")
        print("4. Скопируйте токен")
        return
    
    try:
        app = Application.builder().token(TOKEN).build()
        
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("quote", quote_command))
        app.add_handler(CommandHandler("tags", tags_command))
        app.add_handler(CommandHandler("add", add_command))
        app.add_handler(CommandHandler("search", search_command))
        
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        print("Бот успешно запущен!")
        print("Нажмите Ctrl+C для остановки")
        
        app.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
        print(f"❌ Критическая ошибка: {e}")


if __name__ == "__main__":
    main()
