"""
Smoke тест покупки билетов.
"""
import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from config import Config


@pytest.mark.smoke
@pytest.mark.ui
class TestKinopoiskTickets:
    """Smoke тест покупки билетов."""
    
    @allure.feature("Smoke Тесты")
    @allure.story("Основной поток покупки билетов")
    def test_ticket_purchase_flow(self, browser):
        """Основной поток покупки билетов."""
        
        with allure.step("1. Переходим на сайт"):
            browser.get(Config.BASE_URL)
        
        with allure.step("2. Ищем кнопку 'Билеты в кино'"):
            try:
                tickets_button = WebDriverWait(browser, Config.ELEMENT_TIMEOUT).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Билеты в кино"))
                )
                tickets_button.click()
            except:
                # Пробуем другой селектор
                tickets_button = browser.find_element(
                    By.XPATH, "//a[contains(text(), 'Билеты')]"
                )
                tickets_button.click()
        
        with allure.step("3. Ждём загрузки страницы с билетами"):
            WebDriverWait(browser, Config.SEARCH_TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1, .movie-list, .schedule"))
            )
        
        with allure.step("4. Ищем фильмы для покупки"):
            movies = browser.find_elements(By.CSS_SELECTOR, ".movie-item, .film-card")
            
            if movies:
                with allure.step("5. Кликаем на первый доступный фильм"):
                    # Прокручиваем к элементу перед кликом
                    actions = ActionChains(browser)
                    actions.move_to_element(movies[0]).perform()
                    
                    # Ждём, пока элемент станет кликабельным
                    WebDriverWait(browser, 5).until(
                        EC.element_to_be_clickable(movies[0])
                    )
                    
                    movies[0].click()
            else:
                pytest.skip("Нет фильмов для тестирования покупки билетов")
