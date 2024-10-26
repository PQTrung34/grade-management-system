from customtkinter import *
from tkinter import *
from tkinter.ttk import Treeview, Style
from util import *
import mysql.connector

config = {
        'user': 'root',
        'password': 'pqtrung34',
        'host': 'localhost',
        'database': 'student_management'
    }
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

with open('login.txt', 'r') as f:
    id = f.read()
with open('login.txt', 'w'):
    pass

window = CTk()
window.title('Sinh viên')
window.geometry('1000x600')
window.resizable(0,0)

# Left frame
leftFrame = CTkFrame(window, width=300, height=600, fg_color='#ebebeb')
leftFrame.place(x=30,y=70)

def showInfo():
    for x in viewFrame.winfo_children():
        x.destroy()
    query = 'SELECT * FROM students WHERE id=%s'
    cursor.execute(query, (id,))
    res = cursor.fetchall()
    CTkLabel(viewFrame, text='Mã sinh viên', bg_color='#ebebeb', padx=10).grid(row=0, column=0, padx=10, pady=10, sticky="w")
    CTkLabel(viewFrame, text='Họ tên', bg_color='#ebebeb', padx=10).grid(row=1, column=0, padx=10, pady=10, sticky="w")
    CTkLabel(viewFrame, text='Lớp', bg_color='#ebebeb', padx=10).grid(row=2, column=0, padx=10, pady=10, sticky="w")
    CTkLabel(viewFrame, text='Giới tính', bg_color='#ebebeb', padx=10).grid(row=3, column=0, padx=10, pady=10, sticky="w")
    CTkLabel(viewFrame, text='Gmail', bg_color='#ebebeb', padx=10).grid(row=4, column=0, padx=10, pady=10, sticky="w")
    CTkLabel(viewFrame, text='Ngày sinh', bg_color='#ebebeb', padx=10).grid(row=5, column=0, padx=10, pady=10, sticky="w")
    CTkLabel(viewFrame, text='Số điện thoại', bg_color='#ebebeb', padx=10).grid(row=6, column=0, padx=10, pady=10, sticky="w")

    CTkLabel(viewFrame, text=res[0][0], bg_color='#ebebeb', padx=10).grid(row=0, column=1, padx=10, pady=10, sticky="w")
    CTkLabel(viewFrame, text=res[0][1], bg_color='#ebebeb', padx=10).grid(row=1, column=1, padx=10, pady=10, sticky="w")
    CTkLabel(viewFrame, text=res[0][2], bg_color='#ebebeb', padx=10).grid(row=2, column=1, padx=10, pady=10, sticky="w")
    CTkLabel(viewFrame, text=res[0][3], bg_color='#ebebeb', padx=10).grid(row=3, column=1, padx=10, pady=10, sticky="w")
    CTkLabel(viewFrame, text=res[0][4], bg_color='#ebebeb', padx=10).grid(row=4, column=1, padx=10, pady=10, sticky="w")
    CTkLabel(viewFrame, text=res[0][5], bg_color='#ebebeb', padx=10).grid(row=5, column=1, padx=10, pady=10, sticky="w")
    CTkLabel(viewFrame, text=res[0][6], bg_color='#ebebeb', padx=10).grid(row=6, column=1, padx=10, pady=10, sticky="w")
infoBtn = CTkButton(leftFrame, text='Thông tin', command=showInfo)
infoBtn.grid(row=0, column=0, pady=30)

def showGrade():
    for x in viewFrame.winfo_children():
        x.destroy()
    query = 'SELECT tenMon,grade FROM grades WHERE id=%s'
    cursor.execute(query, (id,))
    res = cursor.fetchall()
    columns = ['#1', '#2']
    gradeTable = Treeview(viewFrame, columns=columns, show='headings',)
    gradeTable.heading('#1', text='Môn')
    gradeTable.heading('#2', text='Điểm')
    style = Style()
    style.configure('Treeview',rowheight=40, font=('',13))
    style.configure('Treeview.Heading',font=('',15))
    gradeTable.pack()
    for data in res:
        gradeTable.insert('', END, values=data)
gradeBtn = CTkButton(leftFrame, text='Điểm thi', command=showGrade)
gradeBtn.grid(row=1, column=0, pady=30)

def logout():
    window.destroy()
    import login
logoutBtn = CTkButton(leftFrame, text='Đăng xuất', command=logout)
logoutBtn.grid(row=2, column=0, pady=30)

exitBtn = CTkButton(leftFrame, text='Thoát', command=window.destroy)
exitBtn.grid(row=3, column=0, pady=30)

viewFrame = CTkFrame(window, width=780, height=500, fg_color='#ebebeb')
viewFrame.place(x=400, y=70)

window.mainloop()