"""
Клиент для работы с API Кинопоиска.
"""
import requests
from settings import settings


class KinopoiskAPIClient:
    """Клиент для работы с API Кинопоиска."""
    
    def __init__(self):
        """Инициализация клиента с настройками."""
        self.base_url = settings.API_URL
        self.headers = {
            "accept": "application/json",
            "X-API-KEY": settings.API_KEY
        }

    def search_movies(self, query, page=1, limit=10):
        """
        Поиск фильмов по названию.
        
        Args:
            query: Строка для поиска
            page: Номер страницы
            limit: Количество результатов (макс 50)
        
        Returns:
            Словарь с результатами поиска
        """
        url = f"{self.base_url}/search"
        params = {
            "query": query,
            "page": page,
            "limit": min(limit, 50)
        }
        
        response = requests.get(
            url,
            headers=self.headers,
            params=params
        )
        response.raise_for_status()
        return response.json()

    def get_random_movie(self):
        """Получает случайный фильм."""
        url = f"{self.base_url}/random"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            # В реальном проекте здесь было бы логирование
            return None
