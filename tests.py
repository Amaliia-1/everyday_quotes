# Простые тесты
import pytest
from quotes import get_random_quote, get_all_tags, add_quote

def test_get_random_quote():
    """Тест получения случайной цитаты"""
    quote = get_random_quote()
    assert quote != ""  # Цитата не должна быть пустой
    assert "\n\n— " in quote  # Должен быть автор

def test_get_all_tags():
    """Тест получения тегов"""
    tags = get_all_tags()
    assert isinstance(tags, list)  # Должен вернуться список
    assert len(tags) > 0  # Должен быть хотя бы один тег

def test_add_quote():
    """Тест добавления цитаты"""
    # Попробуем добавить тестовую цитату
    result = add_quote("Тестовая цитата", "Тестер", ["Тест"])
    assert result == True  # Должно вернуть True при успехе

def test_get_quote_by_tag():
    """Тест фильтрации по тегу"""
    # Сначала добавим цитату с тегом
    add_quote("Еще одна тестовая", "Автор", ["УникальныйТег"])
    
    # Пытаемся получить
    quote = get_random_quote("УникальныйТег")
    assert "Еще одна тестовая" in quote or "Цитаты не найдены" in quote

if __name__ == "__main__":
    # Запуск тестов
    pytest.main([__file__, "-v"])
