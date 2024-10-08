from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import time

class QuestionSuggestionTests(LiveServerTestCase):
    base_url = "http://localhost:8000/easyquizzy/"
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chromedriver_path = r"C:\Users\Miletic\PycharmProjects\testarinjePSI\chromedriver-win64\chromedriver.exe"
        cls.service = ChromeService(executable_path=chromedriver_path)
        cls.driver = webdriver.Chrome(service=cls.service)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        self.driver.get(self.base_url)

    def test_suggestion_as_guest(self):
        login_as_guest = self.driver.find_element(By.ID, "pocetnaGost")
        login_as_guest.click()
        self.driver.get("http://localhost:8000/easyquizzy/loginAsGuest")

        try:
            link = self.driver.find_element(By.CSS_SELECTOR, "a[href='/easyquizzy/questionSuggestion'].icons")
            self.fail("Question suggestion link is present on the page")
        except NoSuchElementException:
            pass
        except BaseException as e:
            self.fail("Test failed: {e}")

    def test_suggestion_as_mod(self):
        username_input = self.driver.find_element(By.NAME, "username")
        username_input.send_keys("elena123")
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys("Psii123+")
        submit = self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Prijavi se']")
        submit.click()

        try:
            link = self.driver.find_element(By.CSS_SELECTOR, "a[href='/easyquizzy/questionSuggestion'].icons")
            self.fail("Question suggestion link is present on the page")
        except NoSuchElementException:
            pass
        except BaseException as e:
            self.fail("Test failed: {e}")
        finally:
            logout_link = self.driver.find_element(By.CSS_SELECTOR, "a[href='/easyquizzy/logout'].icons")
            logout_link.click()

    def test_suggestion_as_admin(self):
        username_input = self.driver.find_element(By.NAME, "username")
        username_input.send_keys("meg123")
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys("Psii123+")
        submit = self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Prijavi se']")
        submit.click()

        try:
            link = self.driver.find_element(By.CSS_SELECTOR, "a[href='/easyquizzy/questionSuggestion'].icons")
            self.fail("Question suggestion link is present on the page")
        except NoSuchElementException:
            pass
        except BaseException as e:
            self.fail("Test failed: {e}")
        finally:
            logout_link = self.driver.find_element(By.CSS_SELECTOR, "a[href='/easyquizzy/logout'].icons")
            logout_link.click()

    def test_suggest_empty(self):
        username_input = self.driver.find_element(By.NAME, "username")
        username_input.send_keys("ilija123")
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys("Psii123+")
        submit = self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Prijavi se']")
        submit.click()

        try:
            link = self.driver.find_element(By.CSS_SELECTOR, "a[href='/easyquizzy/questionSuggestion'].icons")
            link.click()

            submit = self.driver.find_element(By.TAG_NAME, "button")
            submit.click()

            time.sleep(2)
            message_div = self.driver.find_element(By.ID, "message")
            self.assertEqual(message_div.text, "Uneli ste prazno pitanje!")
        except BaseException as e:
            self.fail("Test failed: {e}")
        finally:
            logout_link = self.driver.find_element(By.CSS_SELECTOR, "a[href='/easyquizzy/logout'].icons")
            logout_link.click()
