from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from config import *
from words import final_words





LOGIN_URL = "https://web.telegram.org/k/"


def create_driver(options):
    return webdriver.Chrome(options=options, executable_path="chromedriver.exe")

def create_and_set_options():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    return options


def login(driver):
    driver.get(LOGIN_URL)
    sleep(7)

    driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/div/div[2]/button[1]/div").click()
    sleep(4)

    driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[2]/div[1]").send_keys(phone_number)
    driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[1]/div/div[3]/button[1]").click()
    sleep(15)



    chats = driver.find_elements(By.CLASS_NAME, "user-caption")
    chat_number = 0
    current_chat_number = 0
    for chat in chats:
        title = chat.find_element(By.CLASS_NAME, "peer-title").text


        if (title == chat_name):

            elems = driver.find_elements(By.CLASS_NAME, "c-ripple")
            for elem in elems:
                if (current_chat_number == chat_number + 2):
                    sleep(2)
                    elem.click()
                current_chat_number += 1
            break
        chat_number += 1



def get_buttons_count(driver):
    buttons = driver.find_elements(By.CLASS_NAME, "reply-markup")
    buttons_count = len(buttons)
    result = list()
    result.append( buttons_count ); result.append( buttons )

    return result

def get_last_message(driver):
    messages = driver.find_elements(By.CLASS_NAME, "message")

    itteration_counter = 0
    messages_count = len(messages)
    for message in messages:
        itteration_counter += 1
        if (itteration_counter == messages_count):
            return message.text



def main():
    try:
        options = create_and_set_options()
        driver = create_driver(options)

        login(driver)

        buttons_count = get_buttons_count(driver)[ 0 ]

        while True:
            response = get_buttons_count(driver)
            current_buttons_count = response[ 0 ]

            if (buttons_count < current_buttons_count):
                buttons = response[ 1 ]
                itteration_counter = 0
                for button in buttons:
                    is_ok = False
                    itteration_counter += 1
                    if (itteration_counter == current_buttons_count):
                        buttons_count = current_buttons_count
                        message = get_last_message(driver)
                        for final_word in final_words:
                            if (final_word in message):
                                is_ok = True
                        if (is_ok):
                            button.click()


    except Exception as ex:
        print(ex)

    finally:
        driver.close()
        driver.quit()


if __name__ == "__main__":
    main()