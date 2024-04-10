from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QGraphicsDropShadowEffect, QStackedWidget, QVBoxLayout, QFrame, QMessageBox, QDialog, QPlainTextEdit, QPushButton, QComboBox
from PyQt5.QtCore import QTimer, QDateTime, Qt, QLocale
from PyQt5.QtGui import QColor, QFontDatabase, QFont, QPixmap
from PyQt5.uic import loadUi
import DataBase
import sys
import re
import datetime
import random

class RejisterPage(QWidget):
    def __init__(self):
        super(RejisterPage, self).__init__()
        loadUi("./ui/registerPage.ui", self)
        self.shadow()
        self.stacked()
        self.fonts()
        self.labels()
        self.buttons()

    def fonts(self):
        tanha = QFontDatabase.addApplicationFont('./font/Tanha.ttf')
        self.tanha = QFontDatabase.applicationFontFamilies(tanha)

    def shadow(self):
        self.shadow1 = QGraphicsDropShadowEffect(self)
        self.shadow1.setBlurRadius(15)
        self.shadow1.setColor(QColor(54, 54, 54).lighter())
        self.shadow1.setOffset(0)

        self.mainFram.setGraphicsEffect(self.shadow1)

    def stacked(self):
        self.stack = QStackedWidget()
        self.stack.addWidget(Login())
        self.stack.addWidget(SignUp())
        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.rightFrame.setLayout(layout)

    def labels(self):
        self.iconLabel.setPixmap(QPixmap('./image/appIcon.png'))
        self.appNameLabel.setFont(QFont(self.tanha[0],18))
        self.shortDecLabel.setFont(QFont(self.tanha[0],11))

    def buttons(self):
        self.signUpButton.setFont(QFont(self.tanha[0],10))
        self.signInButton.setFont(QFont(self.tanha[0], 10))

        self.signUpButton.clicked.connect(self.singupPage)
        self.signInButton.clicked.connect(self.singInPage)

    # ---------------------------------------------------------------------------

    def singupPage(self):
        self.stack.setCurrentIndex(1)

    def singInPage(self):
        self.stack.setCurrentIndex(0)

class Login(QWidget):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("./ui/login.ui", self)
        self.fonts()
        self.labels()
        self.lineEdits()
        self.pushButton()

    def fonts(self):
        tanha = QFontDatabase.addApplicationFont('./font/Tanha.ttf')
        self.tanha = QFontDatabase.applicationFontFamilies(tanha)

    def labels(self):
        self.titleLabel.setFont(QFont(self.tanha[0],20))
        self.commentLabel.setFont(QFont(self.tanha[0],10))
        self.userNameLabel.setFont(QFont(self.tanha[0],10))
        self.passwordLabel.setFont(QFont(self.tanha[0],10))

        self.errorLabel.setFont(QFont(self.tanha[0],10))

    def lineEdits(self):
        self.userNameLineEdit.setFont(QFont(self.tanha[0],10))
        self.passwordLineEdit.setFont(QFont(self.tanha[0],10))

    def pushButton(self):
        self.loginBtn.setFont(QFont(self.tanha[0],14))
        self.loginBtn.clicked.connect(self.checkUser)

    #===================================================#
    def checkUser(self):
        allUser = DataBase.checkUser()
        for user in allUser:
            if user['userName'] == self.userNameLineEdit.text() and user['password'] == self.passwordLineEdit.text():
                self.errorLabel.setText('')
                loggedUser['id'] = user['id']
                loggedUser['userName'] = user['userName']
                loggedUser['password'] = user['password']
                loggedUser['score'] = user['score']
                loggedUser['class'] = user['class']
                loggedUser['email'] = user['email']
                loggedUser['profileImage'] = user['profileImage']

                mainWindow.show()
                rejisterWindow.close()

            else:
                self.errorLabel.setText('نام کاربری یا رمز عبور اشتباه است')

class SignUp(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('./ui/signUp.ui',self)
        self.numbersCheckResult = False
        self.spiecialCharacterCheckResult = False
        self.capitalLettersCheckResult = False
        self.widthCheckResult = False

        self.fonts()
        self.labels()
        self.butten()
        self.lineEdits()

    def fonts(self):
        tanha = QFontDatabase.addApplicationFont('./font/Tanha.ttf')
        self.tanha = QFontDatabase.applicationFontFamilies(tanha)

    def labels(self):
        self.title.setFont(QFont(self.tanha[0],20))
        self.shortDec.setFont(QFont(self.tanha[0],10))
        self.userName.setFont(QFont(self.tanha[0],10))
        self.password.setFont(QFont(self.tanha[0],10))
        self.rePassword.setFont(QFont(self.tanha[0],10))
        self.widthText.setFont(QFont(self.tanha[0],8))
        self.numText.setFont(QFont(self.tanha[0],8))
        self.specText.setFont(QFont(self.tanha[0],8))
        self.capText.setFont(QFont(self.tanha[0],8))

        self.userNameErrorLabel.setFont(QFont(self.tanha[0],8))
        self.passwoedValidErrorLabel.setFont(QFont(self.tanha[0],8))
        self.samePasswordErrorLabel.setFont(QFont(self.tanha[0],8))

        self.numbersCheck.setPixmap(QPixmap('./image/cross.png'))
        self.spiecialCharacterCheck.setPixmap(QPixmap('./image/cross.png'))
        self.capitalLettersCheck.setPixmap(QPixmap('./image/cross.png'))
        self.widthCheck.setPixmap(QPixmap('./image/cross.png'))

    def lineEdits(self):
        self.userNameLineEdit.setFont(QFont(self.tanha[0], 8))
        self.passwordLineEdit.textChanged.connect(self.validat)

    def butten(self):
        self.singUpBtn.setFont(QFont(self.tanha[0], 14))
        self.singUpBtn.clicked.connect(self.saveUser)

    # -------------------------------------------------------------------------------
    def validat(self):
        password = self.passwordLineEdit.text()

        if re.findall(".{8,}$", password):
            self.widthCheck.setPixmap(QPixmap('./image/accept.png'))
            self.widthCheckResult = True
        else:
            self.widthCheck.setPixmap(QPixmap('./image/cross.png'))
            self.widthCheckResult = False

        if re.findall("^(?=.* ?[A-Z])(?=.* ?[a-z])", password):
            self.capitalLettersCheck.setPixmap(QPixmap('./image/accept.png'))
            self.capitalLettersCheckResult = True
        else:
            self.capitalLettersCheck.setPixmap(QPixmap('./image/cross.png'))
            self.capitalLettersCheckResult = False

        if re.findall("(?=.* ?[0-9])", password):
            self.numbersCheck.setPixmap(QPixmap('./image/accept.png'))
            self.numbersCheckResult = True
        else:
            self.numbersCheck.setPixmap(QPixmap('./image/cross.png'))
            self.numbersCheckResult = False

        if re.findall("(?=.*?[#?!@$%^&*-])", password):
            self.spiecialCharacterCheck.setPixmap(QPixmap('./image/accept.png'))
            self.spiecialCharacterCheckResult = True
        else:
            self.spiecialCharacterCheck.setPixmap(QPixmap('./image/cross.png'))
            self.spiecialCharacterCheckResult = False

    def saveUser(self):
        allUser= DataBase.checkUserName()
        userName = self.userNameLineEdit.text()
        password = self.passwordLineEdit.text()
        rePassword = self.repeatPasswordLineEdit.text()

        userNameValid = False
        passwordValid = False
        rePasswordValid = False
        if userName.replace(' ',''):
            if userName not in allUser:
                self.userNameErrorLabel.setText('')
                userNameValid = True
            else:
                self.userNameErrorLabel.setText('این نام کاربری قبلا انتخاب شده است')
        else:
            self.userNameErrorLabel.setText('نام کاربری نباید خالی باشد')

        if self.numbersCheckResult and self.spiecialCharacterCheckResult and self.capitalLettersCheckResult and self.widthCheckResult:
            self.passwoedValidErrorLabel.setText('')
            passwordValid = True
        else:
            self.passwoedValidErrorLabel.setText('رمز عبور باید بصورت گفته شده وارد شود')

        if password == rePassword:
            self.samePasswordErrorLabel.setText('')
            rePasswordValid = True
        else:
            self.samePasswordErrorLabel.setText('پسورد و تکرار آن مطابقت ندارد')

        if userNameValid and passwordValid and rePasswordValid:
            massage = QMessageBox(self)
            massage.setText('آیا از اطلاعت وارد شده مطمئن هستید؟')
            massage.setIcon(QMessageBox.Warning)
            massage.setWindowTitle('مهم')
            massage.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            anwser = massage.exec()
            if anwser == QMessageBox.Ok:
                DataBase.createAccount(userName, password)
                self.userNameLineEdit.setText('')
                self.passwordLineEdit.setText('')
                self.repeatPasswordLineEdit.setText('')
                massage2 = QMessageBox(self)
                massage2.setText('حساب کاربری شما ایجاد شد.')
                massage2.setStandardButtons(QMessageBox.Ok)
                massage2.exec()

class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        loadUi('./ui/mainPage.ui', self)
        self.shadows()
        self.fonts()
        self.lineEdit()
        self.comboBox()
        self.labels()
        self.buttons()

    def shadows(self):
        self.shadow1 = QGraphicsDropShadowEffect(self)
        self.shadow1.setBlurRadius(12)
        self.shadow1.setColor(QColor(150, 150, 150).darker())
        self.shadow1.setOffset(0)

        self.searchFrame.setGraphicsEffect(self.shadow1)

    def showEvent(self, event):
        self.profileNameLabel.setText(str(loggedUser['userName']))
        self.profileScoreLabel.setText(f' امتیاز:{loggedUser["score"]}')

        row = 0
        column = 0
        exams = DataBase.gotAllExams()
        for exam in exams:
            card = CardFrame(exam)
            self.contectLayout.addWidget(card, row, column)
            column += 1
            if column == 1:
                row += 1
                column = 0

    def fonts(self):
        tanha = QFontDatabase.addApplicationFont('./font/Tanha.ttf')
        self.tanha = QFontDatabase.applicationFontFamilies(tanha)

    def lineEdit(self):
        self.searchLineEdit.setFont(QFont(self.tanha[0],10))

    def labels(self):
        self.profileNameLabel.setFont(QFont(self.tanha[0],11))
        self.profileScoreLabel.setFont(QFont(self.tanha[0],11))

        self.classLabel.setFont(QFont(self.tanha[0],10))

        self.profileImageLabel.setPixmap(QPixmap('./image/personIcon.png'))

    def buttons(self):
        self.ratingTableButton.setFont(QFont(self.tanha[0],10))
        self.profileSettingButton.setFont(QFont(self.tanha[0],10))
        self.searchButton.setFont(QFont(self.tanha[0],10))

        self.profileSettingButton.clicked.connect(self.showProfileSettingPage)

        self.searchButton.clicked.connect(self.searchInExams)

    def comboBox(self):
        self.classComboBox.setFont(QFont(self.tanha[0],10))

    #=========================================================#
    def showProfileSettingPage(self):
        profileSettingWindow.show()

    def searchInExams(self):
        while self.contectLayout.count():
            cardFrame = self.contectLayout.takeAt(0)
            if cardFrame.widget():
                cardFrame.widget().deleteLater()

        row = 0
        column = 0
        exams = DataBase.filterExames(self.searchLineEdit.text(), self.classComboBox.currentText())
        for exam in exams:
            card = CardFrame(exam)
            self.contectLayout.addWidget(card, row, column)
            column += 1
            if column == 1:
                row += 1
                column = 0

class ProfileSetting(QWidget):
    def __init__(self):
        super(ProfileSetting, self).__init__()
        loadUi('./ui/profileSetting.ui', self)
        self.fonts()
        self.labels()
        self.lineEdits()
        self.buttons()
        self.comboBox()

    def showEvent(self, event):
        self.userNameLineEdit.setText(loggedUser['userName'])
        self.scoreLineEdit.setText(f'امتیاز:{loggedUser["score"]}')

        self.emailLineEdit.setText(loggedUser['email'])
        if loggedUser['class'] == '':
            self.classComboBox.setCurrentText('خالی')
        else:
            self.classComboBox.setCurrentText(loggedUser['class'])

    def fonts(self):
        tanha = QFontDatabase.addApplicationFont('./font/Tanha.ttf')
        self.tanha = QFontDatabase.applicationFontFamilies(tanha)

    def labels(self):
        self.emailLabel.setFont(QFont(self.tanha[0],10))
        self.classLabel.setFont(QFont(self.tanha[0],10))

    def lineEdits(self):
        self.userNameLineEdit.setFont(QFont(self.tanha[0],10))
        self.scoreLineEdit.setFont(QFont(self.tanha[0],10))

        self.emailLineEdit.setFont(QFont(self.tanha[0],10))

    def buttons(self):
        self.saveButton.setFont(QFont(self.tanha[0],10))
        self.changeUserNameButton.setFont(QFont(self.tanha[0],10))
        self.changePasswordButton.setFont(QFont(self.tanha[0],10))
        self.changeProfileImageButton.setFont(QFont(self.tanha[0],10))

        self.saveButton.clicked.connect(self.saveInfo)
        self.changeUserNameButton.clicked.connect(self.showChangeUserNameWindow)
        self.changePasswordButton.clicked.connect(self.showChangePasswordWindow)

    def comboBox(self):
        self.classComboBox.setFont(QFont(self.tanha[0],10))

    #=======================================================#
    def saveInfo(self):
        newEmail = self.emailLineEdit.text()
        newClass = self.classComboBox.currentText()

        if newEmail != loggedUser['email'] or newClass != loggedUser['class']:
            massage = QMessageBox(self)
            massage.setText('آیا از اطلاعت وارد شده مطمئن هستید؟')
            massage.setIcon(QMessageBox.Warning)
            massage.setWindowTitle('مهم')
            massage.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            anwser = massage.exec()
            if anwser == QMessageBox.Ok:
                DataBase.updateEmailAndClass(loggedUser['userName'], newEmail, newClass)
                loggedUser['email'] = newEmail
                loggedUser['class'] = newClass

    def showChangeUserNameWindow(self):
        changeUserNameWindow.show()

    def showChangePasswordWindow(self):
        changePasswordWindow.show()

class ChangeUserName(QDialog):
    def __init__(self):
        super(ChangeUserName, self).__init__()
        loadUi('./ui/changeUserName.ui', self)
        self.userNameValid = True
        self.allUser = DataBase.checkUserName()
        self.fonts()
        self.labels()
        self.lineEdit()
        self.buttons()

    def showEvent(self, event):
        self.userNameLineEdit.setText(loggedUser['userName'])

    def fonts(self):
        tanha = QFontDatabase.addApplicationFont('./font/Tanha.ttf')
        self.tanha = QFontDatabase.applicationFontFamilies(tanha)

    def lineEdit(self):
        self.userNameLineEdit.setFont(QFont(self.tanha[0], 10))

        self.userNameLineEdit.textChanged.connect(self.checkUserName)

    def labels(self):
        self.titleLabel.setFont(QFont(self.tanha[0], 10))
        self.errorLabel.setFont(QFont(self.tanha[0], 10))

        self.checkUserNameIcon.setPixmap(QPixmap('./image/accept.png'))

    def buttons(self):
        self.buttonBox.clicked.connect(self.saveNewUserName)

    #======================================================#
    def checkUserName(self):
        text = self.userNameLineEdit.text()
        if text in self.allUser:
            if text == loggedUser['userName']:
                self.checkUserNameIcon.setPixmap(QPixmap('./image/accept.png'))
                self.userNameValid = True
            else:
                self.checkUserNameIcon.setPixmap(QPixmap('./image/cross.png'))
                self.userNameValid = False
                self.errorLabel.setText('این نام کاربری قبلا انتخاب شده است. نام کاربری ثبت نخواهد شد.')
        else:
            self.checkUserNameIcon.setPixmap(QPixmap('./image/accept.png'))
            self.userNameValid = True
            self.errorLabel.setText('')


    def saveNewUserName(self, button):
        if button.text() == 'OK':
            if self.userNameValid == True:
                if self.userNameLineEdit.text() != loggedUser['userName']:
                    DataBase.updateUserName(loggedUser['userName'], self.userNameLineEdit.text())
                    loggedUser['userName'] = self.userNameLineEdit.text()
                    mainWindow.profileNameLabel.setText(str(loggedUser['userName']))
                    profileSettingWindow.userNameLineEdit.setText(loggedUser['userName'])

class ChangePassword(QDialog):
    def __init__(self):
        super(ChangePassword, self).__init__()
        loadUi('./ui/changePassword.ui', self)
        self.widthCheckResult = False
        self.capitalLettersCheckResult = False
        self.numbersCheckResult = False
        self.spiecialCharacterCheckResult = False
        self.rePasswordCheckResult = False

        self.fonts()
        self.labels()
        self.lineEdits()
        self.buttons()

    def fonts(self):
        tanha = QFontDatabase.addApplicationFont('./font/Tanha.ttf')
        self.tanha = QFontDatabase.applicationFontFamilies(tanha)

    def labels(self):
        self.titleLabel.setFont(QFont(self.tanha[0], 10))
        self.passwordLabel.setFont(QFont(self.tanha[0], 10))
        self.rePasswordLabel.setFont(QFont(self.tanha[0], 10))

        self.passwordErrorLabel.setFont(QFont(self.tanha[0], 10))
        self.rePasswordErrorLabel.setFont(QFont(self.tanha[0], 10))

        self.widthCheck.setPixmap(QPixmap('./image/cross.png'))
        self.capitalLettersCheck.setPixmap(QPixmap('./image/cross.png'))
        self.numbersCheck.setPixmap(QPixmap('./image/cross.png'))
        self.spiecialCharacterCheck.setPixmap(QPixmap('./image/cross.png'))

        self.widthText.setFont(QFont(self.tanha[0], 8))
        self.numText.setFont(QFont(self.tanha[0], 8))
        self.specText.setFont(QFont(self.tanha[0], 8))
        self.capText.setFont(QFont(self.tanha[0], 8))

    def lineEdits(self):
        self.passwordLineEdit.setFont(QFont(self.tanha[0], 10))
        self.rePasswordLineEdit.setFont(QFont(self.tanha[0], 10))

        self.passwordLineEdit.textChanged.connect(self.passwordValidat)
        self.rePasswordLineEdit.textChanged.connect(self.rePasswordValidat)

    def buttons(self):
        self.buttonBox.clicked.connect(self.saveNewPassword)

    #===========================================================#
    def passwordValidat(self):
        password = self.passwordLineEdit.text()

        if re.findall(".{8,}$", password):
            self.widthCheck.setPixmap(QPixmap('./image/accept.png'))
            self.widthCheckResult = True
        else:
            self.widthCheck.setPixmap(QPixmap('./image/cross.png'))
            self.widthCheckResult = False

        if re.findall("^(?=.* ?[A-Z])(?=.* ?[a-z])", password):
            self.capitalLettersCheck.setPixmap(QPixmap('./image/accept.png'))
            self.capitalLettersCheckResult = True
        else:
            self.capitalLettersCheck.setPixmap(QPixmap('./image/cross.png'))
            self.capitalLettersCheckResult = False

        if re.findall("(?=.* ?[0-9])", password):
            self.numbersCheck.setPixmap(QPixmap('./image/accept.png'))
            self.numbersCheckResult = True
        else:
            self.numbersCheck.setPixmap(QPixmap('./image/cross.png'))
            self.numbersCheckResult = False

        if re.findall("(?=.*?[#?!@$%^&*-])", password):
            self.spiecialCharacterCheck.setPixmap(QPixmap('./image/accept.png'))
            self.spiecialCharacterCheckResult = True
        else:
            self.spiecialCharacterCheck.setPixmap(QPixmap('./image/cross.png'))
            self.spiecialCharacterCheckResult = False

        if self.widthCheckResult and self.capitalLettersCheckResult and self.numbersCheckResult and self.spiecialCharacterCheckResult:
            self.passwordErrorLabel.setText('')
        else:
            self.passwordErrorLabel.setText('رمز عبور وارد شده شرایط لازم را ندارد. رمز عبور جدید ثبت نخواهد شد.')

    def rePasswordValidat(self):
        if self.rePasswordLineEdit.text() == self.passwordLineEdit.text():
            self.rePasswordCheckResult = True
            self.rePasswordErrorLabel.setText('')
        else:
            self.rePasswordCheckResult = False
            self.rePasswordErrorLabel.setText('رمز عبور و تکرار آن مطابقت ندارد. رمز عبور جدید ثبت نخواهد شد.')

    def saveNewPassword(self, button):
        if button.text() == 'OK':
            if self.passwordLineEdit.text() != loggedUser['password']:
                if self.widthCheckResult and self.capitalLettersCheckResult and self.numbersCheckResult and self.spiecialCharacterCheckResult:
                    DataBase.updatePassword(loggedUser['userName'], self.passwordLineEdit.text())
                    loggedUser['password'] = self.passwordLineEdit.text()

class CardFrame(QFrame):
    def __init__(self, exam):
        super(CardFrame, self).__init__()
        loadUi('./ui/cardFrame2.ui',self)
        self.exam = exam
        self.userDoExame = DataBase.checkUserDoExame(loggedUser['id'], self.exam['id'])
        self.fonts()
        self.shadows()
        self.labels()
        self.button()

    def fonts(self):
        tanha = QFontDatabase.addApplicationFont('./font/Tanha.ttf')
        self.tanha = QFontDatabase.applicationFontFamilies(tanha)

    def shadows(self):
        self.shadow1 = QGraphicsDropShadowEffect(self)
        self.shadow1.setBlurRadius(12)
        self.shadow1.setColor(QColor(150, 150, 150).darker())
        self.shadow1.setOffset(0)

        self.shadow2 = QGraphicsDropShadowEffect(self)
        self.shadow2.setBlurRadius(5)
        self.shadow2.setColor(QColor(93, 93, 93).darker())
        self.shadow2.setOffset(0)

        # self.setGraphicsEffect(self.shadow1)
        self.showMoreButton.setGraphicsEffect(self.shadow2)

    def labels(self):
        self.cardTitle.setFont(QFont(self.tanha[0], 12))
        self.cardShortDes.setFont(QFont(self.tanha[0], 9))
        self.scoreLabel.setFont(QFont(self.tanha[0], 9))
        self.questionsCountLabel.setFont(QFont(self.tanha[0], 9))
        self.classLabel.setFont(QFont(self.tanha[0], 9))

        if self.userDoExame:
            self.errorLabel.setText('شما قبلا این آزمون را انجام داده اید')

        self.cardTitle.setText(self.exam['examTitle'])
        self.cardShortDes.setText(self.exam['examInfo'])
        self.scoreLabel.setText(f'امتیاز:{str(self.exam["examScore"])}')
        self.questionsCountLabel.setText(f'تعداد سوال:{str(self.exam["examQuestionsCount"])}')
        self.classLabel.setText(f'پایه:{str(self.exam["examClass"])}')

        self.imageLabel.setPixmap(QPixmap('./image/article2.jpg'))

    def button(self):
        self.showMoreButton.setFont(QFont(self.tanha[0], 9))
        if self.userDoExame:
            self.showMoreButton.setEnabled(False)

        self.showMoreButton.clicked.connect(self.showExameDetail)

    #============================================================#
    def showExameDetail(self):
        selectedExam['id'] = str(self.exam['id'])
        selectedExam['examTitle'] = self.exam['examTitle']
        selectedExam['examClass'] = self.exam['examClass']
        selectedExam['examInfo'] = self.exam['examInfo']
        selectedExam['examScore'] = str(self.exam['examScore'])
        selectedExam['examQuestionsCount'] = str(self.exam['examQuestionsCount'])
        selectedExam['examTime'] = self.exam['examTime']
        selectedExam['examMaker'] = self.exam['examMaker']
        exameDetailWindow.show()


class ExameDetail(QWidget):
    def __init__(self):
        super(ExameDetail, self).__init__()
        loadUi('./ui/exameDetailPage.ui', self)
        self.fonts()
        self.labels()
        self.button()
        self.shadows()

    def showEvent(self, e):
        self.titleLabel.setText(selectedExam['examTitle'])
        self.exameInfoLabel.setText(selectedExam['examInfo'])
        self.timeLabel.setText(f'زمان آزمون: {selectedExam["examTime"]}')
        self.scoreLabel.setText(f'مقدار امتیاز: {selectedExam["examScore"]}')
        self.numQuestionlabel.setText(f'تعداد سوال: {selectedExam["examQuestionsCount"]}')
        self.classLabel.setText(f'پایه: {selectedExam["examClass"]}')
        self.makerLabel.setText(f'طراح سوال: {selectedExam["examMaker"]}')

    def fonts(self):
        tanha = QFontDatabase.addApplicationFont('./font/Tanha.ttf')
        self.tanha = QFontDatabase.applicationFontFamilies(tanha)

    def shadows(self):
        self.shadow1 = QGraphicsDropShadowEffect(self)
        self.shadow1.setBlurRadius(5)
        self.shadow1.setColor(QColor(93, 93, 93).darker())
        self.shadow1.setOffset(0)

        self.shadow2 = QGraphicsDropShadowEffect(self)
        self.shadow2.setBlurRadius(5)
        self.shadow2.setColor(QColor(93, 93, 93).darker())
        self.shadow2.setOffset(0)

        self.shadow3 = QGraphicsDropShadowEffect(self)
        self.shadow3.setBlurRadius(5)
        self.shadow3.setColor(QColor(93, 93, 93).darker())
        self.shadow3.setOffset(0)

        self.shadow4 = QGraphicsDropShadowEffect(self)
        self.shadow4.setBlurRadius(5)
        self.shadow4.setColor(QColor(93, 93, 93).darker())
        self.shadow4.setOffset(0)

        self.shadow5 = QGraphicsDropShadowEffect(self)
        self.shadow5.setBlurRadius(5)
        self.shadow5.setColor(QColor(93, 93, 93).darker())
        self.shadow5.setOffset(0)

        self.shadow6 = QGraphicsDropShadowEffect(self)
        self.shadow6.setBlurRadius(5)
        self.shadow6.setColor(QColor(93, 93, 93).darker())
        self.shadow6.setOffset(0)

        self.shadow7 = QGraphicsDropShadowEffect(self)
        self.shadow7.setBlurRadius(5)
        self.shadow7.setColor(QColor(93, 93, 93).darker())
        self.shadow7.setOffset(0)


        self.exameInfoLabel.setGraphicsEffect(self.shadow1)
        self.timeLabel.setGraphicsEffect(self.shadow2)
        self.scoreLabel.setGraphicsEffect(self.shadow3)
        self.numQuestionlabel.setGraphicsEffect(self.shadow4)
        self.startExameButton.setGraphicsEffect(self.shadow5)
        self.classLabel.setGraphicsEffect(self.shadow6)
        self.makerLabel.setGraphicsEffect(self.shadow7)

    def labels(self):
        self.titleLabel.setFont(QFont(self.tanha[0], 13))
        self.exameInfoLabel.setFont(QFont(self.tanha[0], 10))
        self.timeLabel.setFont(QFont(self.tanha[0], 10))
        self.scoreLabel.setFont(QFont(self.tanha[0], 10))
        self.numQuestionlabel.setFont(QFont(self.tanha[0], 10))
        self.classLabel.setFont(QFont(self.tanha[0], 10))
        self.makerLabel.setFont(QFont(self.tanha[0], 10))

    def button(self):
        self.startExameButton.setFont(QFont(self.tanha[0], 13))
        self.startExameButton.clicked.connect(self.startExam)

    #==========================================================#
    def startExam(self):
        examePageWindow.show()
        mainWindow.close()
        self.close()

class ExamePage(QWidget):
    def __init__(self):
        super(ExamePage, self).__init__()
        loadUi('./ui/examePage.ui', self)
        self.fonts()
        self.timer()
        self.labels()
        self.questionsList()
        self.buttons()
        self.anweredCount = 0

    def showEvent(self, e):
        self.targetTime = QDateTime.currentDateTime().addSecs(int(selectedExam['examTime']) * 60)
        self.examTimer.start()

        self.answeredLabel.setText(f'{self.anweredCount} از {selectedExam["examQuestionsCount"]}')

        questions = random.sample(DataBase.gotExamQuestions(selectedExam['id']), k=int(selectedExam['examQuestionsCount']))
        index = 1
        for question in questions:
            currentExamQuestions.append({'idInExam': index, 'id': question['id'], 'question': question['question'], 'optionOne': question['optionOne'], 'optionTwo': question['optionTwo'], 'optionThree': question['optionThree'], 'optionFour': question['optionFour'], 'anwser': question['anwser'], 'score': question['score'], 'isAnwsered': False, 'userAnwser': ''})
            index += 1
        for question in currentExamQuestions:
            self.questionsStackedWidget.addWidget(QuestionFrame(question))

    def fonts(self):
        tanha = QFontDatabase.addApplicationFont('./font/Tanha.ttf')
        self.tanha = QFontDatabase.applicationFontFamilies(tanha)

    def timer(self):
        self.examTimer = QTimer(self)
        self.examTimer.setInterval(1000)
        self.examTimer.timeout.connect(self.checkTime)

    def labels(self):
        self.timeLabel.setFont(QFont(self.tanha[0], 10))
        self.questionsLabel.setFont(QFont(self.tanha[0], 10))
        self.answeredLabel.setFont(QFont(self.tanha[0], 10))

    def questionsList(self):
        self.questionsStackedWidget = QStackedWidget(self)
        self.questionsLayout.addWidget(self.questionsStackedWidget)

    def buttons(self):
        self.nextButton.setFont(QFont(self.tanha[0], 10))
        self.previousButton.setFont(QFont(self.tanha[0], 10))
        self.finishButton.setFont(QFont(self.tanha[0], 10))

        self.nextButton.clicked.connect(lambda : self.changeQuestion('next'))
        self.previousButton.clicked.connect(lambda : self.changeQuestion('previous'))
        self.finishButton.clicked.connect(self.finishExame)

    #=============================================================#
    def changeQuestion(self, event):
        if event == 'next':
            self.questionsStackedWidget.setCurrentIndex(self.questionsStackedWidget.currentIndex() + 1)
        else:
            self.questionsStackedWidget.setCurrentIndex(self.questionsStackedWidget.currentIndex() - 1)
        # count = 0
        # for question in currentExamQuestions:
        #     if question['userAnwser']:
        #         count += 1
        # self.anweredCount = count
        # self.answeredLabel.setText(f'{self.anweredCount} از {selectedExam["examQuestionsCount"]}')


    def checkTime(self):
        now = QDateTime.currentDateTime()
        timeLeft = now.secsTo(self.targetTime)
        timeLeftStr = str(datetime.timedelta(seconds=max(0, timeLeft)))

        self.timeLabel.setText(timeLeftStr)

        if timeLeft <= 0:
            self.timeLabel.setText('End')
            self.finishExame()

    def finishExame(self):
        self.examTimer.stop()
        DataBase.saveUsersDoExame(loggedUser['id'], selectedExam['id'])
        noneAnwser = 0
        rightAnwser = 0
        wrongAnwser = 0
        scoreGot = 0
        for question in currentExamQuestions:
            if question['isAnwsered'] == False:
                noneAnwser += 1
            elif str(question['anwser']) == str(question['userAnwser']):
                rightAnwser +=1
                scoreGot += int(question['score'])
            elif str(question['anwser']) != str(question['userAnwser']):
                wrongAnwser += 1


        DataBase.updateScore(loggedUser['id'], loggedUser['score'], scoreGot)
        loggedUser['score'] = int(loggedUser['score']) + scoreGot

        finishedExameInfo['scoreGot'] = scoreGot
        finishedExameInfo['wrongAnwser'] = wrongAnwser
        finishedExameInfo['rightAnwser'] = rightAnwser
        finishedExameInfo['noneAnwser'] = noneAnwser

        currentExamQuestions.clear()

        for i in range(self.questionsStackedWidget.count()):
            widget = self.questionsStackedWidget.widget(i)
            widget.deleteLater()

        self.close()
        examResultWindow.show()



class QuestionFrame(QFrame):
    def __init__(self, question):
        super(QuestionFrame, self).__init__()
        loadUi('./ui/questionFrame.ui', self)
        self.question = question
        self.fonts()
        self.lineEdits()
        self.buttons()

    def fonts(self):
        tanha = QFontDatabase.addApplicationFont('./font/Tanha.ttf')
        self.tanha = QFontDatabase.applicationFontFamilies(tanha)

        self.anwserLabel.setFont(QFont(self.tanha[0], 10))

    def lineEdits(self):
        self.questionTextEdit.setFont(QFont(self.tanha[0], 10))
        self.anwserLineEdit.setFont(QFont(self.tanha[0], 10))

        self.questionTextEdit.setText(f'{self.question["idInExam"]}- {self.question["question"]}\n\n1: {self.question["optionOne"]}\n2: {self.question["optionTwo"]}\n3: {self.question["optionThree"]}\n4: {self.question["optionFour"]}')

    def buttons(self):
        self.optionOneButton.setFont(QFont(self.tanha[0], 10))
        self.optionTwoButton.setFont(QFont(self.tanha[0], 10))
        self.optionThreeButton.setFont(QFont(self.tanha[0], 10))
        self.optionFourButton.setFont(QFont(self.tanha[0], 10))

        self.optionOneButton.clicked.connect(lambda : self.addAnwser('1'))
        self.optionTwoButton.clicked.connect(lambda: self.addAnwser('2'))
        self.optionThreeButton.clicked.connect(lambda: self.addAnwser('3'))
        self.optionFourButton.clicked.connect(lambda: self.addAnwser('4'))

    #============================================================#
    def addAnwser(self, anwser):
        self.anwserLineEdit.setText(f'گزینه{anwser}')
        for question in currentExamQuestions:
            if question['id'] == self.question['id']:
                question['userAnwser'] = anwser
                question['isAnwsered'] = True
                examePageWindow.anweredCount += 1
                examePageWindow.answeredLabel.setText(f'{examePageWindow.anweredCount} از {selectedExam["examQuestionsCount"]}')


class ExamResult(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('./ui/examResultPage.ui', self)
        self.fonts()
        self.shadows()
        self.labels()
        self.lineEdits()
        self.button()

    def fonts(self):
        tanha = QFontDatabase.addApplicationFont('./font/Tanha.ttf')
        self.tanha = QFontDatabase.applicationFontFamilies(tanha)

    def showEvent(self, e):
        self.examTitleLineEdit.setText(str(selectedExam['examTitle']))
        self.examMakerLineEdit.setText(str(selectedExam['examMaker']))
        self.userScoreLineEdit.setText(str(finishedExameInfo['scoreGot']))
        self.noneAnwserCountLineEdit.setText(str(finishedExameInfo['noneAnwser']))
        self.rightAnwserCountLineEdit.setText(str(finishedExameInfo['rightAnwser']))
        self.wrongAnwserLineEdit.setText(str(finishedExameInfo['wrongAnwser']))

    def shadows(self):
        self.shadow1 = QGraphicsDropShadowEffect(self)
        self.shadow1.setBlurRadius(5)
        self.shadow1.setColor(QColor(93, 93, 93).darker())
        self.shadow1.setOffset(0)

        self.shadow2 = QGraphicsDropShadowEffect(self)
        self.shadow2.setBlurRadius(5)
        self.shadow2.setColor(QColor(93, 93, 93).darker())
        self.shadow2.setOffset(0)

        self.shadow3 = QGraphicsDropShadowEffect(self)
        self.shadow3.setBlurRadius(5)
        self.shadow3.setColor(QColor(93, 93, 93).darker())
        self.shadow3.setOffset(0)

        self.shadow4 = QGraphicsDropShadowEffect(self)
        self.shadow4.setBlurRadius(5)
        self.shadow4.setColor(QColor(93, 93, 93).darker())
        self.shadow4.setOffset(0)

        self.shadow5 = QGraphicsDropShadowEffect(self)
        self.shadow5.setBlurRadius(5)
        self.shadow5.setColor(QColor(93, 93, 93).darker())
        self.shadow5.setOffset(0)

        self.shadow6 = QGraphicsDropShadowEffect(self)
        self.shadow6.setBlurRadius(5)
        self.shadow6.setColor(QColor(93, 93, 93).darker())
        self.shadow6.setOffset(0)

        self.shadow7 = QGraphicsDropShadowEffect(self)
        self.shadow7.setBlurRadius(5)
        self.shadow7.setColor(QColor(93, 93, 93).darker())
        self.shadow7.setOffset(0)

        self.examTitleLineEdit.setGraphicsEffect(self.shadow1)
        self.examMakerLineEdit.setGraphicsEffect(self.shadow2)
        self.userScoreLineEdit.setGraphicsEffect(self.shadow3)
        self.noneAnwserCountLineEdit.setGraphicsEffect(self.shadow4)
        self.rightAnwserCountLineEdit.setGraphicsEffect(self.shadow5)
        self.wrongAnwserLineEdit.setGraphicsEffect(self.shadow6)
        self.exitButton.setGraphicsEffect(self.shadow7)

    def labels(self):
        self.titleLabel.setFont(QFont(self.tanha[0], 13))
        self.examTitleLabel.setFont(QFont(self.tanha[0], 10))
        self.examMakerLabel.setFont(QFont(self.tanha[0], 10))
        self.userScoreLabel.setFont(QFont(self.tanha[0], 10))
        self.noneAnwserCountLabel.setFont(QFont(self.tanha[0], 10))
        self.rightAnwserCountLabel.setFont(QFont(self.tanha[0], 10))
        self.wrongAnwserLabel.setFont(QFont(self.tanha[0], 10))
        self.groupBox.setFont(QFont(self.tanha[0], 10))

    def lineEdits(self):
        self.examTitleLineEdit.setFont(QFont(self.tanha[0], 10))
        self.examMakerLineEdit.setFont(QFont(self.tanha[0], 10))
        self.userScoreLineEdit.setFont(QFont(self.tanha[0], 10))
        self.noneAnwserCountLineEdit.setFont(QFont(self.tanha[0], 10))
        self.rightAnwserCountLineEdit.setFont(QFont(self.tanha[0], 10))
        self.wrongAnwserLineEdit.setFont(QFont(self.tanha[0], 10))

    def button(self):
        self.exitButton.setFont(QFont(self.tanha[0], 10))
        self.exitButton.clicked.connect(self.showMainPage)

    #===========================================================#
    def showMainPage(self):
        self.close()
        mainWindow.show()





if __name__ == "__main__":
    global rejisterWindow, mainWindow, exameDetailWindow, profileSettingWindow, changeUserNameWindow, changePasswordWindow, examePageWindow, examResultWindow, currentExamQuestions, loggedUser, selectedExam, finishedExameInfo
    app = QApplication(sys.argv)

    loggedUser = {'id': '', 'userName': '', 'password': '', 'score': '', 'class': '', 'email': '', 'profileImage': ''}
    selectedExam = {'id': '', 'examTitle': '', 'examClass': '', 'examInfo': '', 'examScore': '', 'examQuestionsCount': '', 'examTime': '', 'examMaker': '', 'timeUserFinished': '', }
    finishedExameInfo = {'scoreGot': 0, 'wrongAnwser': 0, 'rightAnwser': 0, 'noneAnwser': 0}
    currentExamQuestions = []

    rejisterWindow = RejisterPage()
    mainWindow = Main()
    exameDetailWindow = ExameDetail()
    examePageWindow = ExamePage()
    examResultWindow = ExamResult()
    profileSettingWindow = ProfileSetting()
    changeUserNameWindow = ChangeUserName()
    changePasswordWindow = ChangePassword()

    rejisterWindow.show()
    sys.exit(app.exec_())

# password Space
# exame question count