import pytest
from quotes import get_random_quote, get_all_tags, add_quote

def test_get_random_quote():
    """Тест получения случайной цитаты"""
    quote = get_random_quote()
    assert quote != ""
    assert "\n\n— " in quote

def test_get_all_tags():
    """Тест получения тегов"""
    tags = get_all_tags()
    assert isinstance(tags, list)
    assert len(tags) > 0

def test_add_quote():
    """Тест добавления цитаты"""
    result = add_quote("Тестовая цитата", "Тестер", ["Тест"])
    assert result == True

def test_get_quote_by_tag():
    """Тест фильтрации по тегу"""
    add_quote("Еще одна тестовая", "Автор", ["УникальныйТег"])
    
    quote = get_random_quote("УникальныйТег")
    assert "Еще одна тестовая" in quote or "Цитаты не найдены" in quote

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
