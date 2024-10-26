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
# lecturerTable = None

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

def lecturerToplevel(title, buttonTitle, command, frame):
    if title == 'Sửa thông tin giảng viên' and lecturerTable.focus() == '':
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
    txtDepart = CTkEntry(screen)

    CTkLabel(screen, text='Mã giảng viên', bg_color='#ebebeb', padx=10).grid(row=0, column=0, padx=20, pady=20, sticky="w")
    txtID.grid(row=0, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
    
    CTkLabel(screen, text='Họ tên', bg_color='#ebebeb', padx=10).grid(row=1, column=0, padx=20, pady=20, sticky="w")
    txtName.grid(row=1, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
    
    CTkLabel(screen, text='Giới tính', bg_color='#ebebeb', padx=10).grid(row=2, column=0, padx=20, pady=20, sticky="w")
    genderFrame.grid(row=2, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
    male_rb.grid(row=0, column=0)
    female_rb.grid(row=0, column=1)
    
    CTkLabel(screen, text='Email', bg_color='#ebebeb', padx=10).grid(row=3, column=0, padx=20, pady=20, sticky="w")
    txtEmail.grid(row=3, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
    
    CTkLabel(screen, text='Ngày sinh', bg_color='#ebebeb', padx=10).grid(row=4, column=0, padx=20, pady=20, sticky="w")
    dobFrame.grid(row=4, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
    txtDOB.grid(row=0, column=0)
    dobBtn = CTkButton(dobFrame, text='Chọn ngày', command=lambda: pickDate(dobVar, txtDOB))
    dobBtn.grid(row=0, column=1, padx=30, sticky='e')
    
    CTkLabel(screen, text='Số điện thoại', bg_color='#ebebeb', padx=10).grid(row=5, column=0, padx=20, pady=20, sticky="w")
    txtPhone.grid(row=5, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
    
    CTkLabel(screen, text='Phòng ban', bg_color='#ebebeb', padx=10).grid(row=6, column=0, padx=20, pady=20, sticky="w")
    txtDepart.grid(row=6, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

    confirmBtn = CTkButton(screen, width=15, text=buttonTitle, cursor='hand2', 
                           command=lambda: command(txtID, txtName, genderVar, txtEmail, dobVar, txtPhone, txtDepart, screen, frame))
    confirmBtn.grid(row=7, column=0, pady=15, sticky='ne')

    def reset():
        txtID.delete(0, END)
        txtName.delete(0, END)
        genderVar.set('nam')
        txtEmail.delete(0, END)
        txtDOB.configure(text='2000-01-01')
        txtPhone.delete(0, END)
        txtDepart.delete(0, END)

    resetBtn = CTkButton(screen, width=15, text='Reset', command=reset, cursor='hand2')
    resetBtn.grid(row=7, column=1, pady=15, sticky='ne')

    if title == 'Sửa thông tin giảng viên' and lecturerTable.focus() != '':
        index = lecturerTable.focus()
        lecturer = lecturerTable.item(index)
        lecturerInfo = lecturer['values']
        txtID.insert(0, lecturerInfo[0])
        txtName.insert(0, lecturerInfo[1])
        genderVar.set(lecturerInfo[2])
        txtEmail.insert(0, lecturerInfo[3])
        txtDOB.configure(text=lecturerInfo[4])
        txtPhone.insert(0, lecturerInfo[5])
        txtDepart.insert(0, lecturerInfo[6])

def addLecturer(txtID, txtName, genderVar, txtEmail, dobVar, txtPhone, txtDepart, screen, frame):
    if txtID.get() == '':
        alert_message('Bạn cần nhập mã giảng viên')
        txtID.focus_set()
        return
    query = f'''SELECT * FROM lecturers WHERE id="{txtID.get()}"'''
    cursor.execute(query)
    if len(cursor.fetchall()) != 0:
        alert_message('Đã tồn tại mã giảng viên')
        txtID.focus_set()
        return
    if txtName.get() == '':
        alert_message('Bạn cần nhập họ tên')
        txtName.focus_set()
        return
    if genderVar.get() == '':
        alert_message('Bạn cần nhập giới tính')
        return
    query = f'''INSERT INTO lecturers VALUES(%s,%s,%s,%s,%s,%s,%s)'''
    cursor.execute(query, (txtID.get(), txtName.get(), genderVar.get(), txtEmail.get(),
             dobVar.get(), txtPhone.get(), txtDepart.get()))
    conn.commit()
    # query = f'''INSERT INTO users VALUES(%s,%s,%s,%s)'''
    # cursor.execute(query, (txtID.get(), 'giảng viên', txtID.get(), txtID.get()))
    # conn.commit()
    success_message('Thêm mới thành công')  
    screen.destroy()
    showLecturer(frame)

def updateLecturer(txtID, txtName, genderVar, txtEmail, dobVar, txtPhone, txtDepart, screen, frame):
    if lecturerTable.focus() != '':
        if yesno_message('Bạn có chắc chắc muốn sửa?') == True:
            query = '''UPDATE lecturers
            SET id=%s, hoten=%s, gioitinh=%s, email=%s, dob=%s, sdt=%s, phongban=%s
            WHERE id=%s'''
            cursor.execute(query, (txtID.get(),txtName.get(), genderVar.get(), txtEmail.get(), dobVar.get(),
                 txtPhone.get(), txtDepart.get(), txtID.get()))
            conn.commit()
            success_message('Sửa thành công')
            screen.destroy()
            showLecturer(frame)
        else: 
            screen.destroy()

def searchLecturer(txtID, txtName, genderVar, txtEmail, dobVar, txtPhone, txtDepart, screen, frame):
    query = f'''SELECT * FROM lecturers WHERE
        id="{txtID.get()}" OR hoten="{txtName.get()}" OR gioitinh="{genderVar.get()}" OR 
        email="{txtEmail.get()}" OR dob="{dobVar.get()}" OR sdt="{txtPhone.get()}" OR
        phongban="{txtDepart.get()}"'''
    cursor.execute(query)
    lecturerTable.delete(*lecturerTable.get_children())
    result = cursor.fetchall()
    for data in result:
        lecturerTable.insert('', END, values=data)
    screen.destroy()

def deleteLecturer(frame):
    if lecturerTable.focus() != '':
        if yesno_message('Bạn có chắc chắc muốn xoá?') == True:
            index = lecturerTable.focus()
            lecturer = lecturerTable.item(index)
            lecturerID = lecturer['values'][0]
            query = '''DELETE FROM lecturers WHERE id=%s'''
            cursor.execute(query, (lecturerID,))
            conn.commit()
            success_message('Xoá thành công')
            showLecturer(frame)

def showLecturer(frame):
    global lecturerTable
    for x in frame.winfo_children():
        x.destroy()
    
    columns = ['#1','#2','#3','#4','#5','#6','#7']
    lecturerTable = Treeview(frame, columns=columns, show='headings')
    lecturerTable.heading('#1', text='Mã giảng viên')
    lecturerTable.heading('#2', text='Họ tên')
    lecturerTable.heading('#3', text='Giới tính')
    lecturerTable.heading('#4', text='Email')
    lecturerTable.heading('#5', text='Ngày sinh')
    lecturerTable.heading('#6', text='Số điện thoại')
    lecturerTable.heading('#7', text='Phòng ban')
    style = Style()
    style.configure('Treeview', rowheight=40, font=('', 13))
    style.configure('Treeview.Heading', font=('', 15))
    # lecturerTable.pack()
    lecturerTable.grid(row=0, column=0, columnspan=4, sticky='nsew')

    button_frame = CTkFrame(frame, fg_color='#ebebeb', bg_color='#ebebeb')
    button_frame.grid(row=1, column=0, columnspan=4, sticky='ew', pady=10)

    query = '''SELECT * FROM lecturers'''
    cursor.execute(query)
    result = cursor.fetchall()
    for data in result:
        lecturerTable.insert('', END, values=data)

    addBtn = CTkButton(button_frame, text='Thêm', command=lambda: lecturerToplevel('Thêm giảng viên', 'Thêm', addLecturer, frame))
    addBtn.place(x=20, y=165)

    updateBtn = CTkButton(button_frame, text='Sửa', command=lambda: lecturerToplevel('Sửa thông tin giảng viên', 'Cập nhật', updateLecturer, frame))
    updateBtn.place(x=220, y=165)

    searchBtn = CTkButton(button_frame, text='Tìm kiếm', command=lambda: lecturerToplevel('Tìm kiếm giảng viên', 'Tìm kiếm', searchLecturer, frame))
    searchBtn.place(x=420, y=165)

    deleteBtn = CTkButton(button_frame, text='Xoá', command=lambda: deleteLecturer(frame))
    deleteBtn.place(x=620, y=165)