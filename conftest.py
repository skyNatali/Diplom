"""
Конфигурация тестов с Selenium WebDriver.
"""
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def browser():
    """
    Фикстура для управления браузером Chrome.
    
    Использует базовые настройки, без сложных anti-detection методов.
    """
    chrome_options = Options()
    
    # Базовые настройки для стабильности
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    
    # Отключаем сообщения в консоли
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    # Отключаем уведомления
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2
    })
    
    # Инициализация драйвера
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    yield driver
    
    # Закрытие браузера после теста
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Делает скриншот при падении теста.
    
    Этот хук автоматически вызывается pytest при выполнении теста.
    Если тест падает и у него есть фикстура 'browser', делается скриншот.
    """
    outcome = yield
    rep = outcome.get_result()
    
    # Проверяем, что тест упал на этапе выполнения (не в setup/teardown)
    if rep.when == "call" and rep.failed:
        # Проверяем, есть ли у теста фикстура browser
        if "browser" in item.fixturenames:
            browser = item.funcargs["browser"]
            
            try:
                # Делаем скриншот
                screenshot = browser.get_screenshot_as_png()
                
                # Прикрепляем к Allure отчёту
                allure.attach(
                    screenshot,
                    name="screenshot_on_failure",
                    attachment_type=allure.attachment_type.PNG
                )
                print("Скриншот сделан при падении теста")
            except Exception as e:
                print(f"Не удалось сделать скриншот: {e}")
