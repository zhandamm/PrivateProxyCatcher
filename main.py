import configparser
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    # Инициализируем драйвер и другие переменные
    global driver
    count = 1

    # Определяем путь к проекту
    project_dir = os.path.dirname(os.path.abspath(__file__))

    # Определяем путь к файлу proxy.txt
    file_path = os.path.join(project_dir, "proxy.txt")

    config_file_path = os.path.join(project_dir, "config.ini")

    # Создаем или загружаем конфигурационный файл
    config = configparser.ConfigParser()
    if not os.path.exists(config_file_path):
        with open(config_file_path, 'w') as configfile:
            config.add_section('SETTINGS')
            config.set('SETTINGS', 'website_url', '')  # Устанавливаем пустое значение по умолчанию
            config.write(configfile)

    # Читаем URL сайта из конфигурационного файла
    config.read(config_file_path)
    website_url = config.get('SETTINGS', 'website_url')

    # Проверяем существование файла proxy.txt и его размер
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        answer = input("Файл proxy.txt уже содержит прокси. Хотите удалить содержимое файла proxy.txt? Y/N: ")
        if answer.lower() == 'y':
            # Очищаем файл
            with open(file_path, 'w') as f:
                pass  # Пустой файл будет создан или перезаписан

    # Запрашиваем у пользователя ввод числа
    amount = input("Пожалуйста, введите кол-во проксей: ")

    try:
        # Преобразуем введенное значение в число
        amount = int(amount)
        print("Выполнение началось, жди!")
    except ValueError:
        print("Введенное значение не является числом.")
        input("Нажмите Enter для выхода...")
        return

    # Инициализация драйвера
    driver = webdriver.Firefox()
    try:
        # Основной цикл работы
        while count <= amount:
            driver.get(website_url)
            
            # Находим необходимые элементы на странице
            get_another_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn.btn-primary"))
            )
            ip_element = driver.find_element(By.CSS_SELECTOR, ".ip")

            # Цикл для получения прокси
            while count <= amount:
                # Кликаем по кнопке
                get_another_button.click()

                try:
                    # Ожидание изменения текста кнопки или таймаут через 5 секунд
                    WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "button.btn.btn-primary"), "Get another"))

                    if "text-danger" in ip_element.get_attribute("class"):
                        continue
                    elif "text-success" in ip_element.get_attribute("class"):
                        # Находим поле ввода и сохраняем значение
                        input_field = driver.find_element(By.CSS_SELECTOR, ".form-control")
                        content = input_field.get_attribute("value")

                        with open(file_path, "a") as file:
                            file.write(content + "\n")
                        print(count)
                        count += 1

                except Exception as e:
                    print("Данные не поступили в течение 5 секунд, перезагрузка страницы...")
                    break  # Прерываем внутренний цикл для обновления страницы

    except Exception as e:
        print("Произошла ошибка:", e)

    finally:
        driver.quit()


main()
