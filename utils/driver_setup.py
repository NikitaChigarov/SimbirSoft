import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class DriverSetup:
    @staticmethod
    def get_driver():
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')  # отключает режим песочницы
        chrome_options.add_argument('--disable-dev-shm-usage')  # для Докера
        chrome_options.add_argument('--headless')  # Запускает браузер графического интерфейса
        chrome_options.add_argument('--disable-gpu')  # Отключает аппаратное ускорение (GPU)

        service = Service(ChromeDriverManager().install())

        try:
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.implicitly_wait(10)
            return driver
        except Exception as e:
            print(f"Error initializing driver: {e}")
            sys.exit(1)
