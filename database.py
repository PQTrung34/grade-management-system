import mysql.connector
from util import alert_message, success_message

config = {
    'user': 'root',
    'password': 'pqtrung34',
    'host': 'localhost',
    'database': 'student_management'
}

def connectDatabase():
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        success_message('Kết nối thành công')
        return
    except:
        alert_message('Kết nối thất bại')
        return

def getLoginInfo(username):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    query = f"""SELECT username, password FROM users WHERE username='{username}'"""
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) != 0:
        username, password = result[0][0], result[0][1]
        conn.close()
        return username, password
    else:
        return 0,0
    
def create_tables():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Grades(
        id nchar(6) NOT NULL,
        hoten nvarchar(50) NOT NULL,
        maMon nchar(5) NOT NULL,
        tenMon nvarchar(50) NOT NULL,
        grade int NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Lecturers(
        id nchar(6) NOT NULL,
        hoten nvarchar(50) NOT NULL,
        gioitinh ENUM('nam','nu') NOT NULL,
        email nvarchar(50) NOT NULL,
        dob date NOT NULL,
        sdt nchar(10) NOT NULL,
        phongban nvarchar(50) NOT NULL,
        CONSTRAINT PK_Lecturers PRIMARY KEY(id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users(
        id nchar(6) NOT NULL,
        role ENUM('admin','giảng viên','sinh viên') NOT NULL,
        username nvarchar(50) NOT NULL,
        password nvarchar(50) NOT NULL,
        CONSTRAINT PK_Users PRIMARY KEY(id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Students(
        id nchar(6) NOT NULL,
        hoten nvarchar(50) NOT NULL,
        lop nchar(6) NOT NULL,
        gioitinh ENUM('nam','nữ') NOT NULL,
        email nvarchar(50) NOT NULL,
        dob date NOT NULL,
        sdt nchar(10) NOT NULL,
        CONSTRAINT PK_Students PRIMARY KEY(id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Subjects(
        maMon nchar(5) NOT NULL,
        tenMon nvarchar(50) NOT NULL,
        soTinChi int NOT NULL,
        CONSTRAINT PK_Subjects PRIMARY KEY(maMon))''')
create_tables()