from customtkinter import *
import time
from tkinter.ttk import Treeview, Style
from util import *
import mysql.connector
import tkcalendar
from lecturer_crud import *
from student_crud import *

count = 0
text = ''
def slider():
    global text, count
    if count == len(s):
        count = 0
        text = ''
    text = text + s[count]
    sliderLabel.configure(text=text)
    count += 1
    sliderLabel.after(200, slider)
def clock():
    date = time.strftime('%d/%m/%Y')
    curr_time = time.strftime('%H:%M:%S')
    datetimeLabel.configure(text=f'   Date: {date}\nTime: {curr_time}')
    datetimeLabel.after(1000,clock)

window = CTk()
window.title('Hệ thống quản lý sinh viên')
window.geometry('1000x600')
window.resizable(0,0)

# Time label
datetimeLabel = CTkLabel(window, font=('Times',18,'bold'))
datetimeLabel.place(x=5,y=5)
clock()
# Slider text
s = 'Hệ thống quản lý sinh viên'
sliderLabel = CTkLabel(window, text=s, font=('Arial',28,'italic'))
sliderLabel.place(x=300,y=0)
slider()

# Left frame
leftFrame = CTkFrame(window, width=300, height=600, fg_color='#ebebeb')
leftFrame.place(x=30,y=70)

def connectDatabase():
    config = {
        'user': 'root',
        'password': 'pqtrung34',
        'host': 'localhost',
        'database': 'student_management'
    }
    try:
        global conn, cursor
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        success_message('Kết nối thành công')
    except:
        alert_message('Kết nối thất bại')

    lecturerBtn.configure(state=NORMAL)
    studentBtn.configure(state=NORMAL)
    subjectBtn.configure(state=NORMAL)
    

connectDBtn = CTkButton(window, text='Kết nối cơ sở dữ liệu', command=connectDatabase)
connectDBtn.place(x=850,y=0)

# Giảng viên
lecturerBtn = CTkButton(leftFrame, text='Giảng viên', state=DISABLED, command=lambda: showLecturer(viewFrame))
lecturerBtn.grid(row=0, column=0, pady=30)

# Sinh viên
studentBtn = CTkButton(leftFrame, text='Sinh viên', command=lambda: showStudent(viewFrame), state=DISABLED)
studentBtn.grid(row=1, column=0, pady=30)

# Môn học
def showSubject():
    for x in viewFrame.winfo_children():
        x.destroy()
    # studentTable Treeview
    columns = ['#1','#2','#3']
    global studentTable
    studentTable = Treeview(viewFrame, columns=columns, show='headings',)
    studentTable.heading('#1', text='Mã môn')
    studentTable.heading('#2', text='Tên môn')
    studentTable.heading('#3', text='Số tín chỉ')
    style = Style()
    style.configure('Treeview',rowheight=40, font=('',13))
    style.configure('Treeview.Heading',font=('',15))
    studentTable.pack()
    query = '''SELECT * FROM subjects'''
    cursor.execute(query)
    result = cursor.fetchall()
    for data in result:
        studentTable.insert('', END, values=data)
subjectBtn = CTkButton(leftFrame, text='Môn học', command=showSubject, state=DISABLED)
subjectBtn.grid(row=2, column=0, pady=30)

# Đăng xuất
def logout():
    window.destroy()
    import login
logoutBtn = CTkButton(leftFrame, text='Đăng xuất', command=logout)
logoutBtn.grid(row=3, column=0, pady=30)

exitBtn = CTkButton(leftFrame, text='Thoát', command=window.destroy)
exitBtn.grid(row=4, column=0, pady=30)

# viewFrame
viewFrame = CTkFrame(window, width=780, height=530, bg_color='#ebebeb', fg_color='#ebebeb')
viewFrame.place(x=200, y=70)

window.mainloop()