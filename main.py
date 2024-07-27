import configparser
import os

from selenium import webdriver
from selenium.webdriver.common.by import By


def main():
    global driver
    count = 1

    # Define the project directory path
    project_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the file path within the project directory
    file_path = os.path.join(project_dir, "proxy.txt")

    config_file_path = os.path.join(project_dir, "config.ini")

    # Create or load the configuration file
    config = configparser.ConfigParser()
    if not os.path.exists(config_file_path):
        with open(config_file_path, 'w') as configfile:
            config.add_section('SETTINGS')
            config.set('SETTINGS', 'website_url', '')  # Set an empty default value initially
            config.write(configfile)

    # Read the website URL from the configuration file
    config.read(config_file_path)
    website_url = config.get('SETTINGS', 'website_url')

    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        # Задаем вопрос пользователю
        answer = input("Файл proxy.txt уже содержит прокси. Хотите удалить содержимое файла proxy.txt? Y/N: ")
        if answer.lower() == 'y':
            # Очищаем файл
            with open(file_path, 'w') as f:
                pass  # Пустой файл будет создан или перезаписан
        else:
            # Продолжаем запись в существующий файл
            pass

    # Запрашиваем у пользователя ввод числа
    amount = input("Пожалуйста, введите кол-во проксей: ")

    # Преобразуем введенное значение в число
    try:
        amount = float(amount)
        print(f"Выполнение началось, жди!")
    except ValueError:
        print("Введенное значение не является числом.")
        input("Нажмите Enter для выхода...")
        return

    try:

        # Set the path to the Firefox driver (assuming geckodriver is in the project directory)
        os.environ["webdriver.gecko.driver"] = os.path.join(project_dir, 'geckodriver.exe')

        # Create the Firefox driver
        driver = webdriver.Firefox()

        # Navigate to the website
        driver.get(website_url)

        # Find the "Get another" button
        get_another_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary")
        ip_element = driver.find_element(By.CSS_SELECTOR, ".ip")

        # Loop to click the "Get another" button
        while count <= amount:
            # Click the "Get another" button
            get_another_button.click()

            # Wait for the button to change to "Getting..."
            while get_another_button.get_attribute("disabled") is None:
                import time
                time.sleep(1)

            # Wait for the button to change back to "Get another"
            while get_another_button.text != "Get another":
                import time
                time.sleep(1)

            if "text-danger" in ip_element.get_attribute("class"):
                continue
            elif "text-success" in ip_element.get_attribute("class"):
                # Find the input field
                input_field = driver.find_element(By.CSS_SELECTOR, ".form-control")

                # Get the content of the input field
                content = input_field.get_attribute("value")

                # Write the content to the file
                with open(file_path, "a") as file:
                    file.write(content + "\n")
                print(count)
                count += 1

        print("Работа окончена")
    except Exception as e:
        print("Произошла ошибка:", e)
    finally:
        driver.quit()


main()
exit()
