from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# Настроим Selenium WebDriver с опциями
options = Options()
options.add_argument("--disable-popup-blocking")  # Отключаем блокировку всплывающих окон
options.add_argument("--headless")  # Запуск браузера без графического интерфейса (опционально)
options.add_argument("--start-maximized")  # Открываем браузер на весь экран
options.add_argument("--no-sandbox")  # Убираем некоторые ограничения
options.add_argument("--disable-dev-shm-usage")  # Исправление для контейнеров (Docker)

# Настроим драйвер
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Переходим на сайт
url = 'https://5ka.ru/catalog/73C2338/gotovaya-eda/'
driver.get(url)


# Функция для ожидания полной загрузки страницы
def wait_for_page_load():
    try:
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        print("Страница полностью загружена.")
    except Exception as e:
        print(f"Ошибка при ожидании загрузки страницы: {e}")


# Функция для обработки кнопки согласия с cookie
def accept_cookies():
    try:
        cookie_accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'chakra-button') and .//p[contains(text(), 'Хорошо')]]")
            )
        )
        cookie_accept_button.click()
        sleep(2)
        print("Нажали на кнопку согласия с cookie.")
    except Exception as e:
        print(f"Не удалось найти кнопку для согласия с cookie: {e}")


# Функция для подтверждения адреса доставки
# def confirm_delivery_address():
#     try:
#         address_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable(
#                 (By.XPATH, "//button[contains(text(), 'Уточните адрес доставки')]")
#             )
#         )
#         address_button.click()
#         print("Открыто окно адреса доставки.")
#
#         # Вводим адрес (пример для Москвы)
#         address_input = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Введите адрес']"))
#         )
#         address_input.send_keys("Москва, Красная площадь")
#         print("Введен адрес доставки.")
#
#         submit_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Применить')]"))
#         )
#         submit_button.click()
#         print("Подтвержден адрес доставки.")
#     except Exception as e:
#         print(f"Ошибка при подтверждении адреса доставки: {e}")


# Функция для получения списка названий продуктов
def get_product_names():
    try:
        # Ждем контейнер с продуктами
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='chakra-stack css-8g6ihq']")
            )
        )
        print("Контейнер с продуктами найден.")

        # Получаем все названия продуктов
        product_names = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//p[contains(@class, 'chakra-text')]")
            )
        )
        print(f"Найдено {len(product_names)} продуктов:")

        for name in product_names:
            text = name.text.strip()
            if text:  # Убираем пустые строки
                print(text)
    except Exception as e:
        driver.save_screenshot("error_screenshot.png")
        print(f"Ошибка при получении списка продуктов: {e}")


# Основной скрипт
try:
    wait_for_page_load()  # Ждем полной загрузки страницы
    accept_cookies()  # Нажимаем на кнопку согласия с cookie
    # confirm_delivery_address()  # Подтверждаем адрес доставки
    get_product_names()  # Получаем список продуктов
finally:
    driver.quit()  # Закрываем браузер
