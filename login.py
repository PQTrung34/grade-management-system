from customtkinter import *
from tkinter import *
from PIL import Image
from util import *
import mysql.connector

def getLoginInfo(username):
    config = {
        'user': 'root',
        'password': 'pqtrung34',
        'host': 'localhost',
        'database': 'student_management'
    }
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    query = f"""SELECT username, password, role FROM users WHERE username='{username}'"""
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) != 0:
        username, password, role = result[0][0], result[0][1], result[0][2]
        conn.close()
        return username, password, role
    else:
        return 0,0,0

def login():
    if usernameEntry.get() == '' or passwordEntry.get() == '':
        alert_message('Vui lòng nhập đầy đủ thông tin đăng nhập')
        return
    else:
        username, password, role = getLoginInfo(usernameEntry.get())
        if username == 0 and password == 0:
            alert_message('Bạn chưa có tài khoản')
        elif username == usernameEntry.get() and password != passwordEntry.get():
            alert_message('Sai thông tin đăng nhập')
        elif username == usernameEntry.get() and password == passwordEntry.get():
            success_message('Đăng nhập thành công')
            if role == 'sinh viên':
                with open('login.txt','a') as f:
                    f.write(username)
            window.destroy()
            match role:
                case 'admin':
                    import admin
                case 'giảng viên':
                    import lecturer
                case 'sinh viên':
                    import student
                    
        else: 
            alert_message('Đăng nhập thất bại')
        return

window = CTk()
window.title('Đăng nhập')
window.geometry('1000x600')
window.resizable(0,0)

loginFrame = CTkFrame(window, fg_color='white')
loginFrame.place(x=350,y=150)

logoImage = CTkImage(light_image=Image.open('assets/logo.png'), size=(60,120))
logoLabel = CTkLabel(loginFrame, image=logoImage,text='')
logoLabel.grid(row=0, column=0, columnspan=2, pady=10)

usernameImage = CTkImage(light_image=Image.open('assets/light_user.png'),
                             dark_image=Image.open('assets/dark_user.png'),
                             size=(30,30))
usernameLabel = CTkLabel(loginFrame, text='Tên đăng nhập', image=usernameImage,
                              compound=LEFT, bg_color='#ffffff')
usernameLabel.grid(row=1, column=0,padx=20, pady=10)
usernameEntry = CTkEntry(loginFrame)
usernameEntry.grid(row=1, column=1, padx=20, pady=10)

passwordImage = CTkImage(light_image=Image.open('assets/light_lock.png'),
                             dark_image=Image.open('assets/dark_lock.png'),
                             size=(30,30))
passwordLabel = CTkLabel(loginFrame, text='Mật khẩu', image=passwordImage,
                              compound=LEFT, bg_color='#ffffff')
passwordLabel.grid(row=2, column=0,padx=20, pady=10, sticky='w')
passwordEntry = CTkEntry(loginFrame, show='*')
passwordEntry.grid(row=2, column=1, padx=20, pady=10)

loginBtn = CTkButton(loginFrame, text='Đăng nhập', command=login)
loginBtn.grid(row=3, column=1, pady=10)
window.mainloop()