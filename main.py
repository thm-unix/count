#!/usr/bin/python3

import os, sys
import json
import random
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import uic
from enum import Enum


main_dir = os.path.abspath(__file__)[:-7]
os.chdir(main_dir)


class releaseData(Enum):
    VERSION      = '0.1'
    PRODUCT_NAME = 'Count!'
    DEVELOPER    = 'thm'
    EMAIL        = 'highsierra.2007@mail.ru'
    WEBSITE      = 'https://thm-unix.github.io/'


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.readConfig('config.json')
        self.prepareUI()
        self.setContextMenuActions()
        self.setPushButtonsActions()
        self.setOtherActions()
        self.setLocaleStrings()

    def readConfig(self, configPath):
        with open(configPath, 'r') as configReader:
            self.config = json.load(configReader)

    def prepareUI(self):
        # load UI
        self.window = uic.loadUi('ui/main.ui')
        self.settings = uic.loadUi('ui/settings.ui')
        self.about = uic.loadUi('ui/about.ui')

        # set style
        if self.config['theme'] == 'dark':
            stylesheetReader = open('styles/dark.qss')
        else:
            stylesheetReader = open('styles/light.qss')

        self.stylesheet = stylesheetReader.read()
        stylesheetReader.close()

        self.window.setStyleSheet(self.stylesheet)
        self.settings.setStyleSheet(self.stylesheet)
        self.about.setStyleSheet(self.stylesheet)

        # set locale
        localePath = 'locales/' + self.config['locale'] + '.json'
        with open(localePath, 'r') as localeReader:
            self.localeStrings = json.load(localeReader)

        # hide all objects for now
        self.window.questionLabel.hide()
        self.window.answerTextEdit.hide()
        self.window.skipPushButton.hide()
        self.window.submitPushButton.hide()
        self.window.statusLabel.setText('Ready')

        # set icon of application
        # does it even work?
        self.window.setWindowIcon(QIcon('assets/icon.png'))
        self.settings.setWindowIcon(QIcon('assets/icon.png'))
        self.about.setWindowIcon(QIcon('assets/icon.png'))

        self.about.iconLabel.setPixmap(QPixmap('assets/icon.png'))

        # set version
        self.about.softwareNameLabel.setText(releaseData.PRODUCT_NAME.value)
        self.about.versionLabel.setText('v.' + releaseData.VERSION.value)
        self.about.developerNameLabel.setText(self.localeStrings['wasBroughtToYou'] + releaseData.DEVELOPER.value)
        self.about.developerEmailLabel.setText(releaseData.EMAIL.value)
        self.about.developerWebsiteLabel.setText(releaseData.WEBSITE.value)

        # show UI
        self.window.show()

    def setLocaleStrings(self):
        self.window.menuFile.setTitle(self.localeStrings['menuFile'])
        self.window.newGameAction.setText(self.localeStrings['newGameAction'])
        self.window.settingsAction.setText(self.localeStrings['settingsAction'])
        self.window.exitAction.setText(self.localeStrings['exitAction'])
        self.window.menuInformation.setTitle(self.localeStrings['menuInformation'])
        self.window.aboutAction.setText(self.localeStrings['aboutAction'])
        self.window.answerTextEdit.setPlaceholderText(self.localeStrings['answerTextEdit'])
        self.window.statusLabel.setText(self.localeStrings['statusLabel_ready'])
        self.window.skipPushButton.setText(self.localeStrings['skipPushButton'])
        self.window.submitPushButton.setText(self.localeStrings['submitPushButton'])
        self.settings.languageGroupBox.setTitle(self.localeStrings['languageGroupBox'])
        self.settings.themeGroupBox.setTitle(self.localeStrings['themeGroupBox'])
        self.settings.lightRadioButton.setText(self.localeStrings['lightRadioButton'])
        self.settings.darkRadioButton.setText(self.localeStrings['darkRadioButton'])
        self.settings.difficultyGroupBox.setTitle(self.localeStrings['difficultyGroupBox'])
        self.settings.easyRadioButton.setText(self.localeStrings['easyRadioButton'])
        self.settings.mediumRadioButton.setText(self.localeStrings['mediumRadioButton'])
        self.settings.hardRadioButton.setText(self.localeStrings['hardRadioButton'])
        self.settings.tasksAmountGroupBox.setTitle(self.localeStrings['tasksAmountGroupBox'])
        self.settings.cancelPushButton.setText(self.localeStrings['cancelPushButton'])
        self.settings.savePushButton.setText(self.localeStrings['savePushButton'])

    def quit(self):
        exit()

    def generateRandomTask(self, difficulty):
        if difficulty == 1:
            operands = ['+', '-']
            numbers = [i for i in range(0, 30)]

            randomA = numbers[random.randint(0, len(numbers)-1)]
            randomB = numbers[random.randint(0, len(numbers)-1)]
            randomOperand = random.randint(0, 1)

            return (randomA, operands[randomOperand], randomB)

        elif difficulty == 2:
            operands = ['+', '-', '*', '/']
            numbersGeneral = [i for i in range(0, 70)]
            numbersMultiply = [i for i in range(2, 10)]
            numbersDivision = [i for i in range(1, 50)]

            self.randomOperand = random.randint(0, 3)
            if self.randomOperand in range(0,2):
                self.randomA = numbersGeneral[random.randint(0, len(numbersGeneral)-1)]
                self.randomB = numbersGeneral[random.randint(0, len(numbersGeneral)-1)]

            elif self.randomOperand == 2:
                self.randomA = numbersMultiply[random.randint(0, len(numbersMultiply)-1)]
                self.randomB = numbersMultiply[random.randint(0, len(numbersMultiply)-1)]

            elif self.randomOperand == 3:
                self.randomA = numbersDivision[random.randint(0, len(numbersDivision)-1)]
                self.randomB = numbersDivision[random.randint(0, len(numbersDivision)-1)]
                while self.randomA % self.randomB != 0 or self.randomA == self.randomB:
                    self.randomA = numbersDivision[random.randint(0, len(numbersDivision)-1)]
                    self.randomB = numbersDivision[random.randint(0, len(numbersDivision)-1)]

            return (self.randomA, operands[self.randomOperand], self.randomB)

        elif difficulty == 3:
            operands = ['+', '-', '*', '/', '^']
            numbers = [i for i in range(20, 100)]
            numbersPow = [i for i in range(2, 6)]

            self.randomOperand = random.randint(0, 4)
            if self.randomOperand in range(0,3):
                self.randomA = numbers[random.randint(0, len(numbers)-1)]
                self.randomB = numbers[random.randint(0, len(numbers)-1)]
            elif self.randomOperand == 3:
                self.randomA = numbers[random.randint(0, len(numbers)-1)]
                self.randomB = numbers[random.randint(0, len(numbers)-1)]
                while self.randomA % self.randomB != 0 or self.randomA == self.randomB:
                    self.randomA = numbers[random.randint(0, len(numbers)-1)]
                    self.randomB = numbers[random.randint(0, len(numbers)-1)]
            elif self.randomOperand == 4:
                self.randomA = numbersPow[random.randint(0, len(numbersPow)-1)]
                self.randomB = numbersPow[random.randint(0, len(numbersPow)-1)]

            return (self.randomA, operands[self.randomOperand], self.randomB)

    def showNewTask(self):
        # self.window.statusLabel.setText('Generating new task...')
        self.myTask = self.generateRandomTask(self.config['difficulty'])
        self.taskShownInUI = str(self.myTask[0]) + ' ' + str(self.myTask[1]) + ' ' + \
                             str(self.myTask[2]) + ' = ?'
        self.window.questionLabel.setText(self.taskShownInUI)
        # self.window.statusLabel.setText('Waiting for answer...')
        self.tasksShownCount += 1

    def newGame(self):
        self.tasksShownCount = 0
        self.correctTasksCount = 0

        self.window.questionLabel.show()
        self.window.answerTextEdit.show()
        self.window.skipPushButton.show()
        self.window.submitPushButton.show()

        self.window.statusLabel.setText(self.localeStrings['statusLabel_start'])

        self.showNewTask()

    def openSettingsWindow(self):
        self.settings.show()

        # set switches in current position
        if self.config['locale'] == 'us':
            self.settings.englishRadioButton.toggle()
        elif self.config['locale'] == 'ru':
            self.settings.russianRadioButton.toggle()

        if self.config['theme'] == 'dark':
            self.settings.darkRadioButton.toggle()
        else:
            self.settings.lightRadioButton.toggle()

        if self.config['difficulty'] == 1:
            self.settings.easyRadioButton.toggle()
        elif self.config['difficulty'] == 2:
            self.settings.mediumRadioButton.toggle()
        elif self.config['difficulty'] == 3:
            self.settings.hardRadioButton.toggle()

        self.settings.tasksDial.setValue(self.config['tasks'])
        self.settings.tasksLCD.display(self.config['tasks'])

    def changeLCDValue(self, value):
        self.settings.tasksLCD.display(value)

    def saveSettingsToConfig(self):
        self._locale,self._theme,self._difficulty,self._tasks = '','',0,0

        if self.settings.englishRadioButton.isChecked():
            self._locale = 'us'
        elif self.settings.russianRadioButton.isChecked():
            self._locale = 'ru'

        self._theme = 'dark' if self.settings.darkRadioButton.isChecked() else 'light'

        if self.settings.easyRadioButton.isChecked():
            self._difficulty = 1
        elif self.settings.mediumRadioButton.isChecked():
            self._difficulty = 2
        elif self.settings.hardRadioButton.isChecked():
            self._difficulty = 3

        self._tasks = self.settings.tasksDial.value()


        configData = {
            'difficulty': self._difficulty,
            'tasks': self._tasks,
            'theme': self._theme,
            'locale': self._locale
        }

        with open('config.json', 'w') as configWriter:
            json.dump(configData, configWriter)


        QMessageBox.information(self, self.localeStrings['informationTitle'], \
            self.localeStrings['restartCountMessage'], QMessageBox.Ok)
        exit()


    def showResults(self):
        QMessageBox.information(self, self.localeStrings['informationTitle'], \
            self.localeStrings['solvedMessage'] + str(self.correctTasksCount) + '/' + \
            str(self.tasksShownCount), QMessageBox.Ok)

        self.window.answerTextEdit.clear()
        self.window.questionLabel.hide()
        self.window.answerTextEdit.hide()
        self.window.skipPushButton.hide()
        self.window.submitPushButton.hide()
        self.window.statusLabel.setText('Ready')

    def skipTask(self):
        if self.tasksShownCount < self.config['tasks']:
            self.showNewTask()
        else:
            self.showResults()

    def checkAnswer(self, userAnswer, task):
        correctString = self.localeStrings['statusLabel_correct']
        incorrectString = self.localeStrings['statusLabel_incorrect']

        a = self.myTask[0]
        operand = self.myTask[1]
        b = self.myTask[2]

        if operand == '+':
            if userAnswer == str(a + b):
                self.correctTasksCount += 1
                if self.tasksShownCount < self.config['tasks']:
                    self.window.statusLabel.setText(correctString)
                    self.showNewTask()
                    self.window.answerTextEdit.clear()
                else:
                    self.showResults()
            else:
                if self.tasksShownCount < self.config['tasks']:
                    self.window.statusLabel.setText(incorrectString)
                    self.showNewTask()
                    self.window.answerTextEdit.clear()
                else:
                    self.showResults()
        elif operand == '-':
            if userAnswer == str(a - b):
                self.correctTasksCount += 1
                if self.tasksShownCount < self.config['tasks']:
                    self.window.statusLabel.setText(correctString)
                    self.showNewTask()
                    self.window.answerTextEdit.clear()
                else:
                    self.showResults()
            else:
                if self.tasksShownCount < self.config['tasks']:
                    self.window.statusLabel.setText(incorrectString)
                    self.showNewTask()
                    self.window.answerTextEdit.clear()
                else:
                    self.showResults()
        elif operand == '*':
            if userAnswer == str(a * b):
                self.correctTasksCount += 1
                if self.tasksShownCount < self.config['tasks']:
                    self.window.statusLabel.setText(correctString)
                    self.showNewTask()
                    self.window.answerTextEdit.clear()
                else:
                    self.showResults()
            else:
                if self.tasksShownCount < self.config['tasks']:
                    self.window.statusLabel.setText(incorrectString)
                    self.showNewTask()
                    self.window.answerTextEdit.clear()
                else:
                    self.showResults()
        elif operand == '/':
            if userAnswer == str(a // b):
                self.correctTasksCount += 1
                if self.tasksShownCount < self.config['tasks']:
                    self.window.statusLabel.setText(correctString)
                    self.showNewTask()
                    self.window.answerTextEdit.clear()
                else:
                    self.showResults()
            else:
                if self.tasksShownCount < self.config['tasks']:
                    self.window.statusLabel.setText(incorrectString)
                    self.showNewTask()
                    self.window.answerTextEdit.clear()
                else:
                    self.showResults()
        elif operand == '^':
            if userAnswer == str(a ** b):
                self.correctTasksCount += 1
                if self.tasksShownCount < self.config['tasks']:
                    self.window.statusLabel.setText(correctString)
                    self.showNewTask()
                    self.window.answerTextEdit.clear()
                else:
                    self.showResults()
            else:
                if self.tasksShownCount < self.config['tasks']:
                    self.window.statusLabel.setText(incorrectString)
                    self.showNewTask()
                    self.window.answerTextEdit.clear()
                else:
                    self.showResults()


    def setContextMenuActions(self):
        self.window.exitAction.triggered.connect(lambda:self.quit())
        self.window.newGameAction.triggered.connect(lambda:self.newGame())
        self.window.settingsAction.triggered.connect(
                                            lambda:self.openSettingsWindow())
        self.window.aboutAction.triggered.connect(
                                            lambda:self.about.show())

    def setPushButtonsActions(self):
        self.window.submitPushButton.clicked.connect(lambda:self.checkAnswer(
                        self.window.answerTextEdit.toPlainText(), self.myTask))
        self.window.skipPushButton.clicked.connect(lambda:self.skipTask())

        self.settings.cancelPushButton.clicked.connect(lambda:self.settings.hide())
        self.settings.savePushButton.clicked.connect(lambda:self.saveSettingsToConfig())

    def setOtherActions(self):
        self.settings.tasksDial.valueChanged.connect(
                            lambda:self.changeLCDValue(
                                            self.settings.tasksDial.value()))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    app.exec_()
