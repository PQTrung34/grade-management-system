from customtkinter import *
from tkinter.ttk import Treeview, Style
from util import *
import mysql.connector
import csv

window = CTk()
window.title('Quản lý điểm sinh viên')
window.geometry('1000x600')
window.resizable(0,0)

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

    gradeBtn.configure(state=NORMAL)
    reportBtn.configure(state=NORMAL)
    exportBtn.configure(state=NORMAL)

connectDBtn = CTkButton(window, text='Kết nối cơ sở dữ liệu', command=connectDatabase)
connectDBtn.place(x=850,y=0)

def updateGrade():
    if gradeTable.focus() != '':
        screen = CTkToplevel()
        screen.grab_set()
        screen.wm_title('Cập nhật điểm')
        CTkLabel(screen, text='Điểm', bg_color='#ebebeb', padx=10).grid(row=0, column=0, padx=20, pady=20, sticky="w")
        txtGrade = CTkEntry(screen)
        txtGrade.grid(row=0, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
        index = gradeTable.focus()
        grade = gradeTable.item(index)
        gradeInfo = grade['values']
        txtGrade.insert(0, gradeInfo[4])
        def updateData():
            if txtGrade.get() == '':
                alert_message('Vui lòng nhập điểm')
                return
            if yesno_message('Bạn có chắc chắc muốn sửa?') == True:
                query = '''UPDATE grades
                SET grade=%s WHERE id=%s AND hoten=%s AND maMon=%s AND tenMon=%s'''
                cursor.execute(query, (txtGrade.get(), gradeInfo[0], gradeInfo[1], gradeInfo[2], gradeInfo[3]))
                conn.commit()
                success_message('Sửa thành công')
                screen.destroy()
                showGrade()
            else: screen.destroy()
        updateBtn = CTkButton(screen, width=15, text='Cập nhật', cursor='hand2', command=updateData)
        updateBtn.grid(row=7, columnspan=2, pady=15)

def addGrade():
    # global screen, txtID, nameVar,txtName, subjectIdVar, subjectNameVar, txtIdSubject, txtNameSubject, txtGrade
    screen = CTkToplevel()
    screen.grab_set()
    screen.wm_title('Thêm điểm')

    CTkLabel(screen, text='Mã sinh viên', bg_color='#ebebeb', padx=10).grid(row=0, column=0, padx=20, pady=20, sticky="w")
    CTkLabel(screen, text='Họ tên', bg_color='#ebebeb', padx=10).grid(row=1, column=0, padx=20, pady=20, sticky="w")
    CTkLabel(screen, text='Mã môn', bg_color='#ebebeb', padx=10).grid(row=2, column=0, padx=20, pady=20, sticky="w")
    CTkLabel(screen, text='Tên môn', bg_color='#ebebeb', padx=10).grid(row=3, column=0, padx=20, pady=20, sticky="w")
    CTkLabel(screen, text='Điểm', bg_color='#ebebeb', padx=10).grid(row=4, column=0, padx=20, pady=20, sticky="w")


    txtID = CTkEntry(screen)
    nameVar = StringVar()
    nameVar.set('')
    txtName = CTkLabel(screen, text=nameVar.get())
    subjectIdVar = StringVar()
    subjectIdVar.set('')
    txtIdSubject = CTkLabel(screen, text=subjectIdVar.get())
    subjectNameVar = StringVar()
    subjectNameVar.set(subjects[0])
    txtNameSubject = CTkOptionMenu(screen, values=subjects, variable=subjectNameVar)
    txtGrade = CTkEntry(screen)

    txtID.grid(row=0, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
    txtName.grid(row=1, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
    txtIdSubject.grid(row=2, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
    txtNameSubject.grid(row=3, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
    txtGrade.grid(row=4, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

    def addData():
        if txtID.get() == '':
            alert_message('Bạn cần nhập mã sinh viên')
            return
        
        cursor.execute('SELECT hoten FROM students WHERE id=%s', (txtID.get(), ))
        res = cursor.fetchall()
        if len(res) == 0:
            alert_message('Không tồn tại sinh viên')
            return
        nameVar.set(res[0][0])
        txtName.configure(text=nameVar.get())

        if subjectNameVar.get() == '':
            alert_message('Bạn cần chọn môn')
            return
        
        cursor.execute('SELECT * FROM grades WHERE id=%s AND tenMon=%s', (txtID.get(), subjectNameVar.get(), ))
        res = cursor.fetchall()
        if len(res) != 0:
            alert_message('Điểm đã có trên hệ thống')
            return
        
        subjectIdVar.set(idSubjects[subjects.index(subjectNameVar.get())])
        txtIdSubject.configure(text=subjectIdVar.get())

        if txtGrade.get() == '':
            alert_message('Bạn cần nhập điểm')
            return
        query = '''INSERT INTO grades VALUES(%s,%s,%s,%s,%s)'''
        cursor.execute(query, (txtID.get(),nameVar.get(), subjectIdVar.get(), subjectNameVar.get(), txtGrade.get()))
        conn.commit()
        success_message('Thêm điểm thành công')
        screen.destroy()
        showGrade()
    confirmBtn = CTkButton(screen, width=15, text='Thêm', cursor='hand2', command=addData)
    confirmBtn.grid(row=7, column=0, pady=15, sticky='ne')

    def reset():
        txtID.delete(0, END)
        txtName.configure(text='')
        txtIdSubject.configure(text=idSubjects[0])
        subjectNameVar.set(subjects[0])
        txtGrade.delete(0, END)
    resetBtn = CTkButton(screen, width=15, text='Reset', command=reset, cursor='hand2')
    resetBtn.grid(row=7, column=1, pady=15, sticky='ne')
    
# Điểm thi
def showGrade():
    for x in viewFrame.winfo_children():
        x.destroy()
    # gradeTable Treeview
    columns = ['#1','#2','#3', '#4', '#5']
    global gradeTable
    gradeTable = Treeview(viewFrame, columns=columns, show='headings',)
    gradeTable.heading('#1', text='Mã sinh viên')
    gradeTable.heading('#2', text='Tên sinh viên')
    gradeTable.heading('#3', text='Mã môn')
    gradeTable.heading('#4', text='Tên môn')
    gradeTable.heading('#5', text='Điểm')
    style = Style()
    style.configure('Treeview',rowheight=40, font=('',13))
    style.configure('Treeview.Heading',font=('',15))
    gradeTable.pack()
    query = '''SELECT * FROM grades'''
    cursor.execute(query)
    result = cursor.fetchall()
    for data in result:
        gradeTable.insert('', END, values=data)

    cursor.execute('SELECT * FROM subjects')
    res = cursor.fetchall()
    global idSubjects, subjects
    idSubjects = []
    subjects = []
    for sub in res:
        idSubjects.append(sub[0])
        subjects.append(sub[1])

    addBtn = CTkButton(viewFrame, text='Thêm', command= addGrade)
    addBtn.place(x=10, y=255)

    updateBtn = CTkButton(viewFrame, text='Sửa', command= updateGrade)
    updateBtn.place(x=200, y=255)
gradeBtn = CTkButton(leftFrame, text='Điểm thi', command=showGrade, state=DISABLED)
gradeBtn.grid(row=0, column=0, pady=30)

# Thống kê
def reportGrade():
    for x in viewFrame.winfo_children():
        x.destroy()
    maxGradeVar = StringVar()
    cursor.execute('SELECT MAX(grade) FROM grades')
    res = cursor.fetchall()
    maxGradeVar.set(res[0][0])
    maxGradeLabel = CTkLabel(viewFrame, text='Điểm cao nhất', width=50, height=100, fg_color='purple',
                             corner_radius=10, font=("Arial", 15), text_color="white")
    CTkLabel(maxGradeLabel, text=maxGradeVar.get(), font=('Arial', 30), text_color="white").place(x=10, y=60)
    maxGradeLabel.place(x=10, y=10)

    minGradeVar = StringVar()
    cursor.execute('SELECT MIN(grade) FROM grades')
    res = cursor.fetchall()
    minGradeVar.set(res[0][0])
    minGradeLabel = CTkLabel(viewFrame, text='Điểm thấp nhất', width=50, height=100, fg_color='purple',
                             corner_radius=10, font=("Arial", 15), text_color="white")
    CTkLabel(minGradeLabel, text=minGradeVar.get(), font=('Arial', 30), text_color="white").place(x=10, y=60)
    minGradeLabel.place(x=200, y=10)
    
    maxGradeSubject = StringVar()
    cursor.execute('''SELECT tenMon, AVG(grade) as avgGrade FROM grades GROUP BY tenMon
            ORDER BY avgGrade DESC''')
    res = cursor.fetchall()
    maxGradeSubject.set(res[0][0])
    maxGradeSubjectLabel = CTkLabel(viewFrame, text='Môn có điểm trung bình cao nhất',width=500, height=100, fg_color='purple',
                             corner_radius=10, font=("Arial", 15), text_color="white")
    CTkLabel(maxGradeSubjectLabel, text=maxGradeSubject.get(), font=('Arial', 30), text_color="white").place(x=10, y=60)
    maxGradeSubjectLabel.place(x=10, y=150)

    minGradeSubject = StringVar()
    cursor.execute('''SELECT tenMon, AVG(grade) as avgGrade FROM grades GROUP BY tenMon
            ORDER BY avgGrade''')
    res = cursor.fetchall()
    minGradeSubject.set(res[0][0])
    minGradeSubjectLabel = CTkLabel(viewFrame, text='Môn có điểm trung bình thấp nhất',width=500, height=100, fg_color='purple',
                             corner_radius=10, font=("Arial", 15), text_color="white")
    CTkLabel(minGradeSubjectLabel, text=minGradeSubject.get(), font=('Arial', 30), text_color="white").place(x=10, y=60)
    minGradeSubjectLabel.place(x=10, y=350)
reportBtn = CTkButton(leftFrame, text='Thống kê', command=reportGrade, state=DISABLED)
reportBtn.grid(row=1, column=0, pady=30)

# Xuất báo cáo
def exportData():
    # data = [('All tyes(*.*)', '*.*'),("csv file(*.csv)","*.csv")]
    # file = filedialog.asksaveasfile(defaultextension='.csv', filetypes=data,)
    cursor.execute('SELECT * FROM grades')
    res = cursor.fetchall()
    with open('data.csv', mode='a') as f:
        exp_writer = csv.writer(f, delimiter=',', dialect='excel')
        for i in res:
            exp_writer.writerow(i)
        success_message('Xuất file thành công')
exportBtn = CTkButton(leftFrame, text='Xuất báo cáo', command=exportData, state=DISABLED)
exportBtn.grid(row=2, column=0, pady=30)

# Đăng xuất
def logout():
    window.destroy()
    import login
logoutBtn = CTkButton(leftFrame, text='Đăng xuất', command=logout)
logoutBtn.grid(row=3, column=0, pady=30)

# Thoát
exitBtn = CTkButton(leftFrame, text='Thoát', command=window.destroy)
exitBtn.grid(row=4, column=0, pady=30)

# viewFrame
viewFrame = CTkFrame(window, width=780, height=500, fg_color='#ebebeb')
viewFrame.place(x=200, y=70)

window.mainloop()