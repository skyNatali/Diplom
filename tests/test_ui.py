"""
UI тесты для поиска на Кинопоиске.
"""
import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config


@pytest.mark.ui
class TestKinopoiskSearch:
    """Тесты поиска фильмов."""
    
    @allure.feature("UI Тесты")
    @allure.story("Поиск по русскому названию")
    def test_search_russian_movie(self, browser):
        """Поиск фильма по русскому названию."""
        browser.get(Config.BASE_URL)
        
        with allure.step("1. Находим поле поиска"):
            search_input = WebDriverWait(browser, Config.ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located((By.NAME, "kp_query"))
            )
        
        with allure.step("2. Вводим название фильма"):
            search_input.clear()
            search_input.send_keys("Простоквашино")
            search_input.submit()
        
        with allure.step("3. Ожидаем результаты"):
            WebDriverWait(browser, Config.SEARCH_TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".search_results"))
            )
        
        with allure.step("4. Проверяем, что фильм найден"):
            results = browser.find_elements(By.CSS_SELECTOR, ".search_results .name")
            assert len(results) > 0, "Результаты поиска не найдены"
    
    @allure.feature("UI Тесты")
    @allure.story("Поиск по английскому названию")
    def test_search_english_movie(self, browser):
        """Поиск по английскому названию."""
        browser.get(Config.BASE_URL)
        
        search_input = WebDriverWait(browser, Config.ELEMENT_TIMEOUT).until(
            EC.presence_of_element_located((By.NAME, "kp_query"))
        )
        
        search_input.send_keys("Prostokvashino")
        search_input.submit()
        
        WebDriverWait(browser, Config.SEARCH_TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".search_results"))
        )
        
        results = browser.find_elements(By.CSS_SELECTOR, ".search_results .name, .search_results .alternativeName")
        assert len(results) > 0, "Результаты поиска не найдены"
    
    @allure.feature("UI Тесты")
    @allure.story("Пустой поиск")
    def test_empty_search(self, browser):
        """Проверка пустого поиска."""
        browser.get(Config.BASE_URL)
        
        search_input = WebDriverWait(browser, Config.ELEMENT_TIMEOUT).until(
            EC.presence_of_element_located((By.NAME, "kp_query"))
        )
        
        search_input.clear()
        search_input.submit()
        
        # Ждём либо загрузки страницы, либо появления результатов
        try:
            WebDriverWait(browser, 10).until(
                lambda d: "/chance/" in d.current_url or
                d.find_elements(By.CSS_SELECTOR, ".search_results")
            )
        except:
            # Если ничего не произошло, тест продолжается
            pass
