"""
Конфигурация тестового окружения.
"""

class Config:
    # Базовый URL
    BASE_URL = "https://www.kinopoisk.ru/"
    
    # Увеличенные таймауты для стабильности
    SEARCH_TIMEOUT = 25  # Увеличили с 15
    ELEMENT_TIMEOUT = 25  # Увеличили с 15
    
    # Тестовые данные
    TEST_DATA = {
        "russian_film": "Простоквашино",
        "english_film": "Prostokvashino",
        "wrong_film": "НесуществующийФильм3-1-2",
        "typo_film": "Простаквашино",
    }
    
    @classmethod
    def get_test_data(cls, key):
        """Возвращает тестовые данные по ключу."""
        if key not in cls.TEST_DATA:
            raise KeyError(f"Ключ '{key}' не найден")
        return cls.TEST_DATA[key]
