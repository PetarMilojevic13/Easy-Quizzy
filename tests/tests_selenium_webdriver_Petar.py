# Petar Milojević 2021/0336
import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService

#http://127.0.0.1:8000/easyquizzy/
#C:\Users\Petar\OneDrive\Desktop\Faza5\chromedriver-win64\chromedriver.exe


class TP1_PregledKategorije_Gost(LiveServerTestCase):

    def test_login(self):
        chromedriver_path = r"C:\Users\Petar\OneDrive\Desktop\Faza5\chromedriver-win64\chromedriver.exe"

        service = ChromeService(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service)

        driver.implicitly_wait(100)
        driver.get("http://127.0.0.1:8000/easyquizzy/login")

        time.sleep(2)
        prijava_gost = driver.find_element(By.ID, 'pocetnaGost')
        prijava_gost.click()
        driver.get("http://127.0.0.1:8000/easyquizzy/loginAsGuest")
        #driver.refresh()
        time.sleep(2)

        links = driver.find_elements(By.TAG_NAME, 'a')

        # Ispisati URL adrese svih pronađenih linkova
        for link in links:
            if link.get_attribute("href")=="http://127.0.0.1:8000/easyquizzy/categories":
                link.click()
                time.sleep(2)
                break

        self.assertTrue(driver.current_url == "http://127.0.0.1:8000/easyquizzy/categories")

        driver.quit()



class TP2_PregledKategorije_Registrovan(LiveServerTestCase):

    def test_login(self):
        chromedriver_path = r"C:\Users\Petar\OneDrive\Desktop\Faza5\chromedriver-win64\chromedriver.exe"

        service = ChromeService(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service)



        driver.implicitly_wait(100)
        driver.get("http://127.0.0.1:8000/easyquizzy/login")

        time.sleep(2)

        korime = driver.find_element(By.NAME, 'username')
        sifra = driver.find_element(By.NAME, 'password')
        korime.send_keys("elena123")
        time.sleep(2)
        sifra.send_keys("Psii123+")
        time.sleep(2)

        inputi = driver.find_elements(By.TAG_NAME, 'input')
        for input in inputi:
            if input.get_attribute("value")=="Prijavi se":
                input.click()

        time.sleep(2)
        #driver.get("http://127.0.0.1:8000/easyquizzy/main")
        #driver.refresh()
        time.sleep(2)

        links = driver.find_elements(By.TAG_NAME, 'a')

        # Ispisati URL adrese svih pronađenih linkova
        for link in links:
            if link.get_attribute("href")=="http://127.0.0.1:8000/easyquizzy/categories":
                link.click()
                time.sleep(2)
                break

        self.assertTrue(driver.current_url == "http://127.0.0.1:8000/easyquizzy/categories")

        links = driver.find_elements(By.TAG_NAME, 'a')

        for link in links:

            if link.get_attribute("href")=="http://127.0.0.1:8000/easyquizzy/logout":
                link.click()
                time.sleep(3)
                break


        driver.quit()

'''class TP3_RegistracijaUspesna(LiveServerTestCase):

    def test_login(self):
        driver = webdriver.Chrome()

        driver.implicitly_wait(100)
        driver.get("http://127.0.0.1:8000/easyquizzy/login")

        time.sleep(2)


        inputi = driver.find_elements(By.TAG_NAME, 'a')
        for input in inputi:
            if input.get_attribute("href")=="register":
                input.click()
                break


        time.sleep(2)
        driver.get("http://127.0.0.1:8000/easyquizzy/register")
        #driver.refresh()
        time.sleep(2)

        username = driver.find_element(By.NAME, 'username')
        username.send_keys("proba123")

        name = driver.find_element(By.NAME, 'name')
        name.send_keys("Proba")

        surname = driver.find_element(By.NAME, 'surname')
        surname.send_keys("Proba")

        email = driver.find_element(By.NAME, 'email')
        email.send_keys("proba@etf.rs")


        gender = driver.find_element(By.ID, 'm')
        gender.click()

        password = driver.find_element(By.NAME, 'password')
        password.send_keys("Psii123+")

        passwordVal = driver.find_element(By.NAME, 'passwordVal')
        passwordVal.send_keys("Psii123+")

        button = driver.find_element(By.ID, 'sub')
        button.click()


       # print(driver.current_url)
        self.assertTrue(driver.current_url == "http://127.0.0.1:8000/easyquizzy/register")
        driver.quit()
        
class TP4_RegistracijaNeuspesna(LiveServerTestCase):

    def test_login(self):
        driver = webdriver.Chrome()

        driver.implicitly_wait(100)
        driver.get("http://127.0.0.1:8000/easyquizzy/login")

        time.sleep(2)


        inputi = driver.find_elements(By.TAG_NAME, 'a')
        for input in inputi:
            if input.get_attribute("href")=="register":
                input.click()
                break


        time.sleep(2)
        driver.get("http://127.0.0.1:8000/easyquizzy/register")
        #driver.refresh()
        time.sleep(2)

        username = driver.find_element(By.NAME, 'username')
        username.send_keys("proba123")

        name = driver.find_element(By.NAME, 'name')
        name.send_keys("Proba")

        surname = driver.find_element(By.NAME, 'surname')
        surname.send_keys("Proba")

        email = driver.find_element(By.NAME, 'email')
        email.send_keys("proba@etf.rs")


        gender = driver.find_element(By.ID, 'm')
        gender.click()

        password = driver.find_element(By.NAME, 'password')
        password.send_keys("Psii123+")

        passwordVal = driver.find_element(By.NAME, 'passwordVal')
        passwordVal.send_keys("Psii123+")

        button = driver.find_element(By.ID, 'sub')
        button.click()
        time.sleep(2)

       # print(driver.current_url)
        self.assertTrue(driver.current_url == "http://127.0.0.1:8000/easyquizzy/register")
        driver.quit()'''


class TP3_DodavanjeModeratoraUspesnoPutemTabele(LiveServerTestCase):

    def test_login(self):
        chromedriver_path = r"C:\Users\Petar\OneDrive\Desktop\Faza5\chromedriver-win64\chromedriver.exe"

        service = ChromeService(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service)

        driver.implicitly_wait(100)
        driver.get("http://127.0.0.1:8000/easyquizzy/login")

        time.sleep(2)

        korime = driver.find_element(By.NAME, 'username')
        sifra = driver.find_element(By.NAME, 'password')
        korime.send_keys("meg123")
        time.sleep(2)
        sifra.send_keys("Psii123+")
        time.sleep(2)

        inputi = driver.find_elements(By.TAG_NAME, 'input')
        for input in inputi:
            if input.get_attribute("value") == "Prijavi se":
                input.click()

        time.sleep(2)
        # driver.get("http://127.0.0.1:8000/easyquizzy/main")
        # driver.refresh()
        time.sleep(2)

        links = driver.find_elements(By.TAG_NAME, 'a')

        # Ispisati URL adrese svih pronađenih linkova
        for link in links:
            if link.get_attribute("href") == "http://127.0.0.1:8000/easyquizzy/users":
                link.click()
                time.sleep(2)
                break

        radiodugme = driver.find_element(By.ID, 'ilija123')
        radiodugme.click()

        dodajmoderatora = driver.find_element(By.ID, 'moderatorButton')
        dodajmoderatora.click()
        time.sleep(2)
        uloga = driver.find_element(By.ID, 'roleilija123')
        self.assertTrue(uloga.text=='moderator')
        links = driver.find_elements(By.TAG_NAME, 'a')

        for link in links:

            if link.get_attribute("href")=="http://127.0.0.1:8000/easyquizzy/logout":
                link.click()
                time.sleep(3)
                break


        driver.quit()


class TP4_DodavanjeModeratoraUspesnoMetodomUnosa(LiveServerTestCase):

    def test_login(self):
        chromedriver_path = r"C:\Users\Petar\OneDrive\Desktop\Faza5\chromedriver-win64\chromedriver.exe"

        service = ChromeService(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service)

        driver.implicitly_wait(100)
        driver.get("http://127.0.0.1:8000/easyquizzy/login")

        time.sleep(2)

        korime = driver.find_element(By.NAME, 'username')
        sifra = driver.find_element(By.NAME, 'password')
        korime.send_keys("meg123")
        time.sleep(2)
        sifra.send_keys("Psii123+")
        time.sleep(2)

        inputi = driver.find_elements(By.TAG_NAME, 'input')
        for input in inputi:
            if input.get_attribute("value") == "Prijavi se":
                input.click()

        time.sleep(2)
        # driver.get("http://127.0.0.1:8000/easyquizzy/main")
        # driver.refresh()
        time.sleep(2)

        links = driver.find_elements(By.TAG_NAME, 'a')

        # Ispisati URL adrese svih pronađenih linkova
        for link in links:
            if link.get_attribute("href") == "http://127.0.0.1:8000/easyquizzy/users":
                link.click()
                time.sleep(2)
                break



        unosime = driver.find_element(By.ID, 'inputUser')
        unosime.send_keys("petar123")



        dodajmoderatora = driver.find_element(By.ID, 'moderatorButton')
        dodajmoderatora.click()

        time.sleep(2)
        uloga = driver.find_element(By.ID, 'rolepetar123')
        self.assertTrue(uloga.text=='moderator')

        links = driver.find_elements(By.TAG_NAME, 'a')

        for link in links:

            if link.get_attribute("href")=="http://127.0.0.1:8000/easyquizzy/logout":
                link.click()
                time.sleep(3)
                break


        driver.quit()


class TP5_DodavanjeModeratoraNeuspesnoKorisnikVecModerator(LiveServerTestCase):

    def test_login(self):
        chromedriver_path = r"C:\Users\Petar\OneDrive\Desktop\Faza5\chromedriver-win64\chromedriver.exe"

        service = ChromeService(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service)

        driver.implicitly_wait(100)
        driver.get("http://127.0.0.1:8000/easyquizzy/login")

        time.sleep(2)

        korime = driver.find_element(By.NAME, 'username')
        sifra = driver.find_element(By.NAME, 'password')
        korime.send_keys("meg123")
        time.sleep(2)
        sifra.send_keys("Psii123+")
        time.sleep(2)

        inputi = driver.find_elements(By.TAG_NAME, 'input')
        for input in inputi:
            if input.get_attribute("value") == "Prijavi se":
                input.click()

        time.sleep(2)
        # driver.get("http://127.0.0.1:8000/easyquizzy/main")
        # driver.refresh()
        time.sleep(2)

        links = driver.find_elements(By.TAG_NAME, 'a')

        # Ispisati URL adrese svih pronađenih linkova
        for link in links:
            if link.get_attribute("href") == "http://127.0.0.1:8000/easyquizzy/users":
                link.click()
                time.sleep(2)
                break



        unosime = driver.find_element(By.ID, 'inputUser')
        unosime.send_keys("elena123")

        dodajmoderatora = driver.find_element(By.ID, 'moderatorButton')
        dodajmoderatora.click()

        #Ne znam kako message da uhvatim
        poruka = driver.find_element(By.ID, 'errorMessage')
        self.assertTrue(poruka.text=="Izabrani korisnik već ima ulogu moderatora")
        time.sleep(2)

        links = driver.find_elements(By.TAG_NAME, 'a')

        for link in links:

            if link.get_attribute("href") == "http://127.0.0.1:8000/easyquizzy/logout":
                link.click()
                time.sleep(3)
                break

        driver.quit()


class TP6_DodavanjeModeratoraNeuspesnoNepostojeciKorisnik(LiveServerTestCase):

    def test_login(self):
        chromedriver_path = r"C:\Users\Petar\OneDrive\Desktop\Faza5\chromedriver-win64\chromedriver.exe"

        service = ChromeService(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service)

        driver.implicitly_wait(100)
        driver.get("http://127.0.0.1:8000/easyquizzy/login")

        time.sleep(2)

        korime = driver.find_element(By.NAME, 'username')
        sifra = driver.find_element(By.NAME, 'password')
        korime.send_keys("meg123")
        time.sleep(2)
        sifra.send_keys("Psii123+")
        time.sleep(2)

        inputi = driver.find_elements(By.TAG_NAME, 'input')
        for input in inputi:
            if input.get_attribute("value") == "Prijavi se":
                input.click()

        time.sleep(2)
        # driver.get("http://127.0.0.1:8000/easyquizzy/main")
        # driver.refresh()
        time.sleep(2)

        links = driver.find_elements(By.TAG_NAME, 'a')

        # Ispisati URL adrese svih pronađenih linkova
        for link in links:
            if link.get_attribute("href") == "http://127.0.0.1:8000/easyquizzy/users":
                link.click()
                time.sleep(2)
                break



        unosime = driver.find_element(By.ID, 'inputUser')
        unosime.send_keys("nepostojeci")

        dodajmoderatora = driver.find_element(By.ID, 'moderatorButton')
        dodajmoderatora.click()


        poruka = driver.find_element(By.ID, 'errorMessage')
        self.assertTrue(poruka.text=="Korisnik sa unetim korisničkim imenom ne postoji")
        time.sleep(2)

        links = driver.find_elements(By.TAG_NAME, 'a')

        for link in links:

            if link.get_attribute("href") == "http://127.0.0.1:8000/easyquizzy/logout":
                link.click()
                time.sleep(3)
                break

        driver.quit()


class TP7_DodavanjeModeratoraBezIzboraKorisnika(LiveServerTestCase):

    def test_login(self):
        chromedriver_path = r"C:\Users\Petar\OneDrive\Desktop\Faza5\chromedriver-win64\chromedriver.exe"

        service = ChromeService(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service)

        driver.implicitly_wait(100)
        driver.get("http://127.0.0.1:8000/easyquizzy/login")

        time.sleep(2)

        korime = driver.find_element(By.NAME, 'username')
        sifra = driver.find_element(By.NAME, 'password')
        korime.send_keys("meg123")
        time.sleep(2)
        sifra.send_keys("Psii123+")
        time.sleep(2)

        inputi = driver.find_elements(By.TAG_NAME, 'input')
        for input in inputi:
            if input.get_attribute("value") == "Prijavi se":
                input.click()

        time.sleep(2)
        # driver.get("http://127.0.0.1:8000/easyquizzy/main")
        # driver.refresh()
        time.sleep(2)

        links = driver.find_elements(By.TAG_NAME, 'a')

        # Ispisati URL adrese svih pronađenih linkova
        for link in links:
            if link.get_attribute("href") == "http://127.0.0.1:8000/easyquizzy/users":
                link.click()
                time.sleep(2)
                break


        dodajmoderatora = driver.find_element(By.ID, 'moderatorButton')
        dodajmoderatora.click()

        poruka = driver.find_element(By.ID, 'errorMessage')
        self.assertTrue(poruka.text == "Niste izabrali korisnika koga želite postavite za moderatora")
        time.sleep(2)

        links = driver.find_elements(By.TAG_NAME, 'a')

        for link in links:

            if link.get_attribute("href") == "http://127.0.0.1:8000/easyquizzy/logout":
                link.click()
                time.sleep(3)
                break

        driver.quit()





class TP8_BrisanjeKorisnikaUspesnoPutemTabele(LiveServerTestCase):

    def test_login(self):
        chromedriver_path = r"C:\Users\Petar\OneDrive\Desktop\Faza5\chromedriver-win64\chromedriver.exe"

        service = ChromeService(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service)

        driver.implicitly_wait(100)
        driver.get("http://127.0.0.1:8000/easyquizzy/login")

        time.sleep(2)

        korime = driver.find_element(By.NAME, 'username')
        sifra = driver.find_element(By.NAME, 'password')
        korime.send_keys("meg123")
        time.sleep(2)
        sifra.send_keys("Psii123+")
        time.sleep(2)

        inputi = driver.find_elements(By.TAG_NAME, 'input')
        for input in inputi:
            if input.get_attribute("value") == "Prijavi se":
                input.click()

        time.sleep(2)
        # driver.get("http://127.0.0.1:8000/easyquizzy/main")
        # driver.refresh()
        time.sleep(2)

        links = driver.find_elements(By.TAG_NAME, 'a')

        # Ispisati URL adrese svih pronađenih linkova
        for link in links:
            if link.get_attribute("href") == "http://127.0.0.1:8000/easyquizzy/users":
                link.click()
                time.sleep(2)
                break

        radiodugme = driver.find_element(By.ID, 'petar123')
        radiodugme.click()

        dodajmoderatora = driver.find_element(By.ID, 'deleteButton')
        dodajmoderatora.click()
        time.sleep(2)
        yesdugme = driver.find_element(By.ID, 'yesButton')
        yesdugme.click()

        time.sleep(2)
        celije = driver.find_elements(By.TAG_NAME, 'td')

        for cel in celije:
            if cel.text=="petar123":
                self.assertTrue(driver.current_url == "http://127.0.0.1:8000/easyquizzy/categories")
                time.sleep(2)
                driver.quit()

        self.assertTrue(driver.current_url=="http://127.0.0.1:8000/easyquizzy/users")
        time.sleep(2)

        links = driver.find_elements(By.TAG_NAME, 'a')

        for link in links:

            if link.get_attribute("href") == "http://127.0.0.1:8000/easyquizzy/logout":
                link.click()
                time.sleep(3)
                break

        driver.quit()


class TP9_BrisanjeKorisnikaUspesnoMetodomUnosa(LiveServerTestCase):

    def test_login(self):
        chromedriver_path = r"C:\Users\Petar\OneDrive\Desktop\Faza5\chromedriver-win64\chromedriver.exe"

        service = ChromeService(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service)

        driver.implicitly_wait(100)
        driver.get("http://127.0.0.1:8000/easyquizzy/login")

        time.sleep(2)

        korime = driver.find_element(By.NAME, 'username')
        sifra = driver.find_element(By.NAME, 'password')
        korime.send_keys("meg123")
        time.sleep(2)
        sifra.send_keys("Psii123+")
        time.sleep(2)

        inputi = driver.find_elements(By.TAG_NAME, 'input')
        for input in inputi:
            if input.get_attribute("value") == "Prijavi se":
                input.click()

        time.sleep(2)
        # driver.get("http://127.0.0.1:8000/easyquizzy/main")
        # driver.refresh()
        time.sleep(2)

        links = driver.find_elements(By.TAG_NAME, 'a')

        # Ispisati URL adrese svih pronađenih linkova
        for link in links:
            if link.get_attribute("href") == "http://127.0.0.1:8000/easyquizzy/users":
                link.click()
                time.sleep(2)
                break



        unosime = driver.find_element(By.ID, 'inputUser')
        unosime.send_keys("petar123")

        dodajmoderatora = driver.find_element(By.ID, 'deleteButton')
        dodajmoderatora.click()
        time.sleep(2)
        yesdugme = driver.find_element(By.ID, 'yesButton')
        yesdugme.click()

        time.sleep(2)
        celije = driver.find_elements(By.TAG_NAME, 'td')

        for cel in celije:
            if cel.text=="petar123":
                self.assertTrue(driver.current_url == "http://127.0.0.1:8000/easyquizzy/categories")
                time.sleep(2)
                driver.quit()

        self.assertTrue(driver.current_url=="http://127.0.0.1:8000/easyquizzy/users")
        time.sleep(2)
        links = driver.find_elements(By.TAG_NAME, 'a')

        for link in links:

            if link.get_attribute("href") == "http://127.0.0.1:8000/easyquizzy/logout":
                link.click()
                time.sleep(3)
                break

        driver.quit()


class TP10_BrisanjeKorisnikaNeuspesnoNepostojeci(LiveServerTestCase):

    def test_login(self):
        chromedriver_path = r"C:\Users\Petar\OneDrive\Desktop\Faza5\chromedriver-win64\chromedriver.exe"

        service = ChromeService(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service)

        driver.implicitly_wait(100)
        driver.get("http://127.0.0.1:8000/easyquizzy/login")

        time.sleep(2)

        korime = driver.find_element(By.NAME, 'username')
        sifra = driver.find_element(By.NAME, 'password')
        korime.send_keys("meg123")
        time.sleep(2)
        sifra.send_keys("Psii123+")
        time.sleep(2)

        inputi = driver.find_elements(By.TAG_NAME, 'input')
        for input in inputi:
            if input.get_attribute("value") == "Prijavi se":
                input.click()

        time.sleep(2)
        # driver.get("http://127.0.0.1:8000/easyquizzy/main")
        # driver.refresh()
        time.sleep(2)

        links = driver.find_elements(By.TAG_NAME, 'a')

        # Ispisati URL adrese svih pronađenih linkova
        for link in links:
            if link.get_attribute("href") == "http://127.0.0.1:8000/easyquizzy/users":
                link.click()
                time.sleep(2)
                break



        unosime = driver.find_element(By.ID, 'inputUser')
        unosime.send_keys("nepostojeci")

        dodajmoderatora = driver.find_element(By.ID, 'deleteButton')
        dodajmoderatora.click()

        yesdugme = driver.find_element(By.ID, 'yesButton')
        yesdugme.click()

        poruka = driver.find_element(By.ID, 'errorMessage')
        self.assertTrue(poruka.text == "Ne postoji korisnik koga želite da obrišete")
        time.sleep(2)
        links = driver.find_elements(By.TAG_NAME, 'a')

        for link in links:

            if link.get_attribute("href") == "http://127.0.0.1:8000/easyquizzy/logout":
                link.click()
                time.sleep(3)
                break

        driver.quit()

class TP11_BrisanjeKorisnikaNeuspesnoKorisnikNijeIzabran(LiveServerTestCase):

    def test_login(self):
        chromedriver_path = r"C:\Users\Petar\OneDrive\Desktop\Faza5\chromedriver-win64\chromedriver.exe"

        service = ChromeService(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service)

        driver.implicitly_wait(100)
        driver.get("http://127.0.0.1:8000/easyquizzy/login")

        time.sleep(2)

        korime = driver.find_element(By.NAME, 'username')
        sifra = driver.find_element(By.NAME, 'password')
        korime.send_keys("meg123")
        time.sleep(2)
        sifra.send_keys("Psii123+")
        time.sleep(2)

        inputi = driver.find_elements(By.TAG_NAME, 'input')
        for input in inputi:
            if input.get_attribute("value") == "Prijavi se":
                input.click()

        time.sleep(2)
        # driver.get("http://127.0.0.1:8000/easyquizzy/main")
        # driver.refresh()
        time.sleep(2)

        links = driver.find_elements(By.TAG_NAME, 'a')

        # Ispisati URL adrese svih pronađenih linkova
        for link in links:
            if link.get_attribute("href") == "http://127.0.0.1:8000/easyquizzy/users":
                link.click()
                time.sleep(2)
                break

        dodajmoderatora = driver.find_element(By.ID, 'deleteButton')
        dodajmoderatora.click()
        time.sleep(2)
        yesdugme = driver.find_element(By.ID, 'yesButton')
        yesdugme.click()

        poruka = driver.find_element(By.ID, 'errorMessage')
        self.assertTrue(poruka.text == "Niste izabrali korisnika koga želite da obrišete")
        time.sleep(2)



        links = driver.find_elements(By.TAG_NAME, 'a')

        for link in links:

            if link.get_attribute("href") == "http://127.0.0.1:8000/easyquizzy/logout":
                link.click()
                time.sleep(3)
                break

        driver.quit()


class TP12_BrisanjeKorisnikaNeuspesnoAdministratorOdustaje(LiveServerTestCase):

    def test_login(self):
        chromedriver_path = r"C:\Users\Petar\OneDrive\Desktop\Faza5\chromedriver-win64\chromedriver.exe"

        service = ChromeService(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service)

        driver.implicitly_wait(100)
        driver.get("http://127.0.0.1:8000/easyquizzy/login")

        time.sleep(2)

        korime = driver.find_element(By.NAME, 'username')
        sifra = driver.find_element(By.NAME, 'password')
        korime.send_keys("meg123")
        time.sleep(2)
        sifra.send_keys("Psii123+")
        time.sleep(2)

        inputi = driver.find_elements(By.TAG_NAME, 'input')
        for input in inputi:
            if input.get_attribute("value") == "Prijavi se":
                input.click()

        time.sleep(2)
        # driver.get("http://127.0.0.1:8000/easyquizzy/main")
        # driver.refresh()
        time.sleep(2)

        links = driver.find_elements(By.TAG_NAME, 'a')

        # Ispisati URL adrese svih pronađenih linkova
        for link in links:
            if link.get_attribute("href") == "http://127.0.0.1:8000/easyquizzy/users":
                link.click()
                time.sleep(2)
                break

        dodajmoderatora = driver.find_element(By.ID, 'deleteButton')
        dodajmoderatora.click()
        time.sleep(2)
        nodugme = driver.find_element(By.ID, 'noButton')
        nodugme.click()

        self.assertTrue(driver.current_url=="http://127.0.0.1:8000/easyquizzy/users")
        time.sleep(2)
        links = driver.find_elements(By.TAG_NAME, 'a')

        for link in links:

            if link.get_attribute("href") == "http://127.0.0.1:8000/easyquizzy/logout":
                link.click()
                time.sleep(3)
                break

        driver.quit()
