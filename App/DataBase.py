import sqlite3

connection = sqlite3.connect('./DataBase.db')
cursor = connection.cursor()
sql1 = """
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userName VARCHAR (20), 
    password VARCHAR (60),
    score INTEGER,
    class VARCHAR (10),
    email VARCHAR (100),
    profileImage VARCHAR (30)
    );
"""

sql2 = """
    CREATE TABLE IF NOT EXISTS exams(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    examTitle VARCHAR (50), 
    examClass VARCHAR (30),
    examInfo VARCHAR,
    examScore INTEGER,
    examQuestionsCount INTEGER,
    examTime VARCHAR (100),
    examMaker VARCHAR (40)
    );
"""

sql3 = """
    CREATE TABLE IF NOT EXISTS questions(
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    question VARCHAR,
    optionOne VARCHAR,
    optionTwo VARCHAR ,
    optionThree VARCHAR ,
    optionFour VARCHAR,
    anwser INTEGER,
    score INTEGER,
    examId INTEGER
    );
"""

sql4 = """
    CREATE TABLE IF NOT EXISTS usersDoExams(
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    examId INTEGER,
    userId INTEGER 
    );
"""

cursor.execute(sql1)
cursor.execute(sql2)
cursor.execute(sql3)
cursor.execute(sql4)

connection.commit()
connection.close()


def createAccount(userName, password):
    connection = sqlite3.connect('./DataBase.db')
    cursor = connection.cursor()
    sql = """
        INSERT INTO users VALUES (NULL, ?, ?, 0, NULL, NULL, 1);
    """
    cursor.execute(sql, (userName, password,))
    connection.commit()
    connection.close()


def checkUserName():
    connection = sqlite3.connect('./DataBase.db')
    cursor = connection.cursor()
    sql = """
        SELECT * FROM users;
    """
    cursor.execute(sql)
    userList = []
    for user in list(cursor):
        userList.append(user[1])
    connection.commit()
    connection.close()
    return userList


def checkUser():
    connection = sqlite3.connect('./DataBase.db')
    cursor = connection.cursor()
    sql = """
        SELECT * FROM users;
    """
    cursor.execute(sql)
    userList = []
    for user in list(cursor):
        userList.append({'id': user[0], 'userName': user[1], 'password': user[2], 'score': user[3], 'class': user[4], 'email': user[5],'profileImage': user[6]})
    connection.commit()
    connection.close()
    return userList


def updateEmailAndClass(userName, newEmail, newClass):
    connection = sqlite3.connect('./DataBase.db')
    cursor = connection.cursor()
    sql1 = """
        UPDATE users SET email = ? WHERE userName like ?
    """
    sql2 = """
        UPDATE users SET class = ? WHERE userName like ?
    """
    cursor.execute(sql1, (newEmail, userName,))
    cursor.execute(sql2, (newClass, userName,))

    connection.commit()
    connection.close()


def updateUserName(userName, newUserName):
    connection = sqlite3.connect('./DataBase.db')
    cursor = connection.cursor()
    sql = """
        UPDATE users SET userName = ? WHERE userName like ?
    """

    cursor.execute(sql, (newUserName, userName,))
    connection.commit()
    connection.close()


def updatePassword(userName, newPassword):
    connection = sqlite3.connect('./DataBase.db')
    cursor = connection.cursor()
    sql = """
        UPDATE users SET password = ? WHERE userName like ?
    """

    cursor.execute(sql, (newPassword, userName,))
    connection.commit()
    connection.close()

def gotAllExams():
    connection = sqlite3.connect('./DataBase.db')
    cursor = connection.cursor()
    sql = """
        SELECT * FROM exams;
    """
    cursor.execute(sql)
    examsList = []
    for exam in list(cursor):
        examsList.append({'id': exam[0], 'examTitle': exam[1], 'examClass': exam[2], 'examInfo': exam[3], 'examScore': exam[4], 'examQuestionsCount': exam[5], 'examTime': exam[6], 'examMaker': exam[7]})
    connection.commit()
    connection.close()
    return examsList

def filterExames(text, exameClass):
    connection = sqlite3.connect('./DataBase.db')
    cursor = connection.cursor()
    if exameClass == 'هیچ کدام':
        sql = """
            SELECT * FROM exams WHERE examTitle LIKE ? OR examMaker LIKE ?;
        """
        cursor.execute(sql, (f'%{text}%', f'%{text}%',))

    elif text == '':
        sql = """
            SELECT * FROM exams WHERE examClass == ?;
        """
        cursor.execute(sql, (exameClass,))

    else:
        sql = """
                SELECT * FROM exams WHERE examClass == ? and examTitle LIKE ? or examMaker LIKE ?;
            """
        cursor.execute(sql, (exameClass, f'%{text}%', f'%{text}%',))

    examsList = []
    for exam in list(cursor):
        examsList.append(
            {'id': exam[0], 'examTitle': exam[1], 'examClass': exam[2], 'examInfo': exam[3], 'examScore': exam[4],
             'examQuestionsCount': exam[5], 'examTime': exam[6], 'examMaker': exam[7]})
    connection.commit()
    connection.close()
    return examsList

def gotExamQuestions(examId):
    connection = sqlite3.connect('./DataBase.db')
    cursor = connection.cursor()
    sql = """
        SELECT * FROM questions where examId == ?;
    """
    cursor.execute(sql, (examId,))
    questionsList = []
    for question in list(cursor):
        questionsList.append(
            {'id': question[0], 'question': question[1], 'optionOne': question[2], 'optionTwo': question[3], 'optionThree': question[4], 'optionFour': question[5], 'anwser': question[6], 'score': question[7], 'examId': question[8]})
    connection.commit()
    connection.close()
    return questionsList

def saveUsersDoExame(userId, exameId):
    connection = sqlite3.connect('./DataBase.db')
    cursor = connection.cursor()
    sql = """
        INSERT INTO usersDoExams VALUES (NULL, ?, ?);
    """
    cursor.execute(sql, (exameId, userId,))
    connection.commit()
    connection.close()

def updateScore(userId, scoreHad, scoreGot):
    newScore = int(scoreHad) + int(scoreGot)

    connection = sqlite3.connect('./DataBase.db')
    cursor = connection.cursor()
    sql = """
        UPDATE users SET score = ? WHERE id like ?
    """
    cursor.execute(sql, (newScore, userId,))
    connection.commit()
    connection.close()

def checkUserDoExame(userId, exameId):
    connection = sqlite3.connect('./DataBase.db')
    cursor = connection.cursor()
    sql = """
        SELECT * FROM usersDoExams where userId == ?;
    """
    cursor.execute(sql, (userId,))
    check = False
    for exame in list(cursor):
        if exame[1] == int(exameId):
            check = True
    connection.commit()
    connection.close()
    return check


