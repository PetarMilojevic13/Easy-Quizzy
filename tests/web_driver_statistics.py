from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import time

class Statistics(LiveServerTestCase):
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

    def test_statistics_as_guest(self):
        login_as_guest = self.driver.find_element(By.ID, "pocetnaGost")
        login_as_guest.click()
        self.driver.get("http://localhost:8000/easyquizzy/loginAsGuest")

        try:
            link = self.driver.find_element(By.CSS_SELECTOR, "a[href='/easyquizzy/statistics'].icons")
            self.fail("Question suggestion link is present on the page")
        except NoSuchElementException:
            pass
        except BaseException as e:
            self.fail("Test failed: {e}")
