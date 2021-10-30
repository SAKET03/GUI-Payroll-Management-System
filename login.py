from tkinter import *
import os
import mysql.connector as mysql
from tkinter import messagebox

win = Tk()
win.title("Login for Payroll Management System")
fontType = ("Times New Roman", 13)

connect = mysql.connect(host='localhost', 
                   user='root',
                   password='',
                   database="test")
    
mycursor = connect.cursor()

def login():
    username = un.get()
    password = p.get()
    
    if username == "" or password == "":
        messagebox.showerror("Payroll Management System", "Empty Username or Password fields")
    else:
        search_query = "SELECT * FROM `login` WHERE `username` LIKE '%" +username+ "%'"
        mycursor.execute(search_query)
        rows = mycursor.fetchall()
        print(search_query, rows)
        
        if len(rows) >= 1:
            if rows[0][1] == password: 
                messagebox.showinfo("Payroll Management System", "Login Succesful!")  
                win.destroy()
                os.system("python main.py")
            else:
                messagebox.showerror("Payroll Management System", "Invalid Username or Password")
        else:
                messagebox.showerror("Payroll Management System", "Invalid Username or Password")
            
frame = LabelFrame(win, text="Payroll Management System Login", font= fontType)
frame.pack(ipadx=10, ipady=10, pady=100)

un = StringVar()
p = StringVar()

l1 = Label(frame, text = "Username: ", font= fontType)
l1.grid(row = 0, column = 0, sticky = W, pady = 10, padx = 5)
e1 = Entry(frame, width= 35, textvariable=un)
e1.grid(row = 1, column = 0, pady = 10, padx = 5) 

l2 = Label(frame, text = "Password: ", font= fontType)
l2.grid(row = 2, column = 0, sticky = W, pady = 10, padx = 5)        
e2 = Entry(frame, width= 35, textvariable=p, show="*")
e2.grid(row = 3, column = 0, pady = 10, padx = 5)

b1 = Button(frame, text="Login", command=login, font= fontType)
b1.grid(row = 4, column = 0, ipadx=20)

win.geometry(f"500x500")
win.resizable(0,0)
win.mainloop()