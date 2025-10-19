from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


class FormPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.url = "https://practice-automation.com/form-fields/"

    NAME_FIELD = (By.ID, "name-input")
    PASSWORD_FIELD = (By.CSS_SELECTOR, "input[type='password']")

    # Чекбоксы напитков
    DRINK_CHECKBOX_MILK = (By.ID, "drink2")
    DRINK_CHECKBOX_COFFEE = (By.ID, "drink3")

    # Радиокнопки цвета
    COLOR_RADIO_YELLOW = (By.ID, "color3")

    # Выпадающий список для автоматизации
    AUTOMATION_DROPDOWN = (By.ID, "automation")

    EMAIL_FIELD = (By.ID, "email")
    MESSAGE_FIELD = (By.ID, "message")
    SUBMIT_BUTTON = (By.ID, "submit-btn")

    # Секция с инструментами автоматизации
    AUTOMATION_TOOLS_SECTION = (By.XPATH, "//*[@id='feedbackForm']/ul")

    def open_page(self):
        self.driver.get(self.url)
        self.wait.until(EC.presence_of_element_located(self.NAME_FIELD))

    def safe_click(self, element):
        """Безопасный клик с прокруткой"""
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

        try:
            element.click()
        except:
            self.driver.execute_script("arguments[0].click();", element)

    def fill_name(self, name):
        name_field = self.wait.until(EC.element_to_be_clickable(self.NAME_FIELD))
        name_field.clear()
        name_field.send_keys(name)

    def fill_password(self, password):
        password_field = self.wait.until(EC.element_to_be_clickable(self.PASSWORD_FIELD))
        password_field.clear()
        password_field.send_keys(password)

    def select_drinks(self):
        """Выбирает Milk и Coffee"""

        milk_checkbox = self.wait.until(EC.presence_of_element_located(self.DRINK_CHECKBOX_MILK))
        self.safe_click(milk_checkbox)

        coffee_checkbox = self.wait.until(EC.presence_of_element_located(self.DRINK_CHECKBOX_COFFEE))
        self.safe_click(coffee_checkbox)

    def select_color(self):
        """Выбирает Yellow цвет"""

        yellow_radio = self.wait.until(EC.presence_of_element_located(self.COLOR_RADIO_YELLOW))
        self.safe_click(yellow_radio)
        assert yellow_radio.is_selected(), "Yellow должен быть выбран"

    def select_automation_preference(self):
        """Выбирает вариант в выпадающем списке Automation"""
        automation_dropdown = self.wait.until(EC.element_to_be_clickable(self.AUTOMATION_DROPDOWN))

        select = Select(automation_dropdown)

        select.select_by_index(1)

    def fill_email(self, email):
        email_field = self.wait.until(EC.element_to_be_clickable(self.EMAIL_FIELD))
        email_field.clear()
        email_field.send_keys(email)

    def get_automation_tools_info(self):
        """Получает информацию об инструментах автоматизации"""
        try:
            tools_section = self.wait.until(EC.presence_of_element_located(self.AUTOMATION_TOOLS_SECTION))
            tools_items = tools_section.find_elements(By.TAG_NAME, "li")

            tools = []
            for item in tools_items:
                tool_text = item.text.strip()
                if tool_text:
                    tools.append(tool_text)

            return tools

        except Exception as e:
            print(f"Ошибка при получении инструментов: {e}")
            return [""]

    def fill_message_with_tools_info(self):
        """Заполняет поле Message информацией об инструментах"""
        tools = self.get_automation_tools_info()
        tools_count = len(tools)

        longest_tool = max(tools, key=len) if tools else ""

        message = f"Number of automation tools: {tools_count}. Longest tool name: {longest_tool}"

        message_field = self.wait.until(EC.element_to_be_clickable(self.MESSAGE_FIELD))
        message_field.clear()
        message_field.send_keys(message)

        return message

    def submit_form(self):
        """Отправляет форму"""
        submit_button = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON))
        self.safe_click(submit_button)

    def get_alert_text(self):
        """Получает текст алерта"""
        try:
            alert = self.wait.until(EC.alert_is_present())
            alert_text = alert.text
            alert.accept()
            return alert_text
        except Exception as e:
            print(f"Алерт не появился: {e}")
            return None

    def is_alert_present(self):
        """Проверяет наличие алерта"""
        try:
            self.wait.until(EC.alert_is_present())
            return True
        except:
            return False

    def take_screenshot(self, name):
        """Делает скриншот"""
        self.driver.save_screenshot(f"{name}.png")
