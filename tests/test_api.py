"""
Тесты для API Кинопоиска.
"""
import pytest
import allure
import requests
from api_client import KinopoiskAPIClient


class TestKinopoiskAPI:
    """Тесты API Кинопоиска."""
    
    def setup_method(self):
        """Подготовка перед каждым тестом."""
        self.api_client = KinopoiskAPIClient()
    
    @pytest.mark.api
    @pytest.mark.positive
    @allure.feature("API Тесты")
    @allure.story("Позитивные сценарии поиска")
    def test_search_by_russian_title(self):
        """Поиск фильма по русскому названию."""
        with allure.step("1. Выполняем поиск фильма"):
            result = self.api_client.search_movies("В списках не значился")
        
        with allure.step("2. Проверяем структуру ответа"):
            assert isinstance(result, dict)
            assert "docs" in result
            assert len(result["docs"]) > 0
        
        with allure.step("3. Проверяем, что фильм найден"):
            found = any(
                "В списках не значился" in movie.get("name", "")
                for movie in result["docs"]
            )
            assert found, "Фильм не найден в результатах"
    
    @pytest.mark.api
    @pytest.mark.positive
    @allure.feature("API Тесты")
    @allure.story("Поиск по английскому названию")
    def test_search_by_english_title(self):
        """Поиск фильма по английскому названию."""
        result = self.api_client.search_movies("Prostokvashino")
        
        assert isinstance(result, dict)
        assert "docs" in result
        assert len(result["docs"]) >= 1
    
    @pytest.mark.api
    @pytest.mark.negative
    @allure.feature("API Тесты")
    @allure.story("Негативные сценарии")
    def test_unauthorized_access(self):
        """Проверка доступа без API ключа."""
        url = f"{self.api_client.base_url}/search"
        
        with allure.step("Отправляем запрос без API ключа"):
            response = requests.get(url, params={"query": "test"})
        
        with allure.step("Проверяем код ответа"):
            assert response.status_code == 401, "Ожидался код 401"
    
    @pytest.mark.api
    @allure.feature("API Тесты")
    @allure.story("Получение случайного фильма")
    def test_get_random_movie(self):
        """Получение случайного фильма."""
        movie_data = self.api_client.get_random_movie()
        
        # Проверяем, что получили данные
        if movie_data:
            assert isinstance(movie_data, dict)
            assert "id" in movie_data
            assert "name" in movie_data or "alternativeName" in movie_data
