#Ilija Miletić 2021/0335

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import random
import time

class IlijaAllTests(LiveServerTestCase):
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
            self.assertEqual(message_div.text, "Tekst pitanja nije popunjen!")
        except BaseException as e:
            self.fail("Test failed: {e}")
        finally:
            logout_link = self.driver.find_element(By.CSS_SELECTOR, "a[href='/easyquizzy/logout'].icons")
            logout_link.click()

    def test_add_question_as_guest(self):
        login_as_guest = self.driver.find_element(By.ID, "pocetnaGost")
        login_as_guest.click()

        self.driver.get("http://localhost:8000/easyquizzy/loginAsGuest")

        try:
            link = self.driver.find_element(By.CSS_SELECTOR, "a[href='/easyquizzy/addingQuestions'].icons")
            self.fail("Adding questions link is present on the page")
        except NoSuchElementException:
            pass
        except BaseException as e:
            self.fail("Test failed: {e}")

    def test_add_question_as_reg(self):
        username_input = self.driver.find_element(By.NAME, "username")
        username_input.send_keys("ilija123")
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys("Psii123+")
        submit = self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Prijavi se']")
        submit.click()

        try:
            link = self.driver.find_element(By.CSS_SELECTOR, "a[href='/easyquizzy/addingQuestions'].icons")
            self.fail("Adding questions link is present on the page")
        except NoSuchElementException:
            pass
        except BaseException as e:
            self.fail("Test failed: {e}")
        finally:
            logout_link = self.driver.find_element(By.CSS_SELECTOR, "a[href='/easyquizzy/logout'].icons")
            logout_link.click()

    def test_adding_question(self):
        username_input = self.driver.find_element(By.NAME, "username")
        username_input.send_keys("elena123")
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys("Psii123+")
        submit = self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Prijavi se']")
        submit.click()

        try:
            link = self.driver.find_element(By.CSS_SELECTOR, "a[href='/easyquizzy/addingQuestions'].icons")
            link.click()

            categories = self.driver.find_element(By.XPATH, "//form[@action='/easyquizzy/addNewQuestion']//select[@name='category']")
            categories_list = Select(categories)
            categories_list.select_by_visible_text("Istorija")

            question = self.driver.find_element(By.XPATH, "//form[@action='/easyquizzy/addNewQuestion']//input[@name='question']")
            random.seed(time.time())
            question.send_keys("Istorija novo pitanje " + str(random.randint(0, 1000000000)))

            difficulty = self.driver.find_element(By.ID, "easyyy")
            difficulty.click()

            correct = self.driver.find_element(By.XPATH, "//form[@action='/easyquizzy/addNewQuestion']//input[@name='correct']")
            correct.send_keys("Tacan")
            incorrect1 = self.driver.find_element(By.XPATH, "//form[@action='/easyquizzy/addNewQuestion']//input[@name='incorrect1']")
            incorrect1.send_keys("Netacan 1")
            incorrect2 = self.driver.find_element(By.XPATH, "//form[@action='/easyquizzy/addNewQuestion']//input[@name='incorrect2']")
            incorrect2.send_keys("Netacan 2")
            incorrect3 = self.driver.find_element(By.XPATH, "//form[@action='/easyquizzy/addNewQuestion']//input[@name='incorrect3']")
            incorrect3.send_keys("Netacan 3")

            submit = self.driver.find_element(By.XPATH, "//form[@action='/easyquizzy/addNewQuestion']//button[@type='submit']")
            submit.click()
            time.sleep(2)

            message_div = self.driver.find_element(By.ID, "message")
            self.assertEqual(message_div.text, "Pitanje je uspešno ubačeno u bazu!")

        except BaseException as e:
            self.fail("Test failed: {e}")
        finally:
            logout_link = self.driver.find_element(By.CSS_SELECTOR, "a[href='/easyquizzy/logout'].icons")
            logout_link.click()

    def test_adding_existing_question(self):
        username_input = self.driver.find_element(By.NAME, "username")
        username_input.send_keys("meg123")
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys("Psii123+")
        submit = self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Prijavi se']")
        submit.click()

        try:
            link = self.driver.find_element(By.CSS_SELECTOR, "a[href='/easyquizzy/addingQuestions'].icons")
            link.click()

            categories = self.driver.find_element(By.XPATH, "//form[@action='/easyquizzy/addNewQuestion']//select[@name='category']")
            categories_list = Select(categories)
            categories_list.select_by_visible_text("Istorija")

            question = self.driver.find_element(By.XPATH, "//form[@action='/easyquizzy/addNewQuestion']//input[@name='question']")
            question.send_keys("Dokle je stigao Aleksandar Makedonski u svojim osvajanjima?")

            difficulty = self.driver.find_element(By.ID, "easyyy")
            difficulty.click()

            correct = self.driver.find_element(By.XPATH, "//form[@action='/easyquizzy/addNewQuestion']//input[@name='correct']")
            correct.send_keys("Tacan")
            incorrect1 = self.driver.find_element(By.XPATH, "//form[@action='/easyquizzy/addNewQuestion']//input[@name='incorrect1']")
            incorrect1.send_keys("Netacan 1")
            incorrect2 = self.driver.find_element(By.XPATH, "//form[@action='/easyquizzy/addNewQuestion']//input[@name='incorrect2']")
            incorrect2.send_keys("Netacan 2")
            incorrect3 = self.driver.find_element(By.XPATH, "//form[@action='/easyquizzy/addNewQuestion']//input[@name='incorrect3']")
            incorrect3.send_keys("Netacan 3")

            submit = self.driver.find_element(By.XPATH, "//form[@action='/easyquizzy/addNewQuestion']//button[@type='submit']")
            submit.click()
            time.sleep(2)

            message_div = self.driver.find_element(By.ID, "message")
            self.assertEqual(message_div.text, "Pitanje sa datim tekstom već postoji!")

        except BaseException as e:
            self.fail("Test failed: {e}")
        finally:
            logout_link = self.driver.find_element(By.CSS_SELECTOR, "a[href='/easyquizzy/logout'].icons")
            logout_link.click()

    def test_adding_question_empty_fields(self):
        username_input = self.driver.find_element(By.NAME, "username")
        username_input.send_keys("elena123")
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys("Psii123+")
        submit = self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Prijavi se']")
        submit.click()

        try:
            link = self.driver.find_element(By.CSS_SELECTOR, "a[href='/easyquizzy/addingQuestions'].icons")
            link.click()

            submit = self.driver.find_element(By.XPATH, "//form[@action='/easyquizzy/addNewQuestion']//button[@type='submit']")
            submit.click()
            time.sleep(2)

            message_div = self.driver.find_element(By.ID, "message")
            self.assertEqual(message_div.text, "Niste popunili sva polja!")

        except BaseException as e:
            self.fail("Test failed: {e}")
        finally:
            logout_link = self.driver.find_element(By.CSS_SELECTOR, "a[href='/easyquizzy/logout'].icons")
            logout_link.click()

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

    def test_add_category_as_guest(self):
        login_as_guest = self.driver.find_element(By.ID, "pocetnaGost")
        login_as_guest.click()

        self.driver.get("http://localhost:8000/easyquizzy/loginAsGuest")

        try:
            link = self.driver.find_element(By.CSS_SELECTOR, "a[href='/easyquizzy/addingCategories'].icons")
            self.fail("Adding categories link is present on the page")
        except NoSuchElementException:
            pass
        except BaseException as e:
            self.fail("Test failed: {e}")

    def test_add_category_as_reg(self):
        username_input = self.driver.find_element(By.NAME, "username")
        username_input.send_keys("petar123")
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys("Psii123+")
        submit = self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Prijavi se']")
        submit.click()

        try:
            link = self.driver.find_element(By.CSS_SELECTOR, "a[href='/easyquizzy/addingCategories'].icons")
            self.fail("Adding categories link is present on the page")
        except NoSuchElementException:
            pass
        except BaseException as e:
            self.fail("Test failed: {e}")
        finally:
            logout_link = self.driver.find_element(By.CSS_SELECTOR, "a[href='/easyquizzy/logout'].icons")
            logout_link.click()

    def test_adding_category(self):
        username_input = self.driver.find_element(By.NAME, "username")
        username_input.send_keys("elena123")
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys("Psii123+")
        submit = self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Prijavi se']")
        submit.click()

        try:
            link = self.driver.find_element(By.CSS_SELECTOR, "a[href='/easyquizzy/addingCategories'].icons")
            link.click()

            random.seed(time.time())
            for i in range(5):
                question = self.driver.find_element(By.NAME, "text")
                question.send_keys("Novo pitanje " + str(random.randint(0, 1000000000)) + str(random.randint(0, 1000000000)))
                difficulty = self.driver.find_element(By.ID, "easy")
                difficulty.click()

                correct = self.driver.find_element(By.NAME, "correct")
                correct.send_keys("Tacno")
                incorrect1 = self.driver.find_element(By.NAME, "incorrect1")
                incorrect1.send_keys("Netacno1")
                incorrect2 = self.driver.find_element(By.NAME, "incorrect2")
                incorrect2.send_keys("Netacno2")
                incorrect3 = self.driver.find_element(By.NAME, "incorrect3")
                incorrect3.send_keys("Netacno3")

                add = self.driver.find_element(By.ID, "addQuestion")
                add.click()


            category_name = self.driver.find_element(By.NAME, "newCatName")
            random.seed(time.time())
            category_name.send_keys("Nova kategorija " + str(random.randint(0, 1000000000)))

            category_img = self.driver.find_element(By.NAME, "newCatFile")
            category_img.send_keys("C:\\Software\\PSI\\Projekat\\project_Djangovi_OSvetnici\\Faza5\\EasyQuizzy\\static\\css\\logo.jpeg")

            submit = self.driver.find_element(By.XPATH, "//form[@action='/easyquizzy/addNewCategory']//button[@type='submit']")
            submit.click()
            time.sleep(2)

            message_div = self.driver.find_element(By.ID, "messageCat")
            self.assertEqual(message_div.text, "Kategorija je uspešno dodata")

        except BaseException as e:
            self.fail("Test failed: {e}")
        finally:
            logout_link = self.driver.find_element(By.CSS_SELECTOR, "a[href='/easyquizzy/logout'].icons")
            logout_link.click()

    def test_adding_existing_category(self):
        username_input = self.driver.find_element(By.NAME, "username")
        username_input.send_keys("elena123")
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys("Psii123+")
        submit = self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Prijavi se']")
        submit.click()

        try:
            link = self.driver.find_element(By.CSS_SELECTOR, "a[href='/easyquizzy/addingCategories'].icons")
            link.click()

            random.seed(time.time())
            for i in range(5):
                question = self.driver.find_element(By.NAME, "text")
                question.send_keys("Novo pitanje " + str(random.randint(0, 1000000000)) + str(random.randint(0, 1000000000)))
                difficulty = self.driver.find_element(By.ID, "easy")
                difficulty.click()

                correct = self.driver.find_element(By.NAME, "correct")
                correct.send_keys("Tacno")
                incorrect1 = self.driver.find_element(By.NAME, "incorrect1")
                incorrect1.send_keys("Netacno1")
                incorrect2 = self.driver.find_element(By.NAME, "incorrect2")
                incorrect2.send_keys("Netacno2")
                incorrect3 = self.driver.find_element(By.NAME, "incorrect3")
                incorrect3.send_keys("Netacno3")

                add = self.driver.find_element(By.ID, "addQuestion")
                add.click()


            category_name = self.driver.find_element(By.NAME, "newCatName")
            random.seed(time.time())
            category_name.send_keys("Sport")

            category_img = self.driver.find_element(By.NAME, "newCatFile")
            category_img.send_keys("C:\\Software\\PSI\\Projekat\\project_Djangovi_OSvetnici\\Faza5\\EasyQuizzy\\static\\css\\sport.jpg")

            submit = self.driver.find_element(By.XPATH, "//form[@action='/easyquizzy/addNewCategory']//button[@type='submit']")
            submit.click()
            time.sleep(2)

            message_div = self.driver.find_element(By.ID, "messageCat")
            self.assertEqual(message_div.text, "Kategorija sa datim nazivom već postoji")

        except BaseException as e:
            self.fail("Test failed: {e}")
        finally:
            logout_link = self.driver.find_element(By.CSS_SELECTOR, "a[href='/easyquizzy/logout'].icons")
            logout_link.click()

    def test_changing_category_image(self):
        username_input = self.driver.find_element(By.NAME, "username")
        username_input.send_keys("meg123")
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys("Psii123+")
        submit = self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Prijavi se']")
        submit.click()

        try:
            link = self.driver.find_element(By.CSS_SELECTOR, "a[href='/easyquizzy/addingCategories'].icons")
            link.click()

            category = self.driver.find_element(By.ID, "Umetnost")
            category.click()

            new_img = self.driver.find_element(By.ID, "newCatImg")
            new_img.send_keys(
                "C:\\Software\\PSI\\Projekat\\project_Djangovi_OSvetnici\\Faza5\\EasyQuizzy\\static\\css\\avatar_multiplayer.png")

            submit = self.driver.find_element(By.XPATH,
                                              "//form[@action='/easyquizzy/changeExistingCategory']//button[@type='submit']")
            submit.click()
            time.sleep(2)

            message_div = self.driver.find_element(By.ID, "messageChange")
            self.assertEqual(message_div.text, "Promena je uspešno napravljena")

            category = self.driver.find_element(By.ID, "Umetnost")
            category.click()

            new_img = self.driver.find_element(By.ID, "newCatImg")
            new_img.send_keys(
                "C:\\Software\\PSI\\Projekat\\project_Djangovi_OSvetnici\\Faza5\\EasyQuizzy\\static\\css\\art.jpg")

            submit = self.driver.find_element(By.XPATH,
                                              "//form[@action='/easyquizzy/changeExistingCategory']//button[@type='submit']")
            submit.click()
            time.sleep(2)

            message_div = self.driver.find_element(By.ID, "messageChange")
            self.assertEqual(message_div.text, "Promena je uspešno napravljena")

        except BaseException as e:
            self.fail("Test failed: {e}")
        finally:
            logout_link = self.driver.find_element(By.CSS_SELECTOR, "a[href='/easyquizzy/logout'].icons")
            logout_link.click()
