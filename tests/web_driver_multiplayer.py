#Elena Savić 2021/0332
#Magdalena Obradović 2021/0304

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from threading import Thread
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver import Edge, EdgeOptions

import os
import requests

# Disable SSL certificate verification
requests.packages.urllib3.disable_warnings()
response = requests.get('http://192.168.0.13:8000/easyquizzy', verify=False)
response = requests.get('http://192.168.0.13:8000/easyquizzy/nextMultiplayer/1/', verify=False)
os.environ['WDM_SSL_VERIFY'] = '0'


edgedriver_path = r"C:\Users\HP\Documents\SI\6. semestar\PSI\Projekat\DriverTestiranje\msedgedriver.exe"
mozziladriver_path = r"C:\Users\HP\Documents\SI\6. semestar\PSI\Projekat\DriverTestiranje\geckodriver.exe"
chromedriver_path = r"C:\Users\HP\Documents\SI\6. semestar\PSI\Projekat\DriverTestiranje\chromedriver-win64\chromedriver.exe"

edge_options = EdgeOptions()
edge_options.add_argument("--ignore-certificate-errors--")
service = ChromeService(executable_path=chromedriver_path)
service_mozzila = FirefoxService(executable_path=mozziladriver_path)
service_edge = EdgeService(executable_path=edgedriver_path)
# driver = webdriver.Chrome(service=service)

def simulate_user(browser, room_code, my_username, my_password, other_username):
    # Open the quiz page
    browser.get('http://192.168.0.13:8000/easyquizzy')  # Change URL to your quiz page

    username = browser.find_element(By.NAME, "username")
    username.send_keys(my_username)
    password = browser.find_element(By.NAME, "password")
    password.send_keys(my_password)
    submit = browser.find_element(By.XPATH, "//input[@type='submit' and @value='Prijavi se']")
    submit.click()

    test_button = browser.find_element(By.XPATH, "//input[@type='button' and  @value='Izrada testa']")
    test_button.click()

    multiplayer_button = browser.find_element(By.XPATH, "//input[@type='radio' and  @value='small_multi']")
    # multiplayer_button.click()
    browser.execute_script("arguments[0].click();", multiplayer_button)


    input_room_code = browser.find_element(By.ID, "code")
    input_room_code.send_keys(room_code)

    begin_searching = browser.find_element(By.ID, "continue")
    begin_searching.click()

    # Enter the room code
    # room_input = browser.find_element(By.NAME, 'room_code')
    # room_input.send_keys(room_code)
    # room_input.send_keys(Keys.RETURN)

    # Simulate receiving WebSocket message by manually storing data in localStorage
    # browser.execute_script('''
    #     localStorage.setItem('quiz_data', JSON.stringify({}));
    #     document.getElementById('start_quiz_form').submit();
    # ''')

    # Wait for navigation to the next page
    WebDriverWait(browser, 30).until(
        lambda driver: driver.current_url != 'http://192.168.0.13:8000/easyquizzy/nextMultiplayer/1/'
    )

    time.sleep(5)

    # Simulate answering questions on the new page
    # for i in range(5):  # Assuming there are 5 questions
    #     question = WebDriverWait(browser, 30).until(
    #         EC.presence_of_element_located((By.ID, 'question'))
    #     )
    #     answer = browser.find_element(By.NAME, 'answer')  # Adjust as necessary
    #     answer.send_keys(f'Answer from player {player_id}')  # Simulate user input
    #     submit_button = browser.find_element(By.ID, 'submit_answer')
    #     submit_button.click()

    #     # Wait for the next question or end of quiz
    #     time.sleep(2)  # Adjust based on your application's behavior

    # # Wait for quiz results or end message
    # WebDriverWait(browser, 30).until(
    #     EC.presence_of_element_located((By.ID, 'quiz_end_message'))
    # )

if __name__ == '__main__':
    room_code = 1  # Example room code
    username1 = "meg123"
    username2 = "elena123"

    # Launch two browsers
    browser1 = webdriver.Edge(service=service_edge, options=edge_options)  # or webdriver.Firefox(), etc.
    browser2 = webdriver.Firefox(service=service_mozzila)

    try:
        # Start two threads to simulate two users
        user1 = Thread(target=simulate_user, args=(browser1, room_code, username1, "Psii123+", username2))
        user2 = Thread(target=simulate_user, args=(browser2, room_code, username2, "Psii123+", username1))

        user1.start()
        user2.start()

        user1.join()
        user2.join()

    finally:
        # Close the browsers
        browser1.quit()
        browser2.quit()
