import datetime
import random
import re
import sys

from PyQt5.QtCore import QTimer, QDateTime, Qt
from PyQt5.QtGui import QColor, QFontDatabase, QFont, QPixmap, QCloseEvent, QShowEvent, QMouseEvent
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QGraphicsDropShadowEffect, QStackedWidget, QVBoxLayout, \
    QFrame, QMessageBox, QDialog, QPushButton, QLabel, QComboBox, QSpinBox, QTextEdit, QCheckBox
from PyQt5.uic import loadUi

import DataBase

currentQuizTeacherId = {'id': ''}

class RegisterPage(QWidget):
    def __init__(self):
        super(RegisterPage, self).__init__()
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
        self.appNameLabel.setFont(QFont(self.tanha[0], 18))
        self.shortDecLabel.setFont(QFont(self.tanha[0], 11))

    def buttons(self):
        self.signUpButton.setFont(QFont(self.tanha[0], 10))
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
        self.titleLabel.setFont(QFont(self.tanha[0], 20))
        self.commentLabel.setFont(QFont(self.tanha[0], 10))
        self.userNameLabel.setFont(QFont(self.tanha[0], 10))
        self.passwordLabel.setFont(QFont(self.tanha[0], 10))

        self.errorLabel.setFont(QFont(self.tanha[0], 10))

    def lineEdits(self):
        self.userNameLineEdit.setFont(QFont(self.tanha[0], 10))
        self.passwordLineEdit.setFont(QFont(self.tanha[0], 10))

    def pushButton(self):
        self.loginBtn.setFont(QFont(self.tanha[0], 14))
        self.loginBtn.clicked.connect(self.checkUser)

    # ===================================================#
    def checkUser(self):
        DataBase.checkConnection(registerWindow)
        user = DataBase.checkUser(userName=self.userNameLineEdit.text(), password=self.passwordLineEdit.text())
        if user is not None:
            self.errorLabel.setText('')
            loggedUser['id'] = user['id']
            loggedUser['userName'] = user['userName']
            loggedUser['password'] = user['password']
            loggedUser['score'] = user['score']
            loggedUser['class'] = user['class']
            loggedUser['email'] = user['email']
            loggedUser['profileImage'] = user['profileImage']
            loggedUser['isTeacher'] = user['isTeacher']
            if loggedUser['isTeacher']:
                teacherMainWindow.show()
            else:
                studentMainWindow.show()
            registerWindow.close()
        else:
            self.errorLabel.setText('نام کاربری یا رمز عبور اشتباه است')


class SignUp(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('./ui/signUp.ui', self)
        self.fonts()
        self.buttons()

    def fonts(self):
        tanha = QFontDatabase.addApplicationFont('./font/Tanha.ttf')
        self.tanha = QFontDatabase.applicationFontFamilies(tanha)

        self.title.setFont(QFont(self.tanha[0], 12))
        self.shortDec.setFont(QFont(self.tanha[0], 10))

    def buttons(self):
        self.studentButton.setFont(QFont(self.tanha[0], 10))
        self.teacherButton.setFont(QFont(self.tanha[0], 10))

        self.studentButton.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(0))
        self.teacherButton.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(1))

    def showEvent(self, a0: QShowEvent) -> None:
        self.stackedWidget.removeWidget(self.page)
        self.stackedWidget.removeWidget(self.page_2)
        self.stackedWidget.addWidget(studentSignUpWindow)
        self.stackedWidget.addWidget(teacherSignUpWindow)


class TeacherSignUpPage(QWidget):
    def __init__(self):
        super(TeacherSignUpPage, self).__init__()
        loadUi('./ui/teacherSignUpPage.ui', self)
        self.numbersCheckResult = False
        self.spiecialCharacterCheckResult = False
        self.capitalLettersCheckResult = False
        self.widthCheckResult = False

        self.scrollAreaWidgetContents.setStyleSheet("background: #ffffff;border:none;")

        self.fonts()
        self.labels()
        self.butten()
        self.lineEdits()

    def fonts(self):
        tanha = QFontDatabase.addApplicationFont('./font/Tanha.ttf')
        self.tanha = QFontDatabase.applicationFontFamilies(tanha)

    def labels(self):
        self.title.setFont(QFont(self.tanha[0], 12))
        # self.shortDec.setFont(QFont(self.tanha[0], 10))
        self.userName.setFont(QFont(self.tanha[0], 10))
        self.password.setFont(QFont(self.tanha[0], 10))
        self.rePassword.setFont(QFont(self.tanha[0], 10))
        self.widthText.setFont(QFont(self.tanha[0], 8))
        self.numText.setFont(QFont(self.tanha[0], 8))
        self.specText.setFont(QFont(self.tanha[0], 8))
        self.capText.setFont(QFont(self.tanha[0], 8))

        self.userNameErrorLabel.setFont(QFont(self.tanha[0], 8))
        self.passwoedValidErrorLabel.setFont(QFont(self.tanha[0], 8))
        self.samePasswordErrorLabel.setFont(QFont(self.tanha[0], 8))

        self.firstNameLabel.setFont(QFont(self.tanha[0], 10))
        self.lastNameLabel.setFont(QFont(self.tanha[0], 10))
        self.emailLabel.setFont(QFont(self.tanha[0], 10))

        self.firstNameLineEdit.setFont(QFont(self.tanha[0], 10))
        self.lastNameLineEdit.setFont(QFont(self.tanha[0], 10))
        self.emailLineEdit.setFont(QFont(self.tanha[0], 10))

        self.firstNameErrorLabel.setFont(QFont(self.tanha[0], 8))
        self.lastNameErrorLabel.setFont(QFont(self.tanha[0], 8))
        self.emailErrorLabel.setFont(QFont(self.tanha[0], 8))

        self.numbersCheck.setPixmap(QPixmap('./image/cross.png'))
        self.spiecialCharacterCheck.setPixmap(QPixmap('./image/cross.png'))
        self.capitalLettersCheck.setPixmap(QPixmap('./image/cross.png'))
        self.widthCheck.setPixmap(QPixmap('./image/cross.png'))

    def lineEdits(self):
        self.userNameLineEdit.setFont(QFont(self.tanha[0], 10))
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

        if re.findall("^(?=.* ?[A-Z])(?=.* ?[a-z])", password) and not re.findall(" +", password):
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
        DataBase.checkConnection(registerWindow)
        userName = self.userNameLineEdit.text()
        name = self.firstNameLineEdit.text()
        lastName = self.lastNameLineEdit.text()
        email = self.emailLineEdit.text()
        password = self.passwordLineEdit.text()
        rePassword = self.repeatPasswordLineEdit.text()

        userNameValid = False
        nameValid = False
        lastNameValid = False
        emailValid = False
        passwordValid = False
        rePasswordValid = False

        if userName.replace(' ', ''):
            if DataBase.checkUserName(userName):
                self.userNameErrorLabel.setText('')
                userNameValid = True
            else:
                self.userNameErrorLabel.setText('این نام کاربری قبلا انتخاب شده است')
        else:
            self.userNameErrorLabel.setText('نام کاربری نباید خالی باشد')

        if name.replace(' ', ''):
            self.firstNameErrorLabel.setText('')
            nameValid = True
        else:
            self.firstNameErrorLabel.setText('نام نباید خالی باشد')

        if lastName.replace(' ', ''):
            self.lastNameErrorLabel.setText('')
            lastNameValid = True
        else:
            self.lastNameErrorLabel.setText('نام خوانوادگی نباید خالی باشد')

        if email.replace(' ', ''):
            if re.findall(r"^\S+@\S+\.\S+$", email.replace(' ', '')):
                self.emailErrorLabel.setText('')
                emailValid = True
            else:
                self.emailErrorLabel.setText('لطفا یک ایمیل معتبر وارد کنید')
        else:
            self.emailErrorLabel.setText('ایمیل نباید خالی باشد')

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

        if userNameValid and passwordValid and rePasswordValid and nameValid and lastNameValid and emailValid:
            massage = QMessageBox(self)
            massage.setText('آیا از اطلاعت وارد شده مطمئن هستید؟')
            massage.setIcon(QMessageBox.Warning)
            massage.setWindowTitle('مهم')
            massage.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            anwser = massage.exec()
            if anwser == QMessageBox.Ok:
                DataBase.createAccount(userName, password, name, lastName, email, True)
                self.userNameLineEdit.setText('')
                self.passwordLineEdit.setText('')
                self.repeatPasswordLineEdit.setText('')
                self.lastNameLineEdit.setText('')
                self.firstNameLineEdit.setText('')
                self.emailLineEdit.setText('')
                massage2 = QMessageBox(self)
                massage2.setText('حساب کاربری شما ایجاد شد.')
                massage2.setStandardButtons(QMessageBox.Ok)
                massage2.exec()


class StudentSignUpPage(QWidget):
    def __init__(self):
        super(StudentSignUpPage, self).__init__()
        loadUi('./ui/studentSignUpPage.ui', self)
        self.numbersCheckResult = False
        self.spiecialCharacterCheckResult = False
        self.capitalLettersCheckResult = False
        self.widthCheckResult = False

        self.scrollAreaWidgetContents.setStyleSheet("background: #ffffff;border:none;")

        self.fonts()
        self.labels()
        self.butten()
        self.lineEdits()

    def fonts(self):
        tanha = QFontDatabase.addApplicationFont('./font/Tanha.ttf')
        self.tanha = QFontDatabase.applicationFontFamilies(tanha)

    def labels(self):
        self.title.setFont(QFont(self.tanha[0], 12))
        # self.shortDec.setFont(QFont(self.tanha[0], 10))
        self.userName.setFont(QFont(self.tanha[0], 10))
        self.password.setFont(QFont(self.tanha[0], 10))
        self.rePassword.setFont(QFont(self.tanha[0], 10))
        self.widthText.setFont(QFont(self.tanha[0], 8))
        self.numText.setFont(QFont(self.tanha[0], 8))
        self.specText.setFont(QFont(self.tanha[0], 8))
        self.capText.setFont(QFont(self.tanha[0], 8))

        self.userNameErrorLabel.setFont(QFont(self.tanha[0], 8))
        self.passwoedValidErrorLabel.setFont(QFont(self.tanha[0], 8))
        self.samePasswordErrorLabel.setFont(QFont(self.tanha[0], 8))

        self.numbersCheck.setPixmap(QPixmap('./image/cross.png'))
        self.spiecialCharacterCheck.setPixmap(QPixmap('./image/cross.png'))
        self.capitalLettersCheck.setPixmap(QPixmap('./image/cross.png'))
        self.widthCheck.setPixmap(QPixmap('./image/cross.png'))

    def lineEdits(self):
        self.userNameLineEdit.setFont(QFont(self.tanha[0], 10))
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

        if re.findall("^(?=.* ?[A-Z])(?=.* ?[a-z])", password) and not re.findall(" +", password):
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
        DataBase.checkConnection(registerWindow)
        userName = self.userNameLineEdit.text()
        password = self.passwordLineEdit.text()
        rePassword = self.repeatPasswordLineEdit.text()

        userNameValid = False
        passwordValid = False
        rePasswordValid = False
        if userName.replace(' ', ''):
            if DataBase.checkUserName(userName):
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
                DataBase.createAccount(userName, password, '', '', '', False)
                self.userNameLineEdit.setText('')
                self.passwordLineEdit.setText('')
                self.repeatPasswordLineEdit.setText('')
                massage2 = QMessageBox(self)
                massage2.setText('حساب کاربری شما ایجاد شد.')
                massage2.setStandardButtons(QMessageBox.Ok)
                massage2.exec()


class TeacherMainPage(QMainWindow):
    def __init__(self):
        super(TeacherMainPage, self).__init__()
        loadUi('./ui/teacherMainPage.ui', self)
        self.fonts()
        self.labels()
        self.buttons()

    def showEvent(self, a0: QShowEvent) -> None:
        self.profileNameLabel.setText(str(loggedUser['userName']))

        self.exams = DataBase.gotAllExams(str(loggedUser['id']))
        if self.exams != []:
            self.emptyLabel.setDisabled(True)

        self.gotQuiz()

        if loggedUser['profileImage'] != 1:
            self.profileImageLabel.setStyleSheet(f"""
                border: none;
                border-radius: 50px;
                background: transparent;
                border-image: url('./image/profiles/Student Avatar - {loggedUser['profileImage']}.jpeg') 0 0 0 0 stretch stretch;
            """)
        else:
            self.profileImageLabel.setStyleSheet(f"""
                border: none;
                border-radius: 50px;
                background: transparent;
                border-image: url('./image/profiles/empty.png') 0 0 0 0 stretch stretch;
            """)

    def fonts(self):
        tanha = QFontDatabase.addApplicationFont('./font/Tanha.ttf')
        self.tanha = QFontDatabase.applicationFontFamilies(tanha)

    def labels(self):
        self.titleLabel.setFont(QFont(self.tanha[0], 12))
        self.emptyLabel.setFont(QFont(self.tanha[0], 10))
        self.profileNameLabel.setFont(QFont(self.tanha[0], 10))

    def gotQuiz(self):
        while self.contectLayout.count():
            cardFrame = self.contectLayout.takeAt(0)
            if cardFrame.widget():
                cardFrame.widget().deleteLater()

        row = 0
        column = 0
        DataBase.checkConnection(self)
        self.exams = DataBase.gotAllExams(str(loggedUser['id']))
        if self.exams != []:
            for exam in self.exams:
                card = TeacherCardFrame(exam)
                self.contectLayout.addWidget(card, row, column)
                column += 1
                if column == 1:
                    row += 1
                    column = 0

    def buttons(self):
        self.profileSettingButton.setFont(QFont(self.tanha[0], 10))
        self.ratingTableButton.setFont(QFont(self.tanha[0], 10))
        self.createQuizButton.setFont(QFont(self.tanha[0], 10))

        self.profileSettingButton.clicked.connect(lambda : profileSettingWindow.show())
        self.createQuizButton.clicked.connect(lambda : createNewQuizWindow.show())
        self.ratingTableButton.clicked.connect(lambda : leaderBoardWindow.show())

class TeacherCardFrame(QFrame):
    def __init__(self, exam):
        super(TeacherCardFrame, self).__init__()
        loadUi('./ui/teacherCardFrame.ui', self)
        self.exam = exam
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

        self.showMoreButton.setGraphicsEffect(self.shadow2)

    def labels(self):
        self.cardTitle.setFont(QFont(self.tanha[0], 12))
        self.scoreLabel.setFont(QFont(self.tanha[0], 9))
        self.questionsCountLabel.setFont(QFont(self.tanha[0], 9))
        self.classLabel.setFont(QFont(self.tanha[0], 9))

        self.label.setFont(QFont(self.tanha[0], 12))
        self.codeLineEdit.setFont(QFont(self.tanha[0], 12))

        self.codeLineEdit.setText(self.exam['quiz_code'])

        self.cardTitle.setText(self.exam['title'])
        # self.cardShortDes.setText(self.exam['info'])
        self.scoreLabel.setText(f'امتیاز:{str(self.exam["score"])}')
        self.questionsCountLabel.setText(f'تعداد سوال:{str(self.exam["questions_count"])}')
        self.classLabel.setText(f'پایه:{str(self.exam["quiz_class"])}')
        self.imageLabel.setPixmap(QPixmap('./image/article2.jpg'))

    def button(self):
        self.showMoreButton.setFont(QFont(self.tanha[0], 9))
        self.showMoreButton.clicked.connect(self.showQuizPlayes)

    def showQuizPlayes(self):
        currentQuizTeacherId['id'] = int(self.exam['id'])
        quizPlayersWindow.show()


class QuizPlayersPage(QWidget):
    def __init__(self):
        super(QuizPlayersPage, self).__init__()
        loadUi('./ui/leaderBoardPage.ui', self)
        self.fonts()

    def showEvent(self, a0: QShowEvent):
        while self.contentLayout.count():
            cardFrame = self.contentLayout.takeAt(0)
            if cardFrame.widget():
                cardFrame.widget().deleteLater()

        DataBase.checkConnection(self)
        users = DataBase.getQuizPlayers(currentQuizTeacherId['id'])
        num = 1
        for user in users:
            self.contentLayout.addWidget(UserFrame(user, num))
            num += 1

    def fonts(self):
        tanha = QFontDatabase.addApplicationFont('./font/Tanha.ttf')
        self.tanha = QFontDatabase.applicationFontFamilies(tanha)

        self.label.setFont(QFont(self.tanha[0], 12))


class CreateNewQuizPage(QWidget):
    def __init__(self):
        super(CreateNewQuizPage, self).__init__()
        loadUi('./ui/createQuizPage.ui', self)
        self.fonts()
        self.buttons()

    def showEvent(self, a0: QShowEvent) -> None:
        self.count = 1

        self.newQuiz = {'title': '', 'quiz_class': '', 'info': '', 'score': '', 'questions_count': '', 'time': ''}
        self.questions = {}

    def fonts(self):
        tanha = QFontDatabase.addApplicationFont('./font/Tanha.ttf')
        self.tanha = QFontDatabase.applicationFontFamilies(tanha)

        self.title.setFont(QFont(self.tanha[0], 12))
        self.titleLabel.setFont(QFont(self.tanha[0], 10))
        self.classLabel.setFont(QFont(self.tanha[0], 10))
        self.timeLabel.setFont(QFont(self.tanha[0], 10))
        self.shortDesLabel.setFont(QFont(self.tanha[0], 10))

        self.errorLabel.setFont(QFont(self.tanha[0], 10))

        self.titleLineEdit.setFont(QFont(self.tanha[0], 10))
        self.classComboBox.setFont(QFont(self.tanha[0], 10))
        self.timeSpinBox.setFont(QFont(self.tanha[0], 10))
        self.shortDesTextEdit.setFont(QFont(self.tanha[0], 10))

        self.label_5.setFont(QFont(self.tanha[0], 12))
        self.label_6.setFont(QFont(self.tanha[0], 10))
        self.questionScoreLabel.setFont(QFont(self.tanha[0], 10))
        self.questionCountLabel.setFont(QFont(self.tanha[0], 10))

        self.questionScoreLineEdit.setFont(QFont(self.tanha[0], 10))
        self.randomCountLineEdit.setFont(QFont(self.tanha[0], 10))
        self.questionCountLineEdit.setFont(QFont(self.tanha[0], 10))

        self.randomCheckBox.setFont(QFont(self.tanha[0], 10))
        self.addButton.setFont(QFont(self.tanha[0], 10))
        self.saveQuizButton.setFont(QFont(self.tanha[0], 12))

    def buttons(self):
        self.addButton.clicked.connect(self.addQuestion)
        self.saveQuizButton.clicked.connect(self.createQuiz)

        self.randomCheckBox.stateChanged.connect(self.randomSet)

    #====================================================#
    def randomSet(self, state):
        if state == 2:
            self.randomCountLineEdit.setEnabled(True)
        else:
            self.randomCountLineEdit.setText('')
            self.randomCountLineEdit.setEnabled(False)

    def addQuestion(self):
        self.questionsLayout.addWidget(TeacherQuestionFrame(self.count))
        self.questionCountLineEdit.setText(str(self.count))
        self.count += 1

    def createQuiz(self):
        DataBase.checkConnection(createNewQuizWindow)
        title = self.titleLineEdit.text()
        quizClass = self.classComboBox.currentText()
        time = self.timeSpinBox.text()
        info = self.shortDesTextEdit.toPlainText()
        score = self.questionScoreLineEdit.text()
        randomCount = None
        is_random = False

        if title.replace(' ', '') and quizClass and int(time) > 0 and info.replace(' ', ''):
            try:
                int(score)
                if int(score) > 0:
                    if self.randomCheckBox.checkState() == Qt.Checked:
                        is_random = True
                    if is_random:
                        try:
                            int(self.randomCountLineEdit.text())
                            if int(self.randomCountLineEdit.text()) > 0:
                                if int(self.randomCountLineEdit.text()) < int(self.questionCountLineEdit.text()):
                                    randomCount = int(self.randomCountLineEdit.text())
                                else:
                                    self.errorLabel.setText('تعداد سوال نباید از تعداد کل سوالات وارد شده کمتر باشد')
                                    return None
                            else:
                                self.errorLabel.setText('تعداد سوال را درست وارد کنید')
                                return None
                        except:
                            self.errorLabel.setText('تعداد سوال را درست وارد کنید')
                            return None

                    if self.questions != {}:
                        massage = QMessageBox(self)
                        massage.setText(f'آیا از اطلاعات وارد شده مطمئن هستید؟(آزمون ثبت شده قابل ویرایش نیست.)')
                        massage.setIcon(QMessageBox.Warning)
                        massage.setWindowTitle('مهم')
                        massage.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                        anwser = massage.exec()
                        if anwser == QMessageBox.Ok:
                            valid = True
                            for question in self.questions:
                                newQuestion = self.questions[question]['question']
                                if not newQuestion['questionText'] or not newQuestion['optionOne'] or not newQuestion['optionTwo'] or not newQuestion['optionThree'] or not newQuestion['optionFour']:
                                    valid = False

                            if valid:
                                newQuiz = DataBase.createQuiz(title, quizClass, int(time), info, randomCount, is_random,
                                                              loggedUser['id'])
                                for question in self.questions:
                                    newQuestion = self.questions[question]['question']
                                    DataBase.addQuestion(newQuestion['questionText'], newQuestion['optionOne'], newQuestion['optionTwo'], newQuestion['optionThree'], newQuestion['optionFour'], newQuestion['anwser'], score, newQuiz['id'])

                                self.titleLineEdit.setText('')
                                self.classComboBox.setCurrentIndex(0)
                                self.timeSpinBox.setValue(0)
                                self.shortDesTextEdit.setText('')
                                self.questionScoreLineEdit.setText('')
                                self.randomCountLineEdit.setText('')

                                while self.questionsLayout.count():
                                    cardFrame = self.questionsLayout.takeAt(0)
                                    if cardFrame.widget():
                                        cardFrame.widget().deleteLater()

                                self.questions = {}
                                self.errorLabel.setText('')
                                teacherMainWindow.gotQuiz()
                                createNewQuizWindow.close()

                            else:
                                self.errorLabel.setText('متن یا گزینه های بعضی سوال ها خالی است')

                    else:
                        self.errorLabel.setText('هنوز هیچ سوالی وارد نکرده اید')
                else:
                    self.errorLabel.setText('امتیاز هر سوال را درست وارد کنید')
            except:
                self.errorLabel.setText('امتیاز هر سوال را درست وارد کنید')
        else:
            self.errorLabel.setText('اطلاعات آزمون را کامل کنید')


class TeacherQuestionFrame(QFrame):
    def __init__(self, count):
        super(TeacherQuestionFrame, self).__init__()
        loadUi('./ui/teacherQuestionFrame.ui', self)

        self.count = count
        self.question = {
            'questionText': '',
            'optionOne': '',
            'optionTwo': '',
            'optionThree': '',
            'optionFour': '',
            'anwser': 1
        }
        createNewQuizWindow.questions[self.count] = {'id':self.count , 'question': self.question}
        self.fonts()
        self.shadow()
        self.labels()
        self.buttons()
        self.textEdits()

    def shadow(self):
        self.shadow1 = QGraphicsDropShadowEffect(self)
        self.shadow1.setBlurRadius(12)
        self.shadow1.setColor(QColor(150, 150, 150).darker())
        self.shadow1.setOffset(0)

        self.setGraphicsEffect(self.shadow1)

    def fonts(self):
        tanha = QFontDatabase.addApplicationFont('./font/Tanha.ttf')
        self.tanha = QFontDatabase.applicationFontFamilies(tanha)

        self.questionNumLabel.setFont(QFont(self.tanha[0], 8))
        self.questionTextEdit.setFont(QFont(self.tanha[0], 8))

        self.optionOneButton.setFont(QFont(self.tanha[0], 8))
        self.oneTextEdit.setFont(QFont(self.tanha[0], 8))

        self.optionTwoButton.setFont(QFont(self.tanha[0], 8))
        self.twoTextEdit.setFont(QFont(self.tanha[0], 8))

        self.optionThreeButton.setFont(QFont(self.tanha[0], 8))
        self.threeTextEdit.setFont(QFont(self.tanha[0], 8))

        self.optionFourButton.setFont(QFont(self.tanha[0], 8))
        self.fourTextEdit.setFont(QFont(self.tanha[0], 8))

        self.deleteButton.setFont(QFont(self.tanha[0], 10))

    def textEdits(self):
        self.questionTextEdit.textChanged.connect(lambda : self.changeQuestionInfo('questionText', self.questionTextEdit.toPlainText()))

        self.oneTextEdit.textChanged.connect(lambda : self.changeQuestionInfo('optionOne', self.oneTextEdit.toPlainText()))

        self.twoTextEdit.textChanged.connect(lambda : self.changeQuestionInfo('optionTwo', self.twoTextEdit.toPlainText()))

        self.threeTextEdit.textChanged.connect(lambda : self.changeQuestionInfo('optionThree', self.threeTextEdit.toPlainText()))

        self.fourTextEdit.textChanged.connect(
            lambda: self.changeQuestionInfo('optionFour', self.fourTextEdit.toPlainText()))

    def buttons(self):
        self.optionOneButton.toggled.connect(lambda checked: self.setAnwser('1') if checked else None)
        self.optionTwoButton.toggled.connect(lambda checked: self.setAnwser('2') if checked else None)
        self.optionThreeButton.toggled.connect(lambda checked: self.setAnwser('3') if checked else None)
        self.optionFourButton.toggled.connect(lambda checked: self.setAnwser('4') if checked else None)

        self.deleteButton.clicked.connect(self.deleteFrame)

    def labels(self):
        self.questionNumLabel.setText(f'.{self.count}')


    #======================================================#
    def changeQuestionInfo(self, part, text):
        createNewQuizWindow.questions[self.count]['question'][part] = text

    def setAnwser(self, option):
        createNewQuizWindow.questions[self.count]['question']['anwser'] = int(option)

    def deleteFrame(self):
        massage = QMessageBox(self)
        massage.setText(f'آیا از حذف سوال {self.count} مطمئن هستید؟')
        massage.setIcon(QMessageBox.Warning)
        massage.setWindowTitle('مهم')
        massage.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        anwser = massage.exec()
        if anwser == QMessageBox.Ok:
            widget = createNewQuizWindow.questionsLayout.itemAt(self.count - 1).widget()
            createNewQuizWindow.questionsLayout.removeWidget(widget)

            createNewQuizWindow.questions.pop(self.count)

            for index in range(createNewQuizWindow.questionsLayout.count()):
                frame = createNewQuizWindow.questionsLayout.itemAt(index).widget()
                frame.questionNumLabel.setText(f'.{index + 1}')
                createNewQuizWindow.count -= 1


class StudentMainPage(QMainWindow):
    def __init__(self):
        super(StudentMainPage, self).__init__()
        loadUi('./ui/studendMainPage.ui', self)
        # self.shadows()
        self.fonts()
        self.lineEdit()
        self.comboBox()
        self.labels()
        self.buttons()

    def showEvent(self, a0: QShowEvent) -> None:
        self.profileNameLabel.setText(str(loggedUser['userName']))
        self.profileScoreLabel.setText(f' امتیاز:{loggedUser["score"]}')

        row = 0
        column = 0
        DataBase.checkConnection(studentMainWindow)
        exams = DataBase.gotAllExams('')
        if exams is not None:
            for exam in exams:
                card = CardFrame(exam)
                self.contectLayout.addWidget(card, row, column)
                column += 1
                if column == 1:
                    row += 1
                    column = 0
        else:
            card = EmptyCardFrame()
            self.contectLayout.addWidget(card, 0, 0)

        if loggedUser['profileImage'] != 1:
            self.profileImageLabel.setStyleSheet(f"""
                border: none;
                border-radius: 50px;
                background: transparent;
                border-image: url('./image/profiles/Student Avatar - {loggedUser['profileImage']}.jpeg') 0 0 0 0 stretch stretch;
            """)
        else:
            self.profileImageLabel.setStyleSheet(f"""
                border: none;
                border-radius: 50px;
                background: transparent;
                border-image: url('./image/profiles/empty.png') 0 0 0 0 stretch stretch;
            """)

    def fonts(self):
        tanha = QFontDatabase.addApplicationFont('./font/Tanha.ttf')
        self.tanha = QFontDatabase.applicationFontFamilies(tanha)

    def lineEdit(self):
        self.searchLineEdit.setFont(QFont(self.tanha[0], 10))
        self.codeLineEdit.setFont(QFont(self.tanha[0], 10))

    def labels(self):
        self.profileNameLabel.setFont(QFont(self.tanha[0], 11))
        self.profileScoreLabel.setFont(QFont(self.tanha[0], 11))

        self.searchLabel.setFont(QFont(self.tanha[0], 10))
        self.classLabel.setFont(QFont(self.tanha[0], 10))
        self.codeLabel.setFont(QFont(self.tanha[0], 10))

    def buttons(self):
        self.ratingTableButton.setFont(QFont(self.tanha[0], 10))
        self.profileSettingButton.setFont(QFont(self.tanha[0], 10))
        self.searchButton.setFont(QFont(self.tanha[0], 10))
        self.searchCodeButton.setFont(QFont(self.tanha[0], 10))

        self.profileSettingButton.clicked.connect(self.showProfileSettingPage)

        self.searchButton.clicked.connect(self.searchInExams)

        self.searchCodeButton.clicked.connect(self.getPrivateQuiz)

        self.ratingTableButton.clicked.connect(lambda: leaderBoardWindow.show())

    def comboBox(self):
        self.classComboBox.setFont(QFont(self.tanha[0], 10))

    # =========================================================#
    def showProfileSettingPage(self):
        profileSettingWindow.show()

    def searchInExams(self):
        while self.contectLayout.count():
            cardFrame = self.contectLayout.takeAt(0)
            if cardFrame.widget():
                cardFrame.widget().deleteLater()

        row = 0
        column = 0
        DataBase.checkConnection(studentMainWindow)
        exams = DataBase.filterExames(self.searchLineEdit.text(), self.classComboBox.currentText())
        if exams != []:
            for exam in exams:
                card = CardFrame(exam)
                self.contectLayout.addWidget(card, row, column)
                column += 1
                if column == 1:
                    row += 1
                    column = 0
        else:
            card = EmptyCardFrame()
            self.contectLayout.addWidget(card, 0, 0)

    def getPrivateQuiz(self):
        while self.contectLayout.count():
            cardFrame = self.contectLayout.takeAt(0)
            if cardFrame.widget():
                cardFrame.widget().deleteLater()

        DataBase.checkConnection(studentMainWindow)
        exam = DataBase.searchPrivateQuiz(self.codeLineEdit.text())
        if exam is not None:
            card = CardFrame(exam)
            self.contectLayout.addWidget(card, 0, 0)
        else:
            card = EmptyCardFrame()
            self.contectLayout.addWidget(card, 0, 0)


class LeaderBoardPage(QWidget):
    def __init__(self):
        super(LeaderBoardPage, self).__init__()
        loadUi('./ui/leaderBoardPage.ui', self)
        self.fonts()

    def showEvent(self, a0: QShowEvent):
        while self.contentLayout.count():
            cardFrame = self.contentLayout.takeAt(0)
            if cardFrame.widget():
                cardFrame.widget().deleteLater()

        DataBase.checkConnection(self)
        users = DataBase.getLeaderBoard()
        num = 1
        for user in users:
            self.contentLayout.addWidget(UserFrame(user, num))
            num += 1

    def fonts(self):
        tanha = QFontDatabase.addApplicationFont('./font/Tanha.ttf')
        self.tanha = QFontDatabase.applicationFontFamilies(tanha)

        self.label.setFont(QFont(self.tanha[0], 12))


class UserFrame(QFrame):
    def __init__(self, user, num):
        super(UserFrame, self).__init__()
        loadUi('./ui/leaderBordFrame.ui', self)
        self.fonts()
        self.shadows()

        self.label.setText(str(num))

        if user['image'] != 1:
            self.profileImageLabel.setStyleSheet(f"""
                border: none;
                border-radius: 50px;
                background: transparent;
                border-image: url('./image/profiles/Student Avatar - {user['image']}.jpeg') 0 0 0 0 stretch stretch;
            """)
        else:
            self.profileImageLabel.setStyleSheet(f"""
                border: none;
                border-radius: 50px;
                background: transparent;
                border-image: url('./image/profiles/empty.png') 0 0 0 0 stretch stretch;
            """)

        self.userNameLineEdit.setText(user['username'])
        self.scoreLineEdit.setText(str(user['score']))

    def fonts(self):
        tanha = QFontDatabase.addApplicationFont('./font/Tanha.ttf')
        self.tanha = QFontDatabase.applicationFontFamilies(tanha)

        self.userNameLineEdit.setFont(QFont(self.tanha[0], 10))
        self.scoreLineEdit.setFont(QFont(self.tanha[0], 10))
        self.label.setFont(QFont(self.tanha[0], 10))

    def shadows(self):
        self.shadow1 = QGraphicsDropShadowEffect(self)
        self.shadow1.setBlurRadius(12)
        self.shadow1.setColor(QColor(150, 150, 150).darker())
        self.shadow1.setOffset(0)

        self.shadow2 = QGraphicsDropShadowEffect(self)
        self.shadow2.setBlurRadius(12)
        self.shadow2.setColor(QColor(150, 150, 150).darker())
        self.shadow2.setOffset(0)

        self.shadow3 = QGraphicsDropShadowEffect(self)
        self.shadow3.setBlurRadius(12)
        self.shadow3.setColor(QColor(150, 150, 150).darker())
        self.shadow3.setOffset(0)

        self.userNameLineEdit.setGraphicsEffect(self.shadow1)
        self.scoreLineEdit.setGraphicsEffect(self.shadow2)
        self.profileImageLabel.setGraphicsEffect(self.shadow3)


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

        if loggedUser['profileImage'] != 1:
            self.profileImageLabel.setStyleSheet(f"""
                border: none;
                border-radius: 50px;
                background: transparent;
                border-image: url('./image/profiles/Student Avatar - {loggedUser['profileImage']}.jpeg') 0 0 0 0 stretch stretch;
            """)
        else:
            self.profileImageLabel.setStyleSheet(f"""
                border: none;
                border-radius: 50px;
                background: transparent;
                border-image: url('./image/profiles/empty.png') 0 0 0 0 stretch stretch;
            """)

    def fonts(self):
        tanha = QFontDatabase.addApplicationFont('./font/Tanha.ttf')
        self.tanha = QFontDatabase.applicationFontFamilies(tanha)

    def labels(self):
        self.emailLabel.setFont(QFont(self.tanha[0], 10))
        self.classLabel.setFont(QFont(self.tanha[0], 10))

    def lineEdits(self):
        self.userNameLineEdit.setFont(QFont(self.tanha[0], 10))
        self.scoreLineEdit.setFont(QFont(self.tanha[0], 10))

        self.emailLineEdit.setFont(QFont(self.tanha[0], 10))

    def buttons(self):
        self.saveButton.setFont(QFont(self.tanha[0], 10))
        self.changeUserNameButton.setFont(QFont(self.tanha[0], 10))
        self.changePasswordButton.setFont(QFont(self.tanha[0], 10))
        self.changeProfileImageButton.setFont(QFont(self.tanha[0], 10))

        self.saveButton.clicked.connect(self.saveInfo)
        self.changeUserNameButton.clicked.connect(self.showChangeUserNameWindow)
        self.changePasswordButton.clicked.connect(self.showChangePasswordWindow)
        self.changeProfileImageButton.clicked.connect(self.showChangeProfileWindow)

    def comboBox(self):
        self.classComboBox.setFont(QFont(self.tanha[0], 10))

    # =======================================================#
    def saveInfo(self):
        DataBase.checkConnection(profileSettingWindow)
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

    def showChangeProfileWindow(self):
        changeProfileWindow.show()


class ChangeUserName(QWidget):
    def __init__(self):
        super(ChangeUserName, self).__init__()
        loadUi('./ui/changeUserName.ui', self)
        self.userNameValid = True
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
        self.pushButton.setFont(QFont(self.tanha[0], 12))
        self.pushButton.clicked.connect(self.saveNewUserName)


    # ======================================================#
    def checkUserName(self):
        DataBase.checkConnection(profileSettingWindow)
        text = self.userNameLineEdit.text()
        if not DataBase.checkUserName(text):
            if text == loggedUser['userName']:
                self.checkUserNameIcon.setPixmap(QPixmap('./image/accept.png'))
                self.userNameValid = True
            else:
                self.checkUserNameIcon.setPixmap(QPixmap('./image/cross.png'))
                self.userNameValid = False
        else:
            self.checkUserNameIcon.setPixmap(QPixmap('./image/accept.png'))
            self.userNameValid = True

    def saveNewUserName(self):
        if self.userNameValid == True:
            if self.userNameLineEdit.text() != loggedUser['userName']:
                DataBase.updateUserName(loggedUser['userName'], self.userNameLineEdit.text())
                loggedUser['userName'] = self.userNameLineEdit.text()
                if loggedUser['isTeacher']:
                    teacherMainWindow.profileNameLabel.setText(str(loggedUser['userName']))
                else:
                    studentMainWindow.profileNameLabel.setText(str(loggedUser['userName']))
                profileSettingWindow.userNameLineEdit.setText(loggedUser['userName'])
                self.errorLabel.setText('')
                self.close()
            else:
                self.close()
        else:
            self.errorLabel.setText('این نام کاربری قبلا انتخاب شده است.')


class ChangePassword(QWidget):
    def __init__(self):
        super(ChangePassword, self).__init__()
        loadUi('./ui/changePassword.ui', self)
        self.widthCheckResult = False
        self.capitalLettersCheckResult = False
        self.numbersCheckResult = False
        self.spiecialCharacterCheckResult = False

        self.fonts()
        self.labels()
        self.lineEdits()
        self.buttons()

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.passwordLineEdit.setText('')
        self.rePasswordLineEdit.setText('')
        self.passwordErrorLabel.setText('')
        self.rePasswordErrorLabel.setText('')

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

    def buttons(self):
        self.pushButton.setFont(QFont(self.tanha[0], 12))
        self.pushButton.clicked.connect(self.saveNewPassword)

    # ===========================================================#
    def passwordValidat(self):
        password = self.passwordLineEdit.text()

        if re.findall(".{8,}$", password):
            self.widthCheck.setPixmap(QPixmap('./image/accept.png'))
            self.widthCheckResult = True
        else:
            self.widthCheck.setPixmap(QPixmap('./image/cross.png'))
            self.widthCheckResult = False

        if re.findall("^(?=.* ?[A-Z])(?=.* ?[a-z])", password) and not re.findall(" +", password):
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


    def saveNewPassword(self):
        DataBase.checkConnection(profileSettingWindow)
        if self.passwordLineEdit.text() != loggedUser['password']:
            self.rePasswordErrorLabel.setText('')
            if self.widthCheckResult and self.capitalLettersCheckResult and self.numbersCheckResult and self.spiecialCharacterCheckResult:
                DataBase.updatePassword(loggedUser['userName'], self.passwordLineEdit.text())
                loggedUser['password'] = self.passwordLineEdit.text()
                self.passwordErrorLabel.setText('')
                self.close()
            else:
                self.passwordErrorLabel.setText('رمز عبور وارد شده شرایط لازم را ندارد.')
        else:
            self.rePasswordErrorLabel.setText('رمز عبور و تکرار آن مطابقت ندارد')


class ChangeProfilePage(QWidget):
    def __init__(self):
        super(ChangeProfilePage, self).__init__()
        loadUi('./ui/changeProfileImagePage.ui', self)
        self.shadows()
        self.fonts()
        self.pushButton.clicked.connect(self.saveImage)

        self.imagesLayout.addWidget(ImageFrame('./image/profiles/Student Avatar - 3.jpeg', '3'))
        self.imagesLayout.addWidget(ImageFrame('./image/profiles/Student Avatar - 4.jpeg', '4'))
        self.imagesLayout.addWidget(ImageFrame('./image/profiles/Student Avatar - 5.jpeg', '5'))
        self.imagesLayout.addWidget(ImageFrame('./image/profiles/Student Avatar - 7.jpeg', '7'))
        self.imagesLayout.addWidget(ImageFrame('./image/profiles/Student Avatar - 8.jpeg', '8'))
        self.imagesLayout.addWidget(ImageFrame('./image/profiles/Student Avatar - 10.jpeg', '10'))

    def showEvent(self, a0: QShowEvent):
        if loggedUser['profileImage'] != 1:
            self.currentImage = self.findChild(QFrame, str(loggedUser['profileImage']))
            self.currentImage.setStyleSheet(f"""
                #{self.currentImage.objectName()}{{
                    border-radius: 111px;
                    border:1px solid green;
                }}
            """)
        else:
            self.currentImage = None

    def shadows(self):
        self.shadow1 = QGraphicsDropShadowEffect(self)
        self.shadow1.setBlurRadius(12)
        self.shadow1.setColor(QColor(150, 150, 150).darker())
        self.shadow1.setOffset(0)

        self.scrollArea.setGraphicsEffect(self.shadow1)

    def fonts(self):
        tanha = QFontDatabase.addApplicationFont('./font/Tanha.ttf')
        self.tanha = QFontDatabase.applicationFontFamilies(tanha)

        self.label.setFont(QFont(self.tanha[0], 10))
        self.pushButton.setFont(QFont(self.tanha[0], 10))

    def saveImage(self):
        DataBase.checkConnection(self)
        if self.currentImage is not None:
            DataBase.updateProfileImage(loggedUser['userName'], int(self.currentImage.objectName()))
            loggedUser['profileImage'] = int(self.currentImage.objectName())
            profileSettingWindow.profileImageLabel.setStyleSheet(f"""
                border: none;
                border-radius: 50px;
                background: transparent;
                border-image: url('./image/profiles/Student Avatar - {loggedUser['profileImage']}.jpeg') 0 0 0 0 stretch stretch;
            """)
            if loggedUser['isTeacher']:
                teacherMainWindow.profileImageLabel.setStyleSheet(f"""
                    border: none;
                    border-radius: 50px;
                    background: transparent;
                    border-image: url('./image/profiles/Student Avatar - {loggedUser['profileImage']}.jpeg') 0 0 0 0 stretch stretch;
                """)
            else:
                studentMainWindow.profileImageLabel.setStyleSheet(f"""
                    border: none;
                    border-radius: 50px;
                    background: transparent;
                    border-image: url('./image/profiles/Student Avatar - {loggedUser['profileImage']}.jpeg') 0 0 0 0 stretch stretch;
                """)
        self.close()


class ImageFrame(QFrame):
    def __init__(self, url, objectName):
        super(ImageFrame, self).__init__()
        loadUi('./ui/imageFrame.ui', self)
        self.imageLabel.setStyleSheet(f"""
            border: none;
            border-radius: 100px;
            background: transparent;
            border-image: url({url}) 0 0 0 0 stretch stretch;
        """)
        self.setObjectName(objectName)

    def mousePressEvent(self, a0: QMouseEvent):
        self.setStyleSheet(f"""
            #{self.objectName()}{{
	            border-radius: 111px;
	            border:1px solid green;
            }}
        """)
        if changeProfileWindow.currentImage is not None:
            changeProfileWindow.currentImage.setStyleSheet(f"""
            """)
        changeProfileWindow.currentImage = changeProfileWindow.findChild(QFrame, self.objectName())


class CardFrame(QFrame):
    def __init__(self, exam):
        super(CardFrame, self).__init__()
        loadUi('./ui/cardFrame2.ui', self)
        self.exam = exam
        self.userDoExame = DataBase.checkUserDoExame(int(loggedUser['id']), int(self.exam['id']))
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

        self.showMoreButton.setGraphicsEffect(self.shadow2)

    def labels(self):
        self.cardTitle.setFont(QFont(self.tanha[0], 12))
        self.cardShortDes.setFont(QFont(self.tanha[0], 9))
        self.scoreLabel.setFont(QFont(self.tanha[0], 9))
        self.questionsCountLabel.setFont(QFont(self.tanha[0], 9))
        self.classLabel.setFont(QFont(self.tanha[0], 9))

        if self.userDoExame:
            self.errorLabel.setText('شما قبلا این آزمون را انجام داده اید')

        self.cardTitle.setText(self.exam['title'])
        self.cardShortDes.setText(self.exam['info'])
        self.scoreLabel.setText(f'امتیاز:{str(self.exam["score"])}')
        self.questionsCountLabel.setText(f'تعداد سوال:{str(self.exam["questions_count"])}')
        self.classLabel.setText(f'پایه:{str(self.exam["quiz_class"])}')
        self.imageLabel.setPixmap(QPixmap('./image/article2.jpg'))

    def button(self):
        self.showMoreButton.setFont(QFont(self.tanha[0], 9))
        if self.userDoExame:
            self.showMoreButton.setEnabled(False)

        self.showMoreButton.clicked.connect(self.showExameDetail)

    # ============================================================#
    def showExameDetail(self):
        DataBase.checkConnection(studentMainWindow)
        selectedExam['id'] = str(self.exam['id'])
        selectedExam['examTitle'] = self.exam['title']
        selectedExam['examClass'] = self.exam['quiz_class']
        selectedExam['examInfo'] = self.exam['info']
        selectedExam['examScore'] = str(self.exam['score'])
        selectedExam['examQuestionsCount'] = str(self.exam['questions_count'])
        selectedExam['examTime'] = self.exam['time']
        selectedExam['examMaker'] = self.exam['maker']
        selectedExam['is_random'] = self.exam['is_random']
        selectedExam['random_count'] = self.exam['random_count']
        selectedExam['is_private'] = self.exam['is_private']
        exameDetailWindow.show()


class EmptyCardFrame(QFrame):
    def __init__(self):
        super(EmptyCardFrame, self).__init__()
        loadUi('./ui/emptyCardFrame.ui', self)
        self.fonts()

    def fonts(self):
        tanha = QFontDatabase.addApplicationFont('./font/Tanha.ttf')
        self.tanha = QFontDatabase.applicationFontFamilies(tanha)

        self.label.setFont(QFont(self.tanha[0], 13))


class ExameDetail(QWidget):
    def __init__(self):
        super(ExameDetail, self).__init__()
        loadUi('./ui/exameDetailPage.ui', self)
        self.fonts()
        self.labels()
        self.button()
        self.shadows()

    def showEvent(self, e):
        print(selectedExam)
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

    # ==========================================================#
    def startExam(self):
        DataBase.checkConnection(exameDetailWindow)
        examePageWindow.show()
        studentMainWindow.close()
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

    def showEvent(self, e):
        self.anweredCount = 0
        self.userScore = 0
        count = 1
        for question in range(int(selectedExam["examQuestionsCount"])):
            button = QuestionButton(count)
            button.setObjectName(str(count))
            self.questionsLayout_2.addWidget(button)
            count += 1

        self.targetTime = QDateTime.currentDateTime().addSecs(int(selectedExam['examTime']) * 60)
        self.examTimer.start()

        self.answeredLabel.setText(f'{self.anweredCount} از {selectedExam["examQuestionsCount"]}')

        questions = []
        if selectedExam['is_random']:
            questions = random.sample(DataBase.gotExamQuestions(selectedExam['id']),
                                    k=int(selectedExam['examQuestionsCount']))
        else:
            questions = DataBase.gotExamQuestions(selectedExam['id'])

        index = 1
        for question in questions:
            currentExamQuestions.append({'idInExam': index, 'id': question['id'], 'question': question['question'],
                                         'optionOne': question['optionOne'], 'optionTwo': question['optionTwo'],
                                         'optionThree': question['optionThree'], 'optionFour': question['optionFour'],
                                         'anwser': question['anwser'], 'score': question['score'], 'isAnwsered': False,
                                         'userAnwser': ''})
            index += 1
        for question in currentExamQuestions:
            self.questionsStackedWidget.addWidget(QuestionFrame(question))

    def closeEvent(self, a0: QCloseEvent):
        DataBase.checkConnection(examePageWindow)
        DataBase.saveUsersDoExame(int(loggedUser['id']), int(selectedExam['id']), self.userScore)

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
        self.finishButton.setFont(QFont(self.tanha[0], 10))
        self.finishButton.clicked.connect(self.finishExame)

    def checkTime(self):
        now = QDateTime.currentDateTime()
        timeLeft = now.secsTo(self.targetTime)
        timeLeftStr = str(datetime.timedelta(seconds=max(0, timeLeft)))

        self.timeLabel.setText(timeLeftStr)

        if timeLeft <= 0:
            self.timeLabel.setText('End')
            self.finishExame()

    def finishExame(self):
        DataBase.checkConnection(examePageWindow)

        self.examTimer.stop()
        noneAnwser = 0
        rightAnwser = 0
        wrongAnwser = 0
        scoreGot = 0

        for question in currentExamQuestions:
            if question['isAnwsered'] == False:
                noneAnwser += 1
            elif str(question['anwser']) == str(question['userAnwser']):
                rightAnwser += 1
                scoreGot += int(question['score'])
            elif str(question['anwser']) != str(question['userAnwser']):
                wrongAnwser += 1

        if not selectedExam['is_private']:
            DataBase.updateScore(int(loggedUser['id']), int(scoreGot))
            loggedUser['score'] = int(loggedUser['score']) + scoreGot

        self.userScore = scoreGot

        finishedExameInfo['scoreGot'] = scoreGot
        finishedExameInfo['wrongAnwser'] = wrongAnwser
        finishedExameInfo['rightAnwser'] = rightAnwser
        finishedExameInfo['noneAnwser'] = noneAnwser

        currentExamQuestions.clear()

        for i in range(self.questionsStackedWidget.count()):
            widget = self.questionsStackedWidget.widget(i)
            widget.deleteLater()

        while self.questionsLayout_2.count():
            cardFrame = self.questionsLayout_2.takeAt(0)
            if cardFrame.widget():
                cardFrame.widget().deleteLater()

        self.close()
        examResultWindow.show()


class QuestionButton(QPushButton):
    def __init__(self, number):
        super(QuestionButton, self).__init__()
        self.number = number
        self.shadow()
        self.font()
        self.setting()

    def shadow(self):
        self.shadow1 = QGraphicsDropShadowEffect(self)
        self.shadow1.setBlurRadius(12)
        self.shadow1.setColor(QColor(150, 150, 150).darker())
        self.shadow1.setOffset(0)

        self.setGraphicsEffect(self.shadow1)

    def font(self):
        tanha = QFontDatabase.addApplicationFont('./font/Tanha.ttf')
        self.tanha = QFontDatabase.applicationFontFamilies(tanha)

        self.setFont(QFont(self.tanha[0], 10))

    def setting(self):
        self.clicked.connect(lambda: self.changeQuestion(self.number))
        self.setText(str(self.number))
        self.setMinimumSize(30, 30)
        self.setMaximumSize(30, 30)
        self.setStyleSheet('''
                    border:none;
                    background-color:#ffffff;
                    border-radius:5px;
                ''')

    def changeQuestion(self, number):
        examePageWindow.questionsStackedWidget.setCurrentIndex(int(self.number) - 1)
        # count = 0
        # for question in currentExamQuestions:
        #     if question['userAnwser']:
        #         count += 1
        # self.anweredCount = count
        # self.answeredLabel.setText(f'{self.anweredCount} از {selectedExam["examQuestionsCount"]}')


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

    def lineEdits(self):
        self.questionTextEdit.setFont(QFont(self.tanha[0], 10))
        self.questionTextEdit.setText(f'{self.question["idInExam"]}- {self.question["question"]}')
        self.oneTextEdit.setText(self.question["optionOne"])
        self.twoTextEdit.setText(self.question["optionTwo"])
        self.threeTextEdit.setText(self.question["optionThree"])
        self.fourTextEdit.setText(self.question["optionFour"])

    def buttons(self):
        self.optionOneButton.setFont(QFont(self.tanha[0], 10))
        self.optionTwoButton.setFont(QFont(self.tanha[0], 10))
        self.optionThreeButton.setFont(QFont(self.tanha[0], 10))
        self.optionFourButton.setFont(QFont(self.tanha[0], 10))

        self.oneTextEdit.setFont(QFont(self.tanha[0], 10))
        self.twoTextEdit.setFont(QFont(self.tanha[0], 10))
        self.threeTextEdit.setFont(QFont(self.tanha[0], 10))
        self.fourTextEdit.setFont(QFont(self.tanha[0], 10))

        self.optionOneButton.toggled.connect(lambda checked: self.addAnwser('1') if checked else None)
        self.optionTwoButton.toggled.connect(lambda checked: self.addAnwser('2') if checked else None)
        self.optionThreeButton.toggled.connect(lambda checked: self.addAnwser('3') if checked else None)
        self.optionFourButton.toggled.connect(lambda checked: self.addAnwser('4') if checked else None)

    # ============================================================#
    def addAnwser(self, anwser):
        for question in currentExamQuestions:
            if question['id'] == self.question['id']:
                if not question['isAnwsered']:
                    question['userAnwser'] = anwser
                    question['isAnwsered'] = True
                    examePageWindow.anweredCount += 1
                    examePageWindow.answeredLabel.setText(
                        f'{examePageWindow.anweredCount} از {selectedExam["examQuestionsCount"]}')
                    button = examePageWindow.findChild(QPushButton, str(question['idInExam']))
                    button.setStyleSheet('''
                        border:1px solid #19aa00;
                        background-color:#ffffff;
                        border-radius:5px;
                    ''')
                else:
                    question['userAnwser'] = anwser


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

    # ===========================================================#
    def showMainPage(self):
        self.close()
        studentMainWindow.show()


if __name__ == "__main__":
    global registerWindow, studentSignUpWindow, quizPlayersWindow,teacherSignUpWindow, createNewQuizWindow, studentMainWindow, teacherMainWindow, exameDetailWindow, profileSettingWindow, changeUserNameWindow, changePasswordWindow, examePageWindow, leaderBoardWindow, examResultWindow, currentExamQuestions, loggedUser, selectedExam, finishedExameInfo
    app = QApplication(sys.argv)

    loggedUser = {'id': '', 'userName': '', 'password': '', 'score': '', 'class': '', 'email': '', 'profileImage': '', 'isTeacher': ''}
    selectedExam = {'id': '', 'examTitle': '', 'examClass': '', 'examInfo': '', 'examScore': '',
                    'examQuestionsCount': '', 'examTime': '', 'examMaker': '', 'timeUserFinished': '', 'is_random': False, 'random_count': '', 'is_private': ''}
    finishedExameInfo = {'scoreGot': 0, 'wrongAnwser': 0, 'rightAnwser': 0, 'noneAnwser': 0}
    currentExamQuestions = []

    registerWindow = RegisterPage()
    studentSignUpWindow = StudentSignUpPage()
    teacherSignUpWindow = TeacherSignUpPage()

    studentMainWindow = StudentMainPage()
    teacherMainWindow = TeacherMainPage()
    createNewQuizWindow = CreateNewQuizPage()
    quizPlayersWindow = QuizPlayersPage()

    exameDetailWindow = ExameDetail()
    examePageWindow = ExamePage()
    examResultWindow = ExamResult()

    profileSettingWindow = ProfileSetting()
    changeUserNameWindow = ChangeUserName()
    changePasswordWindow = ChangePassword()
    changeProfileWindow = ChangeProfilePage()

    leaderBoardWindow = LeaderBoardPage()

    registerWindow.show()
    sys.exit(app.exec_())
