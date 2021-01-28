from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, \
    QCheckBox, QInputDialog, QComboBox, QPushButton, QSlider
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
import threading
import time
import os.path
import json
from copy import deepcopy


class HackingThread(threading.Thread):
    # noinspection PyAttributeOutsideInit
    def run(self):
        self.portCount = 1
        self.finished = False
        self.state = False
        self.state = ah_win.attackThState

        while self.state:
            self.state = ah_win.attackThState
            word = driver.find_element_by_xpath('//*[@id="tool-type"]/img')
            if word.get_attribute('src') != "http://s0urce.io/client/img/words/template.png":
                self.finished = False
            if ah_win.CB_AutoContinue.isChecked() and self.finished:  # hacking finished
                OtherWindow = driver.find_element_by_xpath('//*[@id="window-other"]')
                portA = driver.find_element_by_xpath('//*[@id="window-other-port1"]')
                portB = driver.find_element_by_xpath('//*[@id="window-other-port2"]')
                portC = driver.find_element_by_xpath('//*[@id="window-other-port3"]')
                hack_button = driver.find_element_by_xpath('//*[@id="window-other-button"]')
                if "display: none;" not in OtherWindow.get_attribute('style'):
                    if hack_button.get_attribute("style") != "display: none;":
                        hack_button.click()
                    if self.portCount == 1:
                        portA.click()
                    elif self.portCount == 2:
                        portB.click()
                    elif self.portCount == 3:
                        portC.click()
                    self.finished = False
            if word.get_attribute('src') != "http://s0urce.io/client/img/words/template.png":  # hacking start
                self.finished = False
            while not self.finished:  # hacking not finished
                word_inputbox = driver.find_element_by_xpath('//*[@id="tool-type-word"]')
                word = driver.find_element_by_xpath('//*[@id="tool-type"]/img')
                try:
                    typeword = word_dict[word.get_attribute('src')]
                    print('word = {}\t|\turl = {}'.format(typeword, word.get_attribute('src')))
                    word_inputbox.send_keys(typeword)
                    time.sleep(ah_win.Slider_EnterDelay.value() / 1000)
                    word_inputbox.send_keys(Keys.ENTER)
                except KeyError:
                    print("Can't find url {} in Dictionary".format(word.get_attribute('src')))
                    if word.get_attribute('src') == "http://s0urce.io/client/img/words/template.png":
                        self.finished = True
                time.sleep(ah_win.Slider_InputDelay.value() / 1000)
                success_window = driver.find_element_by_xpath('//*[@id="topwindow-success"]')
                if success_window.get_attribute('style') == "opacity: 1;":
                    success_windowclose = driver.find_element_by_xpath(
                        '//*[@id="topwindow-success"]/div/div[1]/span')
                    success_windowclose.click()
                    del success_windowclose, success_window
                    self.finished = True
                    if 0 < self.portCount < 3:
                        self.portCount += 1
                    elif self.portCount >= 3:
                        self.portCount = 1
                    else:
                        self.portCount = 1


class AutoHacker(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    # noinspection PyAttributeOutsideInit
    def initUI(self):
        self.Slider_EnterDelay = QSlider(Qt.Horizontal, self)
        # noinspection PyUnresolvedReferences
        self.Slider_EnterDelay.valueChanged.connect(self.setEDSliderValue)
        self.Slider_EnterDelay.setMaximum(3000)
        self.Slider_EnterDelay.setMinimum(200)
        self.Slider_EnterDelay.setSingleStep(200)
        self.Slider_EnterDelay.setTickInterval(200)
        self.Slider_EnterDelay.setTickPosition(1)
        self.Slider_InputDelay = QSlider(Qt.Horizontal, self)
        # noinspection PyUnresolvedReferences
        self.Slider_InputDelay.valueChanged.connect(self.setIDSliderValue)
        self.Slider_InputDelay.setMaximum(3000)
        self.Slider_InputDelay.setMinimum(500)
        self.Slider_InputDelay.setSingleStep(250)
        self.Slider_InputDelay.setTickInterval(250)
        self.Slider_InputDelay.setTickPosition(1)

        self.CB_AutoHacker = QCheckBox('AutoHacker Enable')
        # noinspection PyUnresolvedReferences
        self.CB_AutoHacker.stateChanged.connect(self.hackThread)
        self.CB_AutoContinue = QCheckBox('AutoContinue')

        self.AV_SetBox = QVBoxLayout()
        self.AV_SetBox.addWidget(self.Slider_EnterDelay)
        self.AV_SetBox.addWidget(self.Slider_InputDelay)

        box = QVBoxLayout()
        box.addWidget(self.CB_AutoHacker)
        box.addWidget(self.CB_AutoContinue)
        box.addLayout(self.AV_SetBox)

        self.setLayout(box)

        self.th = HackingThread()
        self.attackThState = False
        self.loginDiag = False

        self.setWindowTitle("SSerVe's AutoHack")
        self.setWindowIcon(QIcon('ico.png'))
        self.setGeometry(0, 0, 300, 400)
        self.show()

    # noinspection PyAttributeOutsideInit
    def hackThread(self, state):
        if state == Qt.Checked:
            self.attackThState = True
            self.th.start()
        else:
            self.attackThState = False

    # noinspection PyCallByClass
    def setInputDiag_login(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')
        if ok:
            login_nameInput = driver.find_element_by_xpath('//*[@id="login-input"]')
            login_tutorialCheckBox = driver.find_element_by_xpath('//*[@id="checkbox-tutorial"]')
            login_Button = driver.find_element_by_xpath('//*[@id="login-play"]')
            login_nameInput.send_keys(str(text))
            login_tutorialCheckBox.click()
            login_Button.click()

    def setIDSliderValue(self, val):
        self.Slider_InputDelay.setValue(val)

    def setEDSliderValue(self, val):
        self.Slider_EnterDelay.setValue(val)


class ConfigWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.outputIndex = 0
        self.cfg_len = 1
        self.cfg_list = []
        self.ScriptPath = sys.argv[0]
        self.Path = ""
        self.ConfigPath = ""
        for index, path in enumerate(self.ScriptPath.split("\\")):
            if index == len(self.ScriptPath.split("\\")) - 1:
                continue
            else:
                self.Path += (path + "/")
        self.ConfigPath = self.Path + "Config/"
        self.initUI()

    # noinspection PyUnresolvedReferences,PyAttributeOutsideInit
    def initUI(self):
        self.ConfigComboBox = QComboBox(self)
        self.updateConfigList()
        self.ConfigComboBox.activated[int].connect(self.changeInternalConfigVar)
        self.ConfigNum = 0
        self.nowApplied = 0

        self.loadButton = QPushButton("Loa&d", self)  # Load, Shortcut Alt + D
        self.saveButton = QPushButton("&Save", self)  # Save, Shortcut Alt + S
        self.createButton = QPushButton("&New Config", self)  # Create new config, Shortcut Alt + N
        self.refreshButton = QPushButton("&Refresh list", self)  # Refresh config list, Shortcut Alt + R
        self.loadButton.released.connect(self.load_apply_setting)
        self.saveButton.released.connect(self.newsaveJson)
        self.createButton.released.connect(self.createJsonWithoutsave)
        self.refreshButton.released.connect(self.updateConfigList)

        self.box = QVBoxLayout()

        self.HBoxAB = QHBoxLayout()
        self.HBoxAB.addWidget(self.ConfigComboBox)
        self.HBoxAB.addWidget(self.createButton)

        self.HBoxDN = QHBoxLayout()
        self.HBoxDN.addWidget(self.saveButton)
        self.HBoxDN.addWidget(self.loadButton)

        self.HBoxFN = QHBoxLayout()
        self.HBoxFN.addStretch(0)
        self.HBoxFN.addWidget(self.refreshButton)

        self.box.addLayout(self.HBoxAB)
        self.box.addLayout(self.HBoxDN)

        self.setLayout(self.box)

        self.setWindowTitle("Configs")
        self.setGeometry(200, 200, 300, 200)
        self.show()

    # noinspection PyAttributeOutsideInit
    def changeInternalConfigVar(self, num):
        self.ConfigNum = num

    # noinspection PyAttributeOutsideInit
    def load_apply_setting(self):
        self.nowApplied = 0
        print("Config Applying...")
        for _set in self.cfg_list[self.ConfigNum]:
            pt = self.cfg_list[self.ConfigNum][_set]
            if _set == 'AutoHacker':
                if pt["AutoHackerEnable"]:  # AutoHacker Enable
                    print("AutoHackEnable: True")
                    if not ah_win.CB_AutoHacker.isChecked():
                        print("AutoHack enabled.")
                        ah_win.CB_AutoHacker.toggle()
                    elif ah_win.CB_AutoHacker.isChecked():
                        print("AutoHack already enabled.")
                elif not pt["AutoHackerEnable"]:  # AutoHacker Disable
                    print("AutoHackerEnable: False")
                    if ah_win.CB_AutoHacker.isChecked():
                        print("AutoHack disabled.")
                        ah_win.CB_AutoHacker.toggle()
                    elif not ah_win.CB_AutoHacker.isChecked():
                        print("AutoHack already disabled.")
                if pt['AutoPortEnable']:  # AutoPort Enable
                    print("AutoPortEnable: True")
                    if not ah_win.CB_AutoContinue.isChecked():
                        print("AutoPort enabled.")
                        ah_win.CB_AutoContinue.toggle()
                    elif ah_win.CB_AutoContinue.isChecked():
                        print("AutoPort already enabled.")
                elif not pt['AutoPortEnable']:  # AutoPort Disable
                    print("AutoPortEnable: False")
                    if ah_win.CB_AutoContinue.isChecked():
                        print("AutoPort disabled.")
                        ah_win.CB_AutoContinue.toggle()
                    elif not ah_win.CB_AutoContinue.isChecked():
                        print("AutoPort already disabled.")
                ah_win.Slider_EnterDelay.setValue(int(pt["AutoHackerEnterDelay"] * 1000))
                print("EnterDelay set to {}s".format(pt["AutoHackerEnterDelay"]))
                ah_win.Slider_InputDelay.setValue(int(pt["AutoHackerInputDelay"] * 1000))
                print("InputDelay set to {}s".format(pt["AutoHackerInputDelay"]))

    def newsaveJson(self):
        AllItems = [self.ConfigComboBox.itemText(i) for i in range(self.ConfigComboBox.count())]
        llsaveJson = deepcopy(cfg_init)
        # CFG Name Setting
        text, ok = QInputDialog.getText(self, 'SAVE SETTING', 'Enter CFG name:')
        llsaveJson["Name"] = text
        # Save current setting
        AH_Dict = llsaveJson["AutoHacker"]
        AH_Dict["AutoHackerEnable"] = ah_win.CB_AutoHacker.isChecked()
        AH_Dict["AutoPortEnable"] = ah_win.CB_AutoContinue.isChecked()
        AH_Dict["AutoHackerEnterDelay"] = ah_win.Slider_EnterDelay.value() / 1000
        AH_Dict["AutoHackerInputDelay"] = ah_win.Slider_InputDelay.value() / 1000
        if ok:
            with open("{}Config_{}.cfg".format(self.ConfigPath, str(len(AllItems)+int(1))), "w") as js:
                json.dump(llsaveJson, js, indent=4)
                print("JSON Created.")
        del AllItems, llsaveJson

    def createJsonWithoutsave(self):
        AllItems = [self.ConfigComboBox.itemText(i) for i in range(self.ConfigComboBox.count())]
        with open("{}Config_{}.cfg".format(self.ConfigPath, str(len(AllItems) + 1)), "w") as js:
            json.dump(cfg_init, js, indent=4)
            self.outputIndex += 1
            print("JSON Created")
        del AllItems

    def updateConfigList(self):
        print("ConfigList Updating...")
        self.cfg_list = []
        self.cfg_len = 1
        AllItems = [self.ConfigComboBox.itemText(i) for i in range(self.ConfigComboBox.count())]
        for i in range(len(AllItems)-1, 0-1, -1):
            self.ConfigComboBox.removeItem(i)

        while True:
            if os.path.exists("{}Config_{}.cfg".format(self.ConfigPath, self.cfg_len)):
                print("Searching {}Config Files".format(self.ConfigPath))
                if self.cfg_len == 1:
                    print("Config 1st file exist.")
                elif self.cfg_len == 2:
                    print("Config 2nd file exist.")
                elif self.cfg_len == 3:
                    print("Config 3rd file exist.")
                else:
                    print("Config {}th file exist.".format(self.cfg_len))
                self.cfg_len += 1
            else:
                break
        try:
            if self.cfg_len == 0:
                self.createJsonWithoutsave()
            for cfg_num in range(1, self.cfg_len + 1):
                configPath = "{}Config_{}.cfg".format(self.ConfigPath, cfg_num)
                with open(configPath, "r", encoding="UTF-8") as file:
                    print(str(file))
                    self.cfg_list.append(json.load(file))
        except OSError:
            print("OSError, Warning")
        for index, cfg in enumerate(self.cfg_list):
            print(str(cfg))
            self.ConfigComboBox.addItem("Config {}: {}".format(index, cfg['Name']))
        print(str([self.ConfigComboBox.itemText(i) for i in range(self.ConfigComboBox.count())]))


driver = webdriver.Chrome("chromedriver")
driver.get("http://s0urce.io")

cfg_init = {
    "Name": "",
    "AutoHacker": {
        "AutoHackerEnable": False,
        "AutoHackerEnterDelay": 0.2,
        "AutoHackerInputDelay": 0.5,
        "AutoPortEnable": False
    }
}

app = QApplication(sys.argv)

config_win = ConfigWindow()
with open("{}words.json".format(config_win.Path), "r") as djson:
    word_dict = json.load(djson)
ah_win = AutoHacker()

sys.exit(app.exec_())
