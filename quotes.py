from database import get_random_quote, get_all_tags, add_quote


def format_quote_for_display(quote_text: str) -> str:
    if "—" in quote_text:
        return quote_text
    
    return f"💬 {quote_text}"


def get_quote_by_tag(tag_name: str = None) -> str:
    try:
        quote = get_random_quote(tag_name)
        if quote == "Цитаты не найдены":
            if tag_name:
                return f"😔 Цитат с тегом '#{tag_name}' не найдено.\nПопробуйте другой тег или /tags для списка тегов."
            else:
                return "😔 В базе данных пока нет цитат.\nИспользуйте /add, чтобы добавить первую цитату!"
        
        return format_quote_for_display(quote)
    except Exception as e:
        return f"❌ Ошибка при получении цитаты: {str(e)}"


def get_formatted_tags_list() -> str:

    try:
        tags = get_all_tags()
        
        if not tags:
            return "📭 Тегов пока нет. Добавьте первую цитату с тегом командой /add!"
        
        tags_formatted = "\n".join([f"• #{tag}" for tag in tags])
        
        return (f"📚 *Доступные теги:*\n\n"
                f"{tags_formatted}\n\n"
                f"Используйте команду:\n`/quote [тег]`\n\n"
                f"*Пример:* `/quote {tags[0]}`")
    except Exception as e:
        return f"❌ Ошибка при получении тегов: {str(e)}"


def add_new_quote_with_validation(text: str, author: str, tags_input: str) -> str:

    if not text or not text.strip():
        return "❌ Текст цитаты не может быть пустым!"
    
    if not author or not author.strip():
        return "❌ Автор не может быть пустым!"
    
    if not tags_input or not tags_input.strip():
        return "❌ Укажите хотя бы один тег!"
    
    # Обрабатываем теги
    tags_list = []
    for tag in tags_input.split(','):
        tag_clean = tag.strip()
        if tag_clean:
            tags_list.append(tag_clean)
    
    if not tags_list:
        return "❌ Укажите хотя бы один тег!"
    
    # Проверяем длину тегов
    for tag in tags_list:
        if len(tag) > 50:
            return f"❌ Тег '{tag}' слишком длинный (максимум 50 символов)"
    
    # Добавляем цитату
    try:
        success = add_quote(text.strip(), author.strip(), tags_list)
        if success:
            tags_formatted = ", ".join([f"#{tag}" for tag in tags_list])
            return (f"✅ *Цитата добавлена!*\n\n"
                    f"💬 *Цитата:* {text.strip()}\n"
                    f"👤 *Автор:* {author.strip()}\n"
                    f"🏷 *Теги:* {tags_formatted}")
        else:
            return "❌ Не удалось добавить цитату. Проверьте данные и попробуйте снова."
    except Exception as e:
        error_msg = str(e)
        if "UNIQUE constraint failed" in error_msg:
            return "❌ Такая цитата уже существует!"
        else:
            return f"❌ Ошибка при добавлении цитаты: {error_msg}"


def search_quotes_count_by_tag(tag_name: str) -> str:

    try:
        
        from database import cursor, conn
        
        cursor.execute('''
            SELECT COUNT(*) 
            FROM quotes q
            JOIN quote_tags qt ON q.id = qt.quote_id
            JOIN tags t ON qt.tag_id = t.id
            WHERE t.name = ?
        ''', (tag_name,))
        
        count = cursor.fetchone()[0]
        
        if count == 0:
            return f"🔍 Цитат с тегом '#{tag_name}' не найдено."
        elif count == 1:
            return f"🔍 Найдена 1 цитата с тегом #{tag_name}."
        else:
            return f"🔍 Найдено {count} цитат с тегом #{tag_name}."
            
    except Exception as e:
        return f"❌ Ошибка при поиске: {str(e)}"


if __name__ == "__main__":
    print("=== Тестирование модуля quotes.py ===\n")
    
    print("1. Тест получения случайной цитаты:")
    random_quote = get_quote_by_tag()
    print(random_quote[:100] + "..." if len(random_quote) > 100 else random_quote)
    print()
    
    print("2. Тест получения тегов:")
    tags = get_formatted_tags_list()
    print(tags[:150] + "..." if len(tags) > 150 else tags)
    print()
    
    print("3. Тест добавления цитаты:")
    result = add_new_quote_with_validation(
        "Тестовая цитата для проверки",
        "Тестовый автор",
        "тест, проверка"
    )
    print(result)
    print()
    
    print("4. Тест поиска по тегу:")
    search_result = search_quotes_count_by_tag("Мотивация")
    print(search_result)
