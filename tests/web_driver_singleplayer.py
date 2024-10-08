# Magdalena Obradović 2021/0304
# Elena Savić 2021/0332

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import os
import time


chromedriver_path = r"C:\Users\HP\Documents\SI\6. semestar\PSI\Projekat\DriverTestiranje\chromedriver-win64\chromedriver.exe"


service = ChromeService(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service)

try:
    driver.get("http://192.168.0.13:8000/easyquizzy")
    username = driver.find_element(By.NAME, "username")
    username.send_keys("meg123")
    password = driver.find_element(By.NAME, "password")
    password.send_keys("Psii123+")
    submit = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Prijavi se']")
    submit.click()

    test_button = driver.find_element(By.ID, "buttonPlay")
    test_button.click()

    single_button = driver.find_element(By.NAME, "test")
    driver.execute_script("arguments[0].click();", single_button)
    

    category = driver.find_element(By.XPATH, "//input[@type='radio' and @value='opsta']")
    category.click()

    begin_test = driver.find_element(By.XPATH, "//button[@type='button']")
    begin_test.click()

    for i in range(10):
        answer_button = driver.find_element(By.ID, "answer0")
        answer_button.click()
        time.sleep(3)
        grade_button = driver.find_element(By.XPATH, "//input[@type='radio' and @value='preskoci']")
        driver.execute_script("arguments[0].click();", grade_button)
        #grade_button.click()
        end_grading = driver.find_element(By.XPATH, "//button[@type='button']")
        end_grading.click()

    return_main = driver.find_element(By.NAME, "vrati se na pocetni")  
    return_main.click() 

    logout_link = driver.find_element(By.CSS_SELECTOR, "a[href='/easyquizzy/logout'].icons")
    logout_link.click()

    time.sleep(1)

finally:
    # Close the browser
    driver.quit()