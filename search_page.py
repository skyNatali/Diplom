"""
Page Object для страницы поиска.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config


class SearchPage:
    """Page Object для страницы поиска Кинопоиска."""
    
    def __init__(self, browser):
        self.browser = browser
        self.browser.get(Config.BASE_URL)
    
    def search(self, query):
        """Выполняет поиск по запросу."""
        # Ждём поле поиска
        search_input = WebDriverWait(
            self.browser, Config.ELEMENT_TIMEOUT
        ).until(
            EC.presence_of_element_located((By.NAME, "kp_query"))
        )
        
        # Вводим запрос
        search_input.clear()
        search_input.send_keys(query)
        search_input.submit()
        
        return self
    
    def verify_result(self, expected_text=None, is_english=False):
        """Проверяет результаты поиска."""
        try:
            # Ожидаем появление результатов
            WebDriverWait(self.browser, Config.SEARCH_TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".search_results"))
            )

            # Если нужно проверить конкретный текст
            if expected_text:
                results_element = self.browser.find_element(By.CSS_SELECTOR, ".search_results")
                if expected_text not in results_element.text:
                    raise AssertionError(f"Не найден текст: {expected_text}")

            return self

        except Exception:
            raise AssertionError("Не удалось найти результаты поиска")
