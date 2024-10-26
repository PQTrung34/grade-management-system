from customtkinter import *
from tkinter.ttk import Treeview, Style
from util import *
import mysql.connector
import tkcalendar

config = {
    'user': 'root',
    'password': 'pqtrung34',
    'host': 'localhost',
    'database': 'student_management'
}
conn = mysql.connector.connect(**config)
cursor = conn.cursor()
# studentTable = None

def pickDate(dobVar, txtDOB):
    dateWindow = CTkToplevel()
    dateWindow.grab_set()
    dateWindow.geometry('250x200')
    cal = tkcalendar.Calendar(dateWindow, selectmode='day', date_pattern='y-mm-dd')
    cal.grid(row=0, column=0, pady=10, padx=10)
    def grabDate():
        dobVar.set(cal.get_date())
        txtDOB.configure(text=dobVar.get())
        dateWindow.destroy()
    submitDate = CTkButton(dateWindow, text='Chọn', command=grabDate)
    submitDate.grid(row=1, column=0, pady=10)

def studentToplevel(title, buttonTitle, command, frame):
    if title == 'Sửa thông tin sinh viên' and studentTable.focus() == '':
        return
    screen = CTkToplevel()
    screen.grab_set()
    screen.wm_title(title)
    
    txtID = CTkEntry(screen)
    txtName = CTkEntry(screen)
    genderVar = StringVar(value='nam')
    genderFrame = CTkLabel(screen, bg_color='#ebebeb', padx=10, pady=10)
    male_rb = CTkRadioButton(genderFrame, text='Nam', variable=genderVar, value='nam')
    female_rb = CTkRadioButton(genderFrame, text='Nữ', variable=genderVar, value='nữ')
    txtEmail = CTkEntry(screen)
    dobFrame = CTkFrame(screen, fg_color='#ebebeb')
    dobVar = StringVar(value='2000-01-01')
    txtDOB = CTkLabel(dobFrame, text=dobVar.get())
    txtPhone = CTkEntry(screen)

    CTkLabel(screen, text='Mã sinh viên', bg_color='#ebebeb', padx=10).grid(row=0, column=0, padx=20, pady=20, sticky="w")
    CTkLabel(screen, text='Họ tên', bg_color='#ebebeb', padx=10).grid(row=1, column=0, padx=20, pady=20, sticky="w")
    CTkLabel(screen, text='Lớp', bg_color='#ebebeb', padx=10).grid(row=2, column=0, padx=20, pady=20, sticky="w")
    CTkLabel(screen, text='Giới tính', bg_color='#ebebeb', padx=10).grid(row=3, column=0, padx=20, pady=20, sticky="w")
    CTkLabel(screen, text='Email', bg_color='#ebebeb', padx=10).grid(row=4, column=0, padx=20, pady=20, sticky="w")
    CTkLabel(screen, text='Ngày sinh', bg_color='#ebebeb', padx=10).grid(row=5, column=0, padx=20, pady=20, sticky="w")
    CTkLabel(screen, text='Số điện thoại', bg_color='#ebebeb', padx=10).grid(row=6, column=0, padx=20, pady=20, sticky="w")
    genderVar = StringVar()
    genderVar.set('nam')
    txtID = CTkEntry(screen)
    txtName = CTkEntry(screen)
    txtClass = CTkEntry(screen)
    genderFrame = CTkLabel(screen, bg_color='#ebebeb', padx=10, pady=10)
    male_rb = CTkRadioButton(genderFrame, text='Nam', variable=genderVar, value='nam')
    female_rb = CTkRadioButton(genderFrame, text='Nữ', variable=genderVar, value='nữ')
    txtEmail = CTkEntry(screen)
    dobFrame = CTkFrame(screen, fg_color='#ebebeb')
    dobVar = StringVar()
    dobVar.set('2000-01-01')
    txtDOB = CTkLabel(dobFrame, text=dobVar.get())
    dobBtn = CTkButton(dobFrame, text='Chọn ngày', command=pickDate)
    txtPhone = CTkEntry(screen)

    txtID.grid(row=0, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
    txtName.grid(row=1, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
    txtClass.grid(row=2, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
    genderFrame.grid(row=3, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
    male_rb.grid(row=0, column=0)
    female_rb.grid(row=0, column=1)
    txtEmail.grid(row=4, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
    dobFrame.grid(row=5, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
    txtDOB.grid(row=0, column=0)
    dobBtn.grid(row=0, column=1, padx=30, sticky='e')
    txtPhone.grid(row=6, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

    confirmBtn = CTkButton(screen, width=15, text=buttonTitle, cursor='hand2', 
                           command=lambda: command(txtID, txtName, txtClass, genderVar, txtEmail, dobVar, txtPhone, screen, frame))
    confirmBtn.grid(row=7, column=0, pady=15, sticky='ne')

    def reset():
        txtID.delete(0, END)
        txtName.delete(0, END)
        txtClass.delete(0, END)
        genderVar.set('nam')
        txtEmail.delete(0, END)
        txtDOB.configure(text='2000-01-01')
        txtPhone.delete(0, END)

    resetBtn = CTkButton(screen, width=15, text='Reset', command=reset, cursor='hand2')
    resetBtn.grid(row=7, column=1, pady=15, sticky='ne')

    if title == 'Sửa thông tin sinh viên' and studentTable.focus() != '':
        index = studentTable.focus()
        student = studentTable.item(index)
        studentInfo = student['values']
        txtID.insert(0, studentInfo[0])
        txtName.insert(0, studentInfo[1])
        txtClass.insert(0, studentInfo[2])
        genderVar.set(studentInfo[3])
        txtEmail.insert(0, studentInfo[4])
        txtDOB.configure(text=studentInfo[5])
        txtPhone.insert(0, studentInfo[6])

def addStudent(txtID, txtName, txtClass, genderVar, txtEmail, dobVar, txtPhone, screen, frame):
    if txtID.get() == '':
        alert_message('Bạn cần nhập mã sinh viên')
        txtID.focus_set()
        return
    query = f'''SELECT * FROM students WHERE id="{txtID.get()}"'''
    cursor.execute(query)
    if len(cursor.fetchall()) != 0:
        alert_message('Đã tồn tại mã sinh viên')
        txtID.focus_set()
        return
    if txtName.get() == '':
        alert_message('Bạn cần nhập họ tên')
        txtName.focus_set()
        return
    if genderVar.get() == '':
        alert_message('Bạn cần nhập giới tính')
        return
    query = f'''INSERT INTO students VALUES(%s,%s,%s,%s,%s,%s,%s)'''
    cursor.execute(query, (txtID.get(), txtName.get(), txtClass.get(), genderVar.get(), txtEmail.get(),
             dobVar.get(), txtPhone.get()))
    conn.commit()
    # query = f'''INSERT INTO users VALUES(%s,%s,%s,%s)'''
    # cursor.execute(query, (txtID.get(), 'sinh viên', txtID.get(), txtID.get()))
    # conn.commit()
    success_message('Thêm mới thành công')  
    screen.destroy()
    showStudent(frame)

def updateStudent(txtID, txtName, txtClass, genderVar, txtEmail, dobVar, txtPhone, screen, frame):
    if studentTable.focus != '':
        if yesno_message('Bạn có chắc chắc muốn sửa?') == True:
            query = '''UPDATE students
            SET hoten=%s, lop=%s, gioitinh=%s, email=%s, dob=%s, sdt=%s
            WHERE id=%s'''
            cursor.execute(query, (txtName.get(), txtClass.get(), genderVar.get(),
                txtEmail.get(), dobVar.get(), txtPhone.get(),txtID.get()))
            conn.commit()
            success_message('Sửa thành công')
            screen.destroy()
            showStudent(frame)
        else: screen.destroy()

def searchStudent(txtID, txtName, txtClass, genderVar, txtEmail, dobVar, txtPhone, screen, frame):
    query = f'''SELECT * FROM students WHERE
        id="{txtID.get()}" OR hoten="{txtName.get()}" OR gioitinh="{genderVar.get()}" OR 
        email="{txtEmail.get()}" OR dob="{dobVar.get()}" OR sdt="{txtPhone.get()}" OR
        lop="{txtClass.get()}"'''
    cursor.execute(query)
    studentTable.delete(*studentTable.get_children())
    result = cursor.fetchall()
    for data in result:
        studentTable.insert('', END, values=data)
    screen.destroy()

def deleteStudent(frame):
    if studentTable.focus() != '':
        if yesno_message('Bạn có chắc chắc muốn xoá?') == True:
            index = studentTable.selection()
            student = studentTable.item(index)
            studentID = student['values'][0]
            query = '''DELETE FROM students WHERE id=%s'''
            cursor.execute(query, (studentID,))
            conn.commit()
            success_message('Xoá thành công')
            showStudent(frame)

def showStudent(frame):
    global studentTable
    for x in frame.winfo_children():
        x.destroy()
    
    columns = ['#1','#2','#3','#4','#5','#6','#7']
    studentTable = Treeview(frame, columns=columns, show='headings')
    studentTable.heading('#1', text='Mã sinh viên')
    studentTable.heading('#2', text='Họ tên')
    studentTable.heading('#3', text='Lớp')
    studentTable.heading('#4', text='Giới tính')
    studentTable.heading('#5', text='Email')
    studentTable.heading('#6', text='Ngày sinh')
    studentTable.heading('#7', text='Số điện thoại')
    style = Style()
    style.configure('Treeview', rowheight=40, font=('', 13))
    style.configure('Treeview.Heading', font=('', 15))
    studentTable.grid(row=0, column=0, columnspan=4, sticky='nsew')
    # studentTable.pack()

    button_frame = CTkFrame(frame, fg_color='#ebebeb', bg_color='#ebebeb')
    button_frame.grid(row=1, column=0, columnspan=4, sticky='ew', pady=10)
    query = '''SELECT * FROM students'''
    cursor.execute(query)
    result = cursor.fetchall()
    for data in result:
        studentTable.insert('', END, values=data)

    addBtn = CTkButton(button_frame, text='Thêm', command=lambda: studentToplevel('Thêm sinh viên', 'Thêm', addStudent, frame))
    addBtn.place(x=20, y=165)
    # addBtn.grid(row=0, column=0, padx=5)

    updateBtn = CTkButton(button_frame, text='Sửa', command=lambda: studentToplevel('Sửa thông tin sinh viên', 'Cập nhật', updateStudent, frame))
    updateBtn.place(x=220, y=165)
    # updateBtn.grid(row=0, column=1, padx=5)

    searchBtn = CTkButton(button_frame, text='Tìm kiếm', command=lambda: studentToplevel('Tìm kiếm sinh viên', 'Tìm kiếm', searchStudent, frame))
    searchBtn.place(x=420, y=165)
    # searchBtn.grid(row=0, column=2, padx=5)

    deleteBtn = CTkButton(button_frame, text='Xoá', command=lambda: deleteStudent(frame))
    deleteBtn.place(x=620, y=165)
    # deleteBtn.grid(row=0, column=3, padx=5)