"""
Модуль smoke-тестирования функционала поиска на Кинопоиске.
"""
import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config
from search_page import SearchPage


@pytest.mark.ui
@pytest.mark.smoke
class TestKinopoiskSearch:
    """
    Класс для тестирования функционала поиска на сайте Кинопоиск.
    """

    @allure.feature("Поиск фильмов")
    @allure.story("Основные сценарии поиска")
    def test_search_functionality(self, browser):
        """
        Основной тест проверки функционала поиска фильмов.
        """
        search = SearchPage(browser)

        # Шаг 1-2: Поиск и проверка русского названия
        with allure.step("Шаг 1-2: Поиск русского фильма"):
            (search.search(Config.TEST_DATA["russian_film"])
             .verify_result(Config.TEST_DATA["russian_film"]))

        # Шаг 3-4: Поиск и проверка английского названия
        with allure.step("Шаг 3-4: Поиск английского названия"):
            (search.search(Config.TEST_DATA["english_film"])
             .verify_result(Config.TEST_DATA["russian_film"]))

        # Шаг 5: Переход на страницу фильма
        with allure.step("Шаг 5: Переход на страницу фильма"):
            film_link = browser.find_element(
                By.CSS_SELECTOR,
                "div.search_results > div > div.info > p.name > a"
            )
            film_link.click()
            
            # Даем время на загрузку страницы
            time.sleep(3)
            
            # Проверяем, не капча ли это
            if "Вы не робот" in browser.title:
                allure.attach(
                    browser.get_screenshot_as_png(),
                    name="captcha_detected",
                    attachment_type=allure.attachment_type.PNG
                )
                print("ВНИМАНИЕ: Появилась капча, пропускаем проверку заголовка")
            else:
                assert Config.TEST_DATA["russian_film"] in browser.title

        # Шаг 6: Поиск несуществующего фильма
        with allure.step("Шаг 6: Поиск несуществующего фильма"):
            browser.get(Config.BASE_URL)
            search.search(Config.TEST_DATA["wrong_film"])
            assert "ничего не найдено" in browser.page_source

        # Шаг 7: Пустой поиск
        with allure.step("Шаг 7: Пустой поиск"):
            browser.get(Config.BASE_URL)
            search_input = WebDriverWait(
                browser, Config.ELEMENT_TIMEOUT
            ).until(
                EC.presence_of_element_located((By.NAME, "kp_query"))
            )
            search_input.clear()
            search_input.send_keys("\n")
            WebDriverWait(browser, Config.ELEMENT_TIMEOUT).until(
                EC.title_contains("Случайный фильм")
            )
            assert "Случайный фильм" in browser.title

        # Шаг 8: Поиск с опечаткой
        with allure.step("Шаг 8: Поиск с опечаткой"):
            browser.get(Config.BASE_URL)
            (search.search(Config.TEST_DATA["typo_film"])
             .verify_result(Config.TEST_DATA["russian_film"]))
