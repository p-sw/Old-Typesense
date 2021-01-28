from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import sys
try:
    import dict
    _dict = True
except ImportError:
    print("Can't find WORD DICT")
    _dict = False


def init_prg():
    global driver
    driver = webdriver.Chrome("chromedriver")


def start_menu(name):
    driver.get('http://s0urce.io')
    assert "http://s0urce.io" in driver.current_url
    print("Trying to log in..")
    name_box = driver.find_element_by_xpath('//*[@id="login-input"]')
    name_box.send_keys(name)
    print("Inputting nickname...")
    tutorial_checkbox = driver.find_element_by_xpath('//*[@id="checkbox-tutorial"]')
    tutorial_checkbox.click()
    print("Tutorial Unchecking...")
    start_login = driver.find_element_by_xpath('//*[@id="login-play"]')
    start_login.click()
    print("Game Started")
    del name_box, tutorial_checkbox, start_login


def in_game():
    input("ready to hacking? (press enter)")
    portA = driver.find_element_by_xpath('//*[@id="window-other-port1"]')
    portB = driver.find_element_by_xpath('//*[@id="window-other-port2"]')
    portC = driver.find_element_by_xpath('//*[@id="window-other-port3"]')
    success_window = driver.find_element_by_xpath('//*[@id="topwindow-success"]')
    i = 1
    while True:
        hack_button = driver.find_element_by_xpath('//*[@id="window-other-button"]')
        if hack_button.get_attribute("style") != "display: none;":
            hack_button.click()
        if i == 1:
            portA.click()
        if i == 2:
            portB.click()
        if i == 3:
            portC.click()
        word_inputbox = driver.find_element_by_xpath('//*[@id="tool-type-word"]')
        while True:
            word = driver.find_element_by_xpath('//*[@id="tool-type"]/img')
            try:
                typeword = word_dict[word.get_attribute('src')]
                print('word = {}\t|\turl = {}'.format(typeword, word.get_attribute('src')))
                word_inputbox.send_keys(typeword)
                sleep(0.2)
                word_inputbox.send_keys(Keys.ENTER)
            except KeyError:
                print("Can't Find Url {} in Dictionary".format(word.get_attribute('src')))
            sleep(0.75)
            if success_window.get_attribute('style') == "opacity: 1;":  # if success window visible
                success_windowclose = driver.find_element_by_xpath('//*[@id="topwindow-success"]/div/div[1]/span')
                success_windowclose.click()
                del success_windowclose
                break

        if "-AutoContinue" not in sys.argv:
            cont = input("continue? (Y/N)::")
            if "Y" in cont or "y" in cont:
                pass
            elif "N" in cont or "n" in cont:
                break
            else:
                print("Unknown Input.")
        if 0 < i < 3:
            i += 1
        elif i >= 3:
            i = 1
        else:
            i = 1


if _dict is True:
    word_dict = dict.word_dict
elif _dict is False:
    sys.exit()
driver = None
init_prg()
nickname = str(input("Your Nickname:: "))
start_menu(nickname)
in_game()
