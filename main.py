from tkinter import *
from tkinter import ttk
from random import *
from tkcalendar import Calendar
from datetime import *
import mysql.connector as mysql
from math import *
from tkinter import messagebox
import re
import xlrd
from tkinter import filedialog
import csv
import os
from babel import *

connect = mysql.connect(host='localhost', 
                   user='root',
                   password='',
                   database="test")
    
mycursor = connect.cursor()

class Page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()
        
class generatePayroll(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        mydata = []
        def calpayroll():
            global mydata
            try:
                listx = []
                x = []
                
                trv.delete(*trv.get_children())
                total_days = int(q.get())
                file_path = importExcel()
                loc = (r"" + file_path)
                wb = xlrd.open_workbook(loc)
                sheet = wb.sheet_by_index(0)
                sheet.cell_value(0, 0)

                for i in range(1, sheet.nrows):
                    listx.append(sheet.row_values(i))
                    
                for i in listx:
                    gross_salary = f"(basic_salary + hra + oa) * ({i[2]}/{total_days}) "
                    deductions = f"(0.12 * basic_salary * ({i[2]}/{total_days})) + (0.25 * (basic_salary+hra+oa) * ({i[2]}/{total_days})) + 200 "
                    net_salary = f"{gross_salary} - ({deductions})"
                    query = f"SELECT emp_id, name, DOB, department, {gross_salary}, {deductions}, {net_salary} from employees WHERE emp_id = '{i[0]}'"
                    mycursor.execute(query)
                    rows = mycursor.fetchall()
                    x.append(list(rows[0]))
                for j in x:
                    j[4] = round(j[4])
                    j[5] = round(j[5])
                    j[6] = round(j[6])
                    trv.insert('', 'end', values=j)
                    
                    mydata = x.copy()
            except ValueError:
                messagebox.showerror("Payroll Management System", "Please Enter Total No. of Working Days to Proceed")
            
        def importExcel():
            file_path = filedialog.askopenfilename()
            return file_path

        def exportCSV():
            global mydata
            if len(mydata) < 1:
                messagebox.showerror("Payroll Management System", "No data available")
            else:
                fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save CSV", filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")))
                print(fln)
                with open(fln, mode='w+', newline='') as myfile:
                    exp_writer = csv.writer(myfile, delimiter=',')
                    exp_writer.writerow(["Employee ID", "Name", "DOB", "Department", "Gross Salary", "Deductions", "Net Salary"])
                    for i in mydata:
                        exp_writer.writerow(i)
                messagebox.showinfo("Payroll Management System", "Data Exported Successfully")
                os.system(fln)

        # Frames Section
        wrapper2 = LabelFrame(self, text="Actions")
        wrapper2.pack(fill=BOTH, expand=YES, padx=20, pady=10)
        wrapper1 = LabelFrame(self, text="Employee List")
        wrapper1.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        tree_frame = Frame(wrapper1)
        tree_frame.pack(padx=20, pady=20)

        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        trv = ttk.Treeview(tree_frame, columns=(1,2,3,4,5,6,7), show="headings", yscrollcommand=tree_scroll.set, height= 25)
        trv.pack()

        tree_scroll.config(command=trv.yview)

        trv.heading(1, text="Employee ID")
        trv.heading(2, text="Name")
        trv.heading(3, text="DOB")
        trv.heading(4, text="Department")
        trv.heading(5, text="Gross Salary")
        trv.heading(6, text="Deductions")
        trv.heading(7, text="Net Salary")

        # Actions Section
        q = StringVar()

        lbl = Label(wrapper2, text="Total No. of Working Days: ")
        lbl.pack(side=LEFT, padx=10)

        ent = Entry(wrapper2, textvariable=q)
        ent.pack(side=LEFT, padx=10)

        btn = Button(wrapper2, text="Generate Payroll", command=calpayroll)
        btn.pack(side=LEFT, padx=10)

        btn1 = Button(wrapper2, text="Export to Excel", command=exportCSV)
        btn1.pack(side=LEFT, padx=10)

class veiwEmployees(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)        
        def update_rows():
            gross_salary = f"(basic_salary + hra + oa) "
            deductions = f"(0.12 * basic_salary) + (0.25 * (basic_salary+hra+oa)) + 200 "
            net_salary = f"{gross_salary} - ({deductions})"
            selectquery = f"SELECT emp_id, name, DOB, department, {gross_salary}, {deductions}, {net_salary} from employees"
            mycursor.execute(selectquery)
            rows = mycursor.fetchall()
            trv.delete(*trv.get_children())
            for i in rows:
                trv.insert('', 'end', values=i)

        def search():
            update_rows()
            q2 = q.get()
            query = "SELECT emp_id, name, DOB, department, basic_salary+hra+oa, ((0.12 * basic_salary) + (0.25 * basic_salary+hra+oa) + 200), (basic_salary+hra+oa) - ((0.12 * basic_salary) + (0.25 * basic_salary+hra+oa) + 200) from employees WHERE name LIKE '%"+q2+"%'"
            mycursor.execute(query)
            rows = mycursor.fetchall()
            trv.delete(*trv.get_children())
            for i in rows:
                trv.insert('', 'end', values=i)

        def edit():
            selected = trv.focus()
            values = trv.item(selected, 'values')

            query = "SELECT * FROM employees WHERE emp_id = '{}'".format(str(values[0]))
            mycursor.execute(query)
            rows = mycursor.fetchall()
            print(rows[0])
            
            top = Toplevel()
            top.title("Edit Employee Data")    
            group_1 = StringVar()
            fontType = ("Times New Roman", 13)
            frame = LabelFrame(top, text="Personal Details", font= fontType)
            frame.pack(pady= 0, padx= 50, ipadx= 20, ipady= 0, side=LEFT)

            def set_text():
                e1.insert(0, rows[0][1])
                e2.insert(0, rows[0][2])
                e3.insert(0, rows[0][3])
                e4.insert(END, rows[0][4])
                e5.insert(0, rows[0][5])
                e6.insert(0, rows[0][6])
                date.config(text= rows[0][7])
                e8.insert(0, rows[0][9])
                e9.insert(0, rows[0][10])
                e10.insert(0, rows[0][11])
                e11.insert(0, rows[0][12])
                bse.insert(0, rows[0][13])
                hrae.insert(0, rows[0][14])
                oae.insert(0, rows[0][15])
                calDeduction()
                
            def calDeduction():
                try:
                    bs = float(bse.get())
                    pf = (12/100) * bs
                    epfe.config(text = str(pf))
                except ValueError:
                    epfe.config(text = "Invalid Input")
                    
                try:
                    gross = float(bse.get()) + float(hrae.get()) + float(oae.get())
                    tds = (25/100) * gross
                    ite.config(text = str(tds))
                except ValueError:
                    ite.config(text = "Invalid Input")
            
                pte.config(text = str(200))
            
            def grad_date():
                date.config(text = cal.get_date())
                
            def check_email():
                if re.match("^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", e2.get()) == None:
                    return True
                else:
                    return False
            
            def check_phone():
                if re.match("^[0-9]{10}$", e3.get()) == None:
                    return True
                else:
                    return False
            
            def check_account():
                if re.match("^[0-9]{9,18}$", e9.get()) == None:
                    return True
                else:
                    return False
                
            def check_data():
                if  e1.get() == "": 
                    messagebox.showerror("Payroll Management System", "Please Enter Full Name to Proceed")
                    return False
                elif e2.get() == "": 
                    messagebox.showerror("Payroll Management System", "Please Enter Email to Proceed")
                    return False
                elif e3.get() == "":
                    messagebox.showerror("Payroll Management System", "Please Enter Contact Number to Proceed")
                    return False
                elif e4.get("1.0",'end-1c') == "":
                    messagebox.showerror("Payroll Management System", "Please Enter Address to Proceed")
                    return False 
                elif e5.get() == "":
                    messagebox.showerror("Payroll Management System", "Please Enter City to Proceed")
                    return False
                elif e6.get() == "":
                    messagebox.showerror("Payroll Management System", "Please Enter State to Proceed")
                    return False
                elif date.cget("text") == "":
                    messagebox.showerror("Payroll Management System", "Please Select DOB to Proceed")
                    return False
                elif group_1.get() == "":
                    messagebox.showerror("Payroll Management System", "Please Select Gender to Proceed")
                    return False
                elif e8.get() == "":
                    messagebox.showerror("Payroll Management System", "Please Enter Bank Name to Proceed")
                    return False
                elif e9.get() == "":
                    messagebox.showerror("Payroll Management System", "Please Enter Account Number to Proceed")
                    return False
                elif e10.get() == "":
                    messagebox.showerror("Payroll Management System", "Please Enter Department to Proceed")
                    return False
                elif e11.get() == "":
                    messagebox.showerror("Payroll Management System", "Please Enter Position to Proceed")
                    return False
                elif bse.get() == "":
                    messagebox.showerror("Payroll Management System", "Please Enter Basic Salary to Proceed")
                    return False
                elif hrae.get() == "":
                    messagebox.showerror("Payroll Management System", "Please Enter HRA to Proceed")
                    return False
                elif oae.get() == "":
                    messagebox.showerror("Payroll Management System", "Please Enter Other Allowances to Proceed")
                    return False
                elif check_email():
                    messagebox.showerror("Payroll Management System", "Please Enter Valid Email to Proceed")
                    return False
                elif check_phone():
                    messagebox.showerror("Payroll Management System", "Please Enter Valid Phone Number to Proceed")
                    return False
                elif check_account():
                    messagebox.showerror("Payroll Management System", "Please Enter Valid Account Number to Proceed")
                    return False
                # elif epfe.cget("text") == "": 
                
                # elif ite.cget("text") == "":
                
                # elif pte.cget("text") == "":
                    
                else:
                    return True
            
            def update_record():
                calDeduction()
                if check_data():
                    update_query = "UPDATE employees SET name = %s, email = %s, contact_no = %s, address = %s, city = %s, state = %s, dob = %s, gender = %s, bank_name = %s, account_no = %s, department = %s, position = %s, basic_salary = %s, hra = %s, oa = %s WHERE emp_id = '{}'".format(str(values[0]))
                    val = (e1.get(), e2.get(), e3.get(), e4.get("1.0",'end-1c'), e5.get(), e6.get(), date.cget("text"), group_1.get(), e8.get(), e9.get(), e10.get(), e11.get(), bse.get(), hrae.get(), oae.get())
                    
                    mycursor.execute(update_query, val)
                    connect.commit()
                    
                    update_rows()
                    top.destroy()
                
            l1 = Label(frame, text = "Full Name", font= fontType).grid(row = 0, column = 0, sticky = W, pady = 10, padx = 5)
            l2 = Label(frame, text = "Email", font= fontType).grid(row = 1, column = 0, sticky = W, pady = 10, padx = 5)
            l3 = Label(frame, text = "Contact Number", font= fontType).grid(row = 2, column = 0, sticky = W, pady = 10, padx = 5)
            l4 = Label(frame, text = "Address", font= fontType).grid(row = 3, column = 0, sticky = W, pady = 10, padx = 5)
            l5 = Label(frame, text = "City", font= fontType).grid(row = 4, column = 0, sticky = W, pady = 10, padx = 5)
            l6 = Label(frame, text = "State", font= fontType).grid(row = 5, column = 0, sticky = W, pady = 10, padx = 5)
            l7 = Label(frame, text = "DOB", font= fontType).grid(row = 6, column = 0, sticky = W, pady = 10, padx = 5)
            l8 = Label(frame, text = "Selected Date", font= fontType).grid(row = 8, column = 0, sticky = W, pady = 10, padx = 5)
            l13 = Label(frame, text = "Gender", font= fontType).grid(row = 9, column = 0, sticky = W, pady = 10, padx = 5)
            
            e1 = Entry(frame, width= 35)
            e1.grid(row = 0, column = 1) 
            
            e2 = Entry(frame, width= 35)
            e2.grid(row = 1, column = 1)
            
            e3 = Entry(frame, width= 35)
            e3.grid(row = 2, column = 1)
            
            e4 = Text(frame, width= 35, height= 7)
            e4.grid(row = 3, column = 1)
            
            e5 = Entry(frame, width= 35)
            e5.grid(row = 4, column = 1)
            
            e6 = Entry(frame, width= 35)
            e6.grid(row = 5, column = 1)

            cal = Calendar(frame, selectmode = 'day', year = datetime.today().year, month = datetime.today().month, day = datetime.today().day, date_pattern = "y-mm-dd")
            cal.grid(row = 6, column = 1)
                    
            b1 = Button(frame, text = "Get Date", command = grad_date, font=fontType)
            b1.grid(row = 7, column = 1, pady=15)
            date = Label(frame, text = "", font=fontType)
            date.grid(row = 8, column = 1)

            frame1 = LabelFrame(frame, text='')
            frame1.grid(row = 9, column = 1, padx=10)

            Radiobutton(frame1, text='Male', variable=group_1, value="Male", font=("Times New Roman", 13)).pack(side=LEFT, padx=10)
            Radiobutton(frame1, text='Female', variable=group_1, value="Female", font=("Times New Roman", 13)).pack(side=LEFT, padx=10)
            Radiobutton(frame1, text='Other', variable=group_1, value="Other", font=("Times New Roman", 13)).pack(side=LEFT, padx=10)
            
            if rows[0][8] == "male" or rows[0][8] == "Male":
                group_1.set("Male")
            elif rows[0][8] == "female" or rows[0][8] == "Female":
                group_1.set("Female")
            else:
                group_1.set("Other")
                
            frame4 = LabelFrame(top, text="Corporate Details", font= fontType)
            frame4.pack(pady= 10, padx= 0, ipadx= 20, ipady= 10, side=TOP)
            
            l9 = Label(frame4, text = "Bank Name", font= fontType).grid(row = 8, column = 0, sticky = W, pady = 10, padx = 5)
            l10 = Label(frame4, text = "Account Number", font= fontType).grid(row = 9, column = 0, sticky = W, pady = 10, padx = 5)
            l11 = Label(frame4, text = "Department", font= fontType).grid(row = 10, column = 0, sticky = W, pady = 10, padx = 5)
            l12 = Label(frame4, text = "Position", font= fontType).grid(row = 11, column = 0, sticky = W, pady = 10, padx = 5)
            
            e8 = Entry(frame4, width= 35)
            e8.grid(row = 8, column = 1)
            e9 = Entry(frame4, width= 35)
            e9.grid(row = 9, column = 1)
            e10 = Entry(frame4, width= 35)
            e10.grid(row = 10, column = 1)
            e11 = Entry(frame4, width= 35)
            e11.grid(row = 11, column = 1)    
            
            frame2 = LabelFrame(top, text="Gross Salary", font= fontType)
            frame2.pack(pady= 10, padx= 0, ipadx= 20, ipady= 10, side=TOP)

            bs = Label(frame2, text = "Basic Salary", font= fontType).grid(row = 0, column = 0, sticky = W, pady = 10, padx = 5)
            hra = Label(frame2, text = "HRA", font= fontType).grid(row = 1, column = 0, sticky = W, pady = 10, padx = 5)
            oa = Label(frame2, text = "Other Allowances", font= fontType).grid(row = 2, column = 0, sticky = W, pady = 10, padx = 5)

            bse = Entry(frame2, width= 35)
            bse.grid(row = 0, column = 2)
            hrae = Entry(frame2, width= 35)
            hrae.grid(row = 1, column = 2)
            oae = Entry(frame2, width= 35)
            oae.grid(row = 2, column = 2)

            button1 = Button(frame2, text="Calculate Deductions", command = calDeduction, font=("Times New Roman", 13)).grid(row = 3, column = 2)

            frame3 = LabelFrame(top, text="Deductions", font= fontType)
            frame3.pack(pady= 20, padx= 0, ipadx= 20, ipady= 10, side=TOP)

            epf = Label(frame3, text = "Employer's Provident Fund: ", font= fontType).grid(row = 0, column = 0, sticky = W, pady = 10, padx = 5)
            it = Label(frame3, text = "Income Tax: ", font= fontType).grid(row = 1, column = 0, sticky = W, pady = 10, padx = 5)
            pt = Label(frame3, text = "Professional Tax: ", font= fontType).grid(row = 2, column = 0, sticky = W, pady = 10, padx = 5)

            epfe = Label(frame3, text = "0.00", font= fontType)
            epfe.grid(row = 0, column = 1, sticky = W, pady = 10, padx = 5)
            ite = Label(frame3, text = "0.00", font= fontType)
            ite.grid(row = 1, column = 1, sticky = W, pady = 10, padx = 5)
            pte = Label(frame3, text = "0.00", font= fontType)
            pte.grid(row = 2, column = 1, sticky = W, pady = 10, padx = 5)

            button2 = Button(frame3, text="Update Employee Data", command = update_record, font=("Times New Roman", 13)).grid(row = 3, column = 1)
            set_text()
            
            width = win.winfo_screenwidth() 
            height = win.winfo_screenheight()
            top.geometry(f"{width}x{height}+0+0")
            top.mainloop()

        def delete_record():
            selected = trv.focus()
            values = trv.item(selected, 'values')
            
            res = messagebox.askquestion("Payroll Management System", "Are you sure you want to Delete this record?")
            if res == 'yes':
                delete_query = "DELETE from employees WHERE emp_id = '{}'".format(str(values[0]))
                mycursor.execute(delete_query)
                connect.commit()
                update_rows()
            else:
                pass        
        # Frames Section
        wrapper2 = LabelFrame(self, text="Actions")
        wrapper2.pack(fill=BOTH, expand=YES, padx=20, pady=10)
        wrapper1 = LabelFrame(self, text="Employee List")
        wrapper1.pack(fill=BOTH, expand=YES, padx=20, pady=10)
       
        tree_frame = Frame(wrapper1)
        tree_frame.pack(padx=20, pady=20)

        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        trv = ttk.Treeview(tree_frame, columns=(1,2,3,4,5,6,7), show="headings", yscrollcommand=tree_scroll.set, height= 25)
        trv.pack()

        tree_scroll.config(command=trv.yview)

        trv.heading(1, text="Employee ID")
        trv.heading(2, text="Name")
        trv.heading(3, text="DOB")
        trv.heading(4, text="Department")
        trv.heading(5, text="Gross Salary")
        trv.heading(6, text="Deductions")
        trv.heading(7, text="Net Salary")

        update_rows()
        
        # Actions Section
        q = StringVar()

        lbl = Label(wrapper2, text="Search")
        lbl.pack(side=LEFT, padx=10)

        ent = Entry(wrapper2, textvariable=q)
        ent.pack(side=LEFT, padx=10)

        btn = Button(wrapper2, text="Search Records", command=search)
        btn.pack(side=LEFT, padx=10)

        btn1 = Button(wrapper2, text="Update Records", command=edit)
        btn1.pack(side=LEFT, padx=10)   

        btn2 = Button(wrapper2, text="Delete Record", command=delete_record)
        btn2.pack(side=LEFT, padx=10)
        
        btn3 = Button(wrapper2, text="Update Table", command=update_rows)
        btn3.pack(side=LEFT, padx=10)

        lbl1 = Label(wrapper2, text="")
        lbl1.pack(side=LEFT, padx=10)

class registerEmployee(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        
        group_1 = StringVar()
        fontType = ("Times New Roman", 13)
        frame = LabelFrame(self, text="Personal Details", font= fontType)
        frame.pack(pady= 0, padx= 50, ipadx= 20, ipady= 0, side=LEFT)

        def calDeduction():
            try:
                bs = float(bse.get())
                pf = (12/100) * bs
                epfe.config(text = str(pf))
            except ValueError:
                epfe.config(text = "Invalid Input")
                
            try:
                gross = float(bse.get()) + float(hrae.get()) + float(oae.get())
                tds = (25/100) * gross
                ite.config(text = str(tds))
            except ValueError:
                ite.config(text = "Invalid Input")
        
            pte.config(text = str(200))
        
        def grad_date():
            date.config(text = cal.get_date())
            
        def check_email():
            if re.match("^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", e2.get()) == None:
                return True
            else:
                return False
        
        def check_phone():
            if re.match("^[0-9]{10}$", e3.get()) == None:
                return True
            else:
                return False
        
        def check_account():
            if re.match("^[0-9]{9,18}$", e9.get()) == None:
                return True
            else:
                return False
            
        def check_data():
            if  e1.get() == "": 
                messagebox.showerror("Payroll Management System", "Please Enter Full Name to Proceed")
                return False
            elif e2.get() == "": 
                messagebox.showerror("Payroll Management System", "Please Enter Email to Proceed")
                return False
            elif e3.get() == "":
                messagebox.showerror("Payroll Management System", "Please Enter Contact Number to Proceed")
                return False
            elif e4.get("1.0",'end-1c') == "":
                messagebox.showerror("Payroll Management System", "Please Enter Address to Proceed")
                return False 
            elif e5.get() == "":
                messagebox.showerror("Payroll Management System", "Please Enter City to Proceed")
                return False
            elif e6.get() == "":
                messagebox.showerror("Payroll Management System", "Please Enter State to Proceed")
                return False
            elif date.cget("text") == "":
                messagebox.showerror("Payroll Management System", "Please Select DOB to Proceed")
                return False
            elif group_1.get() == "":
                messagebox.showerror("Payroll Management System", "Please Select Gender to Proceed")
                return False
            elif e8.get() == "":
                messagebox.showerror("Payroll Management System", "Please Enter Bank Name to Proceed")
                return False
            elif e9.get() == "":
                messagebox.showerror("Payroll Management System", "Please Enter Account Number to Proceed")
                return False
            elif e10.get() == "":
                messagebox.showerror("Payroll Management System", "Please Enter Department to Proceed")
                return False
            elif e11.get() == "":
                messagebox.showerror("Payroll Management System", "Please Enter Position to Proceed")
                return False
            elif bse.get() == "":
                messagebox.showerror("Payroll Management System", "Please Enter Basic Salary to Proceed")
                return False
            elif hrae.get() == "":
                messagebox.showerror("Payroll Management System", "Please Enter HRA to Proceed")
                return False
            elif oae.get() == "":
                messagebox.showerror("Payroll Management System", "Please Enter Other Allowances to Proceed")
                return False
            elif check_email():
                messagebox.showerror("Payroll Management System", "Please Enter Valid Email to Proceed")
                return False
            elif check_phone():
                messagebox.showerror("Payroll Management System", "Please Enter Valid Phone Number to Proceed")
                return False
            elif check_account():
                messagebox.showerror("Payroll Management System", "Please Enter Valid Account Number to Proceed")
                return False
            # elif epfe.cget("text") == "": 
            
            # elif ite.cget("text") == "":
            
            # elif pte.cget("text") == "":
                
            else:
                return True
        
        def clear_data():
            e1.delete(0, END)
            e2.delete(0, END)
            e3.delete(0, END)
            e4.delete('1.0', END)
            e5.delete(0, END)
            e6.delete(0, END)
            date.config(text= "")
            e8.delete(0, END)
            e9.delete(0, END)
            e10.delete(0, END)
            e11.delete(0, END)
            bse.delete(0, END)
            hrae.delete(0, END)
            oae.delete(0, END)
            epfe.config(text= "")
            ite.config(text= "")
            pte.config(text= "")
            group_1 = ""
        
        def register_employee():
            calDeduction()
            if check_data():
                insertquery = "INSERT INTO employees (emp_id, name, email, contact_no, address, city, state, dob, gender, bank_name, account_no, department, position, basic_salary, hra, oa) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                emp_id = "emp_" + str(randint(1000, 1999))
                val = (emp_id, e1.get(), e2.get(), e3.get(), e4.get("1.0",'end-1c'), e5.get(), e6.get(), date.cget("text"), group_1.get(), e8.get(), e9.get(), e10.get(), e11.get(), bse.get(), hrae.get(), oae.get())
                mycursor.execute(insertquery, val)
                connect.commit()
                messagebox.showinfo("Payroll Management System", "Employee Registered")
                clear_data()
                
            else:
                messagebox.showinfo("Payroll Management System", "Employee Not Registered. Please Try again")
                
        l1 = Label(frame, text = "Full Name", font= fontType).grid(row = 0, column = 0, sticky = W, pady = 10, padx = 5)
        l2 = Label(frame, text = "Email", font= fontType).grid(row = 1, column = 0, sticky = W, pady = 10, padx = 5)
        l3 = Label(frame, text = "Contact Number", font= fontType).grid(row = 2, column = 0, sticky = W, pady = 10, padx = 5)
        l4 = Label(frame, text = "Address", font= fontType).grid(row = 3, column = 0, sticky = W, pady = 10, padx = 5)
        l5 = Label(frame, text = "City", font= fontType).grid(row = 4, column = 0, sticky = W, pady = 10, padx = 5)
        l6 = Label(frame, text = "State", font= fontType).grid(row = 5, column = 0, sticky = W, pady = 10, padx = 5)
        l7 = Label(frame, text = "DOB", font= fontType).grid(row = 6, column = 0, sticky = W, pady = 10, padx = 5)
        l8 = Label(frame, text = "Selected Date", font= fontType).grid(row = 8, column = 0, sticky = W, pady = 10, padx = 5)
        l13 = Label(frame, text = "Gender", font= fontType).grid(row = 9, column = 0, sticky = W, pady = 10, padx = 5)
        
        e1 = Entry(frame, width= 35)
        e1.grid(row = 0, column = 1) 
        
        e2 = Entry(frame, width= 35)
        e2.grid(row = 1, column = 1)
        
        e3 = Entry(frame, width= 35)
        e3.grid(row = 2, column = 1)
        
        e4 = Text(frame, width= 35, height= 7)
        e4.grid(row = 3, column = 1)
        
        e5 = Entry(frame, width= 35)
        e5.grid(row = 4, column = 1)
        
        e6 = Entry(frame, width= 35)
        e6.grid(row = 5, column = 1)

        cal = Calendar(frame, selectmode = 'day', year = datetime.today().year, month = datetime.today().month, day = datetime.today().day, date_pattern = "y-mm-dd")
        cal.grid(row = 6, column = 1)
             
        b1 = Button(frame, text = "Get Date", command = grad_date, font=fontType)
        b1.grid(row = 7, column = 1, pady=15)
        date = Label(frame, text = "", font=fontType)
        date.grid(row = 8, column = 1)

        frame1 = LabelFrame(frame, text='')
        frame1.grid(row = 9, column = 1, padx=10)

        Radiobutton(frame1, text='Male', variable=group_1, value="Male", font=("Times New Roman", 13)).pack(side=LEFT, padx=10)
        Radiobutton(frame1, text='Female', variable=group_1, value="Female", font=("Times New Roman", 13)).pack(side=LEFT, padx=10)
        Radiobutton(frame1, text='Other', variable=group_1, value="Other", font=("Times New Roman", 13)).pack(side=LEFT, padx=10)
        
        frame4 = LabelFrame(self, text="Corporate Details", font= fontType)
        frame4.pack(pady= 10, padx= 0, ipadx= 20, ipady= 10, side=TOP)
        
        l9 = Label(frame4, text = "Bank Name", font= fontType).grid(row = 8, column = 0, sticky = W, pady = 10, padx = 5)
        l10 = Label(frame4, text = "Account Number", font= fontType).grid(row = 9, column = 0, sticky = W, pady = 10, padx = 5)
        l11 = Label(frame4, text = "Department", font= fontType).grid(row = 10, column = 0, sticky = W, pady = 10, padx = 5)
        l12 = Label(frame4, text = "Position", font= fontType).grid(row = 11, column = 0, sticky = W, pady = 10, padx = 5)
        
        e8 = Entry(frame4, width= 35)
        e8.grid(row = 8, column = 1)
        e9 = Entry(frame4, width= 35)
        e9.grid(row = 9, column = 1)
        e10 = Entry(frame4, width= 35)
        e10.grid(row = 10, column = 1)
        e11 = Entry(frame4, width= 35)
        e11.grid(row = 11, column = 1)    
        
        frame2 = LabelFrame(self, text="Gross Salary", font= fontType)
        frame2.pack(pady= 10, padx= 0, ipadx= 20, ipady= 10, side=TOP)

        bs = Label(frame2, text = "Basic Salary", font= fontType).grid(row = 0, column = 0, sticky = W, pady = 10, padx = 5)
        hra = Label(frame2, text = "HRA", font= fontType).grid(row = 1, column = 0, sticky = W, pady = 10, padx = 5)
        oa = Label(frame2, text = "Other Allowances", font= fontType).grid(row = 2, column = 0, sticky = W, pady = 10, padx = 5)

        bse = Entry(frame2, width= 35)
        bse.grid(row = 0, column = 2)
        hrae = Entry(frame2, width= 35)
        hrae.grid(row = 1, column = 2)
        oae = Entry(frame2, width= 35)
        oae.grid(row = 2, column = 2)

        button1 = Button(frame2, text="Calculate Deductions", command = calDeduction, font=("Times New Roman", 13)).grid(row = 3, column = 2)

        frame3 = LabelFrame(self, text="Deductions", font= fontType)
        frame3.pack(pady= 20, padx= 0, ipadx= 20, ipady= 10, side=TOP)

        epf = Label(frame3, text = "Employer's Provident Fund: ", font= fontType).grid(row = 0, column = 0, sticky = W, pady = 10, padx = 5)
        it = Label(frame3, text = "Income Tax: ", font= fontType).grid(row = 1, column = 0, sticky = W, pady = 10, padx = 5)
        pt = Label(frame3, text = "Professional Tax: ", font= fontType).grid(row = 2, column = 0, sticky = W, pady = 10, padx = 5)

        epfe = Label(frame3, text = "0.00", font= fontType)
        epfe.grid(row = 0, column = 1, sticky = W, pady = 10, padx = 5)
        ite = Label(frame3, text = "0.00", font= fontType)
        ite.grid(row = 1, column = 1, sticky = W, pady = 10, padx = 5)
        pte = Label(frame3, text = "0.00", font= fontType)
        pte.grid(row = 2, column = 1, sticky = W, pady = 10, padx = 5)

        button2 = Button(frame3, text="Register Employee Data", command= register_employee,  font=("Times New Roman", 13)).grid(row = 3, column = 1)
        
class MainView(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        
        p1 = registerEmployee(self)
        p2 = veiwEmployees(self)
        p3 = generatePayroll(self)
      
        buttonframe = Frame(self)
        container = Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = Button(buttonframe, text="Register Employee", command=p1.show, font=("Times New Roman", 13))
        b2 = Button(buttonframe, text="View Employees", command=p2.show, font=("Times New Roman", 13))
        b3 = Button(buttonframe, text="Generate Payroll", command=p3.show, font=("Times New Roman", 13))

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")

        p1.show()
        
if __name__ == "__main__":
    win = Tk()
    main = MainView(win)
    main.pack(side="top", fill="both", expand=True)
    win.title("Payroll Dashboard")
    width = win.winfo_screenwidth() 
    height = win.winfo_screenheight()
    win.geometry(f"{width}x{height}+0+0")
    win.mainloop()

