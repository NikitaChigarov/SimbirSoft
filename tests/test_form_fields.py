import allure
import pytest

from pages.from_page import FormPage
from utils.driver_setup import DriverSetup


@allure.feature("Form Fields Tests")
class TestFormFields:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.driver = None
        try:
            self.driver = DriverSetup.get_driver()
            self.form_page = FormPage(self.driver)
            yield
        except Exception as e:
            pytest.fail(f"Failed to initialize driver: {e}")
        finally:
            if self.driver:
                self.driver.quit()

    @allure.story("Test Case 1: Fill basic form fields")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_fill_basic_form_fields(self):
        """Кейс 1: Заполнение основных полей формы"""
        try:
            with allure.step("Step 1: Open form page"):
                self.form_page.open_page()
                # time.sleep(2)

            with allure.step("Step 2: Fill name field"):
                self.form_page.fill_name("Test User")

            with allure.step("Step 3: Fill password field"):
                self.form_page.fill_password("securepassword123")

            with allure.step("Step 4: Select Milk and Coffee from favorite drinks"):
                self.form_page.select_drinks()

            with allure.step("Step 5: Select Yellow from favorite colors"):
                self.form_page.select_color()

            with allure.step("Step 6: Select automation preference"):
                self.form_page.select_automation_preference()

            with allure.step("Step 7: Fill email field"):
                self.form_page.fill_email("name@example.com")

            assert True, "All form fields filled successfully"

        except Exception as e:
            self.form_page.take_screenshot("test_case_1_error")
            pytest.fail(f"Test Case 1 failed: {e}")

    @allure.story("Test Case 2: Complete form submission with tools info")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_complete_form_submission(self):
        """Кейс 2: Полное заполнение формы и отправка"""
        try:
            with allure.step("Open form page"):
                self.form_page.open_page()

            with allure.step("Fill all basic form fields"):
                self.form_page.fill_name("Test User")
                self.form_page.fill_password("securepassword123")
                self.form_page.select_drinks()
                self.form_page.select_color()
                self.form_page.select_automation_preference()
                self.form_page.fill_email("name@example.com")

            with allure.step("Fill message with automation tools info"):
                message = self.form_page.fill_message_with_tools_info()
                allure.attach(message, "Message content", allure.attachment_type.TEXT)

            with allure.step("Submit form"):
                self.form_page.submit_form()

            with allure.step("Verify alert message"):
                assert self.form_page.is_alert_present(), "Alert should be present after form submission"
                alert_text = self.form_page.get_alert_text()
                assert alert_text == "Message received!"

        except Exception as e:
            self.form_page.take_screenshot("test_case_2_error")
            pytest.fail(f"Test Case 2 failed: {e}")
