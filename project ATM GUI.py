import sqlite3
import random
from datetime import timedelta, datetime
from tkinter import *
from tkinter import messagebox

connect = sqlite3.connect('Atm.db')
cursor = connect.cursor()
cursor.execute(
    '''
    CREATE TABLE  IF NOT EXISTS user (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    phone_number INTEGER NOT NULL UNIQUE,
    visa_number INTEGER  NOT NULL UNIQUE,
    password INTEGER  NOT NULL,
    cvv INTEGER  NOT NULL UNIQUE,
    exp_date VARCHAR(5) NOT NULL,
    money INTEGER
    )  
    '''
)


class ATMAPP:
    def __init__(self, root):
        self.root = root
        self.root.geometry('500x380+600+120')
        self.root.title('ATM APPLICATION')
        self.root.configure(background='#000000')
        self.root.resizable(False, False)
        title = Label(self.root, text='Welcome - مرحبا ', font=('monospace', 25, 'bold'), background='#000000',
                      fg='#d5c468')
        title.place(x=130, y=40)
        # -------------------------------------BUTONS---------------------------------------------
        btn_withdraw = Button(self.root, background='#d5c468', text='Withdraw', command=self.Withdraw, fg='black',
                              font=('monospace', 14, 'bold'))
        btn_withdraw.place(x=300, y=100, height=50, width=180)

        btn_deposit = Button(self.root, background='#d5c468', command=self.Deposit, text='Deposit', fg='black',
                             font=('monospace', 14, 'bold'))
        btn_deposit.place(x=300, y=200, height=50, width=180)

        btn_show_the_money = Button(self.root, background='#d5c468', command=self.show_money, text='Show money',
                                    fg='black', font=('monospace', 14, 'bold'))
        btn_show_the_money.place(x=10, y=100, height=50, width=180)

        btn_change_the_password = Button(self.root, background='#d5c468', command=self.Change_the_password,
                                         text='Change password', fg='black', font=('monospace', 14, 'bold'))
        btn_change_the_password.place(x=10, y=200, height=50, width=180)

        btn_show_information = Button(self.root, background='#d5c468', command=self.Show_information,
                                      text='information', fg='black', font=('monospace', 14, 'bold'))
        btn_show_information.place(x=150, y=290, height=50, width=180)

    # --------------------------------------------Withdraw-----------------------------------------
    def Withdraw(self):
        self.new_window = Toplevel()
        self.new_window.geometry('500x380+600+120')
        self.new_window.resizable(False, False)
        self.new_window.title('Withdraw')
        self.new_window.configure(background='#000000')
        title = Label(self.new_window, text='Welcome - مرحبا ', font=('monospace', 24, 'bold'), background='#000000',
                      fg='#d5c468')
        title.place(x=130, y=40)
        # --------------------------------------------label cvv----------------------------------------
        l_cvv = Label(self.new_window, text='Enter the cvv', background='#000000', font=('monospace', 14, 'bold'),
                      fg='#d5c468')
        l_cvv.place(x=190, y=100)
        # --------------------------------------------------entry cvv-------------------------------------
        self.E_cvv = Entry(self.new_window, bg='#d5c468', bd=2, width=15, justify='center', fg='black',
                           font=('monospace', 14, 'bold'))
        self.E_cvv.place(x=166, y=130)
        # --------------------------------------------------lable pass------------------------------
        l_password = Label(self.new_window, text='Enter the password', background='#000000',
                           font=('monospace', 14, 'bold'), fg='#d5c468')
        l_password.place(x=160, y=160)
        # ---------------------------------------------------entry pass------------------------------
        self.E_password = Entry(self.new_window, bg='#d5c468', bd=2, justify='center', width=15, fg='black',
                                font=('monospace', 14, 'bold'), show='*')
        self.E_password.place(x=166, y=190)
        # --------------------------------------------------lable amount------------------------------
        l_amount = Label(self.new_window, text='Enter the amount', background='#000000', font=('monospace', 14, 'bold'),
                         fg='#d5c468')
        l_amount.place(x=166, y=220)
        # ------------------------------------------------entry amount--------------------------------
        self.E_amount = Entry(self.new_window, bg='#d5c468', justify='center', bd=2, width=15, fg='black',
                              font=('monospace', 14, 'bold'))
        self.E_amount.place(x=166, y=250)
        # ----------------------------------------------------btn_--------------------------------------
        btn_withdraw = Button(self.new_window, background='#d5c468', command=self.process_Withdraw, text='withdraw',
                              font=('monospace', 20, 'bold'), fg='black')
        btn_withdraw.place(x=166, y=300, height=50, width=170)

    def process_Withdraw(self):
        cvv_number = self.E_cvv.get()
        password = self.E_password.get()

        cursor.execute('SELECT money FROM user WHERE cvv = ? AND password=?', (cvv_number, password,))
        money = cursor.fetchone()
        if len(cvv_number) == 3 and cvv_number.isdigit():
           if len(password) == 4 and password.isdigit():
              if money:
                 amount = int(self.E_amount.get())
                 if amount <= money[0]:
                    new_money = money[0] - amount
                    cursor.execute('UPDATE user SET money = ? WHERE cvv=?', (new_money, cvv_number,))
                    connect.commit()
                    messagebox.showinfo("success", "The withdrawal process was completed successfully")
                    self.new_window.destroy()
                 else:
                    messagebox.showerror("Error","Your balance is insufficient")
                    self.new_window.destroy()
              else:
                  messagebox.showerror("Error", "Password or CVV is invalid")
                  self.new_window.destroy()
           else:
              messagebox.showerror("ERROR", "The password must consist of 4 numbers")
              self.new_window.destroy()
        else:
            messagebox.showerror("ERROR", "The cvv must consist of 3 numbers")
            self.new_window.destroy()



    # ---------------------------------DEPOSIT------------------------------------------------------
    def Deposit(self):
        self.new_window = Toplevel(self.root)
        self.new_window.geometry('500x380+600+120')
        self.new_window.resizable(False, False)
        self.new_window.title('Deposit')
        self.new_window.configure(background='#000000')
        # ------------------------------------------label cvv------------------------------------------
        title = Label(self.new_window, text='Welcome - مرحبا ', font=('monospace', 24, 'bold'), background='#000000',
                      fg='#d5c468')
        title.place(x=130, y=40)
        # --------------------------------------------label cvv----------------------------------------
        l_cvv = Label(self.new_window, text='Enter the cvv', background='#000000', font=('monospace', 14, 'bold'),
                      fg='#d5c468')
        l_cvv.place(x=190, y=100)
        # --------------------------------------------------entry cvv-------------------------------------
        self.E_cvv = Entry(self.new_window, bg='#d5c468', bd=2, width=15, justify='center', fg='black',
                           font=('monospace', 14, 'bold'))
        self.E_cvv.place(x=166, y=130)
        # --------------------------------------------------label pass------------------------------
        l_password = Label(self.new_window, text='Enter the password', background='#000000',
                           font=('monospace', 14, 'bold'), fg='#d5c468')
        l_password.place(x=160, y=160)
        # ---------------------------------------------------entry pass------------------------------
        self.E_password = Entry(self.new_window, bg='#d5c468', bd=2, justify='center', width=15, fg='black',
                                font=('monospace', 14, 'bold'), show='*')
        self.E_password.place(x=166, y=190)
        # --------------------------------------------------label amount------------------------------
        l_amount = Label(self.new_window, text='Enter the amount', background='#000000', font=('monospace', 14, 'bold'),
                         fg='#d5c468')
        l_amount.place(x=166, y=220)
        # ------------------------------------------------entry amount--------------------------------
        self.E_amount = Entry(self.new_window, bg='#d5c468', justify='center', bd=2, width=15, fg='black',
                              font=('monospace', 14, 'bold'))
        self.E_amount.place(x=166, y=250)
        # ----------------------------------------------------------------------------------------
        btn_Deposit = Button(self.new_window, background='#d5c468', command=self.process_Deposit, text='Deposit',
                             font=('monospace', 20, 'bold'), fg='black')
        btn_Deposit.place(x=166, y=300, height=50, width=170)

    def process_Deposit(self):
        cvv_number = self.E_cvv.get()
        password = self.E_password.get()
        cursor.execute('SELECT money from user WHERE cvv = ? AND password=?', (cvv_number, password,))
        money = cursor.fetchone()
        if len(cvv_number) == 3 and cvv_number.isdigit():
           if len(password) == 4 and password.isdigit():
              if money:
                amount = int(self.E_amount.get())
                new_money = money[0] + amount
                cursor.execute('UPDATE user SET money = ? WHERE cvv=?', (new_money, cvv_number,))
                connect.commit()
                messagebox.showinfo("success", "The deposit was completed successfully")
                self.new_window.destroy()
              else:
                  messagebox.showerror("ERROR", "The password must consist of 4 numbers")
                  self.new_window.destroy()
           else:
               messagebox.showerror("ERROR", "The cvv must consist of 3 numbers")
               self.new_window.destroy()

        else:
                messagebox.showerror("Error", "Error in password or cvv")
                self.new_window.destroy()




    # ------------------------------------Show_the_money-----------------------------------------------------
    def show_money(self):
        self.new_window = Toplevel(self.root)
        self.new_window.geometry('500x380+600+120')
        self.new_window.resizable(False, False)
        self.new_window.title('show money')
        self.new_window.configure(background='#000000')
        title = Label(self.new_window, text='Welcome - مرحبا ', font=('monospace', 28, 'bold'), background='#000000',
                      fg='#d5c468')
        title.place(x=127, y=60)
        # ------------------------------------------label cvv------------------------------------------
        l_cvv = Label(self.new_window, text='Enter the cvv', background='#000000', font=('monospace', 14, 'bold'),
                      fg='#d5c468')
        l_cvv.place(x=190, y=130)
        # --------------------------------------------entry cvv-----------------------------------------
        self.E_cvv = Entry(self.new_window, bg='#d5c468', bd=2, width=15, justify='center', fg='#000000',
                           font=('monospace', 14, 'bold'))
        self.E_cvv.place(x=166, y=160)
        # ----------------------------------------------label pass--------------------------------------
        l_password = Label(self.new_window, text='Enter the password', background='#000000',
                           font=('monospace', 14, 'bold'), fg='#d5c468')
        l_password.place(x=160, y=200)
        # -----------------------------------------------entry pass-------------------------------------
        self.E_password = Entry(self.new_window, bg='#d5c468', bd=2, width=15, justify='center', fg='#000000',
                                font=('monospace', 14, 'bold'), show='*')
        self.E_password.place(x=166, y=230)

        # ---------------------------------btn---------------------------------
        btn_show_money = Button(self.new_window, background='#d5c468', command=self.process_show_money, text='show',
                                font=('monospace', 14, 'bold'), fg='#000000')
        btn_show_money.place(x=184, y=290, height=50, width=140)

    # ---------------------------------- process_show_money-------------------------------------
    def process_show_money(self):
        cvv_number = self.E_cvv.get()
        password = self.E_password.get()
        cursor.execute('SELECT  money from user WHERE cvv=? AND password = ?', (cvv_number, password,))
        money = cursor.fetchone()
        if len(cvv_number) == 3 and cvv_number.isdigit():
           if len(password) == 4 and password.isdigit():
              if money:
                 messagebox.showinfo("show money", f"It is in your account: |--{money[0]}--|")
                 self.new_window.destroy()
              else:
                  messagebox.showerror("Error", "opps,Error in password or CVV")
                  self.new_window.destroy()

           else:
               messagebox.showerror("ERROR", "The password must consist of 4 numbers")
               self.new_window.destroy()
        else:
            messagebox.showerror("ERROR", "The cvv must consist of 3 numbers")
            self.new_window.destroy()


    # -------------------------------------Change_the_password -----------------------------------------
    def Change_the_password(self):
        self.new_window = Toplevel(self.root)
        self.new_window.geometry('500x380+600+120')
        self.new_window.resizable(False, False)
        self.new_window.title('show money')
        self.new_window.configure(background='#000000')
        title = Label(self.new_window, text='Welcome - مرحبا ', font=('monospace', 24, 'bold'), background='#000000',
                      fg='#d5c468')
        title.place(x=140, y=37)
        # ------------------------------------------label cvv------------------------------------------
        l_cvv = Label(self.new_window, text='Enter the cvv', background='#000000', font=('monospace', 14, 'bold'),
                      fg='#d5c468')
        l_cvv.place(x=184, y=100)
        # --------------------------------------------entry cvv-----------------------------------------
        self.E_cvv = Entry(self.new_window, bg='#d5c468', bd=2, width=15, justify='center', fg='#000000',
                           font=('monospace', 14, 'bold'))
        self.E_cvv.place(x=166, y=130)
        # ----------------------------------------------old password -------------------------------------

        l_password = Label(self.new_window, text='Enter the old password', background='#000000',
                           font=('monospace', 14, 'bold'), fg='#d5c468')
        l_password.place(x=150, y=160)
        # -----------------------------------------------entry pass-------------------------------------
        self.old_password = Entry(self.new_window, justify='center', bg='#d5c468', bd=2, width=15, fg='#000000',
                                  font=('monospace', 14, 'bold'))
        self.old_password.place(x=166, y=190)
        # --------------------------------------------- new password -------------------------------------
        l_password = Label(self.new_window, text='Enter the new password', background='#000000',
                           font=('monospace', 14, 'bold'), fg='#d5c468')
        l_password.place(x=150, y=220)
        # -----------------------------------------------entry new pass-------------------------------------
        self.new_password = Entry(self.new_window, bg='#d5c468', justify='center', bd=2, width=15, fg='#000000',
                                  font=('monospace', 14, 'bold'))
        self.new_password.place(x=166, y=250)
        # --------------------------------------btn_change ---------------------------------------------------
        btn_change = Button(self.new_window, background='#d5c468', command=self.process_Change_the_password,
                            text='change', font=('monospace', 24, 'bold'), fg='#000000')
        btn_change.place(x=180, y=300, height=50, width=140)

    def process_Change_the_password(self):
        cvv_number = int(self.E_cvv.get())
        old_password = int(self.old_password.get())
        new_password = self.new_password.get()
        cursor.execute('SELECT password FROM user WHERE cvv = ? ', (cvv_number,))
        result = cursor.fetchone()
        if len(new_password) == 4 and new_password.isdigit():
           if result and result[0] == old_password:
              cursor.execute('UPDATE user SET password = ? WHERE cvv = ? ', (new_password, cvv_number))
              connect.commit()
              messagebox.showinfo("success", "The password has been changed successfully")
              self.new_window.destroy()
           else:
              messagebox.showerror("ERROR", "An error occurred while changing the password")
        else:
            messagebox.showerror("ERROR", "The password must consist of 4 numbers")

    # -------------------------------------Show_information----------------------------------------
    def Show_information(self):
        self.new_window = Toplevel(self.root)
        self.new_window.geometry('500x380+600+120')
        self.new_window.resizable(False, False)
        self.new_window.title('show information')
        self.new_window.configure(background='#000000')
        title = Label(self.new_window, text='Welcome - مرحبا ', font=('monospace', 28, 'bold'), background='#000000',
                      fg='#d5c468')
        title.place(x=130, y=60)
        # ------------------------------------------label cvv------------------------------------------
        l_cvv = Label(self.new_window, text='Enter the cvv', background='#000000', font=('monospace', 14, 'bold'),
                      fg='#d5c468')
        l_cvv.place(x=190, y=130)
        # --------------------------------------------entry cvv-----------------------------------------
        self.E_cvv = Entry(self.new_window, bg='#d5c468', justify='center', bd=2, width=15, fg='#000000',
                           font=('monospace', 14, 'bold'))
        self.E_cvv.place(x=166, y=170)
        # ----------------------------------------------password -------------------------------------

        l_password = Label(self.new_window, text='Enter the password', background='#000000',
                           font=('monospace', 14, 'bold'), fg='#d5c468')
        l_password.place(x=150, y=210)
        # -----------------------------------------------entry pass-------------------------------------
        self.E_password = Entry(self.new_window, bg='#d5c468', justify='center', bd=2, width=15, fg='#000000',
                                font=('monospace', 14, 'bold'), show='*')
        self.E_password.place(x=166, y=250)
        # ----------------------------------------------------btn -----------------------------
        btn_change = Button(self.new_window, background='#d5c468', command=self.process_Show_information, text='Show',
                            font=('monospace', 19, 'bold'), fg='#000000')
        btn_change.place(x=177, y=300, height=50, width=140)
        # ---------------------------------------------process info-----------------------------------------------

    def process_Show_information(self):
        cvv_number = int(self.E_cvv.get())
        password = int(self.E_password.get())
        cursor.execute('SELECT * FROM user WHERE cvv=?', (cvv_number,))
        info = cursor.fetchone()
        if info:
           if info[4] == password:
               messagebox.showinfo("your information",
                                    f'''
                        name : ------{info[1]}---
                        phone : -----{info[2]}---
                        visa_number: {info[3]}
                        password:--- {info[4]}---
                        cvv :------- {info[5]}---
                        exp_date :---{info[6]}---
                        
                        '''
                        )
               self.new_window.destroy()
           else:
               messagebox.showerror("Error", "Error in password.")
               self.new_window.destroy()
        else:
            messagebox.showerror("Error", "Password or CVV is invalid")
            self.new_window.destroy()


# --------------------------------------login--------------------------------------------------
class loginwindow:
    def __init__(self, root):
        self.root = root
        self.root.geometry('400x450+600+120')
        self.root.title('ATM APPLICATION')
        self.root.configure(background='#000000')
        self.root.resizable(False, False)
        title = Label(self.root, text='Welcome - مرحبا ', font=('monospace', 24, 'bold'), background='#000000',
                      fg='#d5c468')
        title.place(x=80, y=50)

        # --------------------------------------lable cvv--------------------------
        l_cvv = Label(self.root, text='Enter the cvv', background='#000000', font=('monospace', 19, 'bold'),
                      fg='#d5c468')
        l_cvv.place(x=110, y=120)
        # ---------------------------------------Entry cvv--------------------------
        self.E_cvv = Entry(self.root, bg='#FFF078', bd=2, width=15, justify="center", fg='#000000',
                           font=('monospace', 14, 'bold'))
        self.E_cvv.place(x=113, y=170)
        # ---------------------------------------lable password------------------------
        l_password = Label(self.root, text='Enter the password', background='#000000', font=('monospace', 14, 'bold'),
                           fg='#d5c468')
        l_password.place(x=110, y=220)
        # -----------------------------------------entry password------------------------
        self.E_password = Entry(self.root, bg='#FFF078', bd=2, width=15, justify="center", fg='#000000',
                                font=('monospace', 14, 'bold'), show='*')
        self.E_password.place(x=113, y=270)

        # -------------------------------------------Button_log----------------------------
        Button_log = Button(self.root, bg='#d5c468', command=self.log, text='login', font=('monospace', 15, 'bold'),
                            justify="center", fg='#000000')
        Button_log.place(x=50, y=350, heigh=50, width=140, )
        # --------------------------------------------Button_craete-------------------------
        Button_craete = Button(self.root, bg='#d5c468', text='Create an account', command=self.create_account,font=('monospace', 12, 'bold'), fg='#000000')
        Button_craete.place(x=200, y=350, height=50, width=147, )


# -----------------------------------------login-----------------------------------------
    def log(self):
        cvv_number_log = self.E_cvv.get()
        password = self.E_password.get()
        cursor.execute("SELECT * FROM user WHERE cvv =? AND password=?", (cvv_number_log, password,))
        user = cursor.fetchone()
        if len(cvv_number_log) == 3 and cvv_number_log.isdigit():
           if len(password) == 4 and password.isdigit():
              if user:
                 self.root.destroy()
                 main_app = Tk()
                 app = ATMAPP(main_app)
                 main_app.mainloop()
              else:
                 messagebox.showerror("Error", "Error in password or CVV")
           else:
                messagebox.showerror("ERROR", "The password must consist of 4 numbers")
        else:
            messagebox.showerror("ERROR", "The cvv must consist of 3 numbers")

    # ------------------------------------------create account-----------------------------------
    def create_account(self):
        self.new_window = Toplevel()
        self.new_window.title("Create Account")
        self.new_window.geometry("400x450+600+120")
        self.new_window.configure(bg="#000000")
        title = Label(self.new_window, text='Welcome - مرحبا ', font=('monospace', 25, 'bold'), background='#000000',
                      fg='#d5c468')
        title.place(x=80, y=50)

        # -------------------------------------------label name-----------------------
        l_name = Label(self.new_window, text='Enter your name', background='#000000', font=('monospace', 14, 'bold'),
                       fg='#d5c468')
        l_name.place(x=115, y=110)
        # ------------------------------------------Entry name-------------------------
        self.E_name = Entry(self.new_window, justify='center', bg='#FFF078', bd=2, width=15, fg='#000000',
                            font=('monospace', 14, 'bold'))
        self.E_name.place(x=115, y=140)
        # -----------------------------------------label phone--------------------------------------------
        l_phone = Label(self.new_window, text='Enter your phone', background='#000000', font=('monospace', 14, 'bold'),
                        fg='#d5c468')
        l_phone.place(x=115, y=170)
        # --------------------------------------------Enter phone-----------------------------------------
        self.E_phone = Entry(self.new_window, bg='#FFF078', bd=2, width=15, fg='#000000', justify='center',font=('monospace', 14, 'bold'))
        self.E_phone.place(x=115, y=200)
        # --------------------------------------------label password---------------------------------------
        l_password = Label(self.new_window, text='Enter your password', background='#000000',font=('monospace', 14, 'bold'), fg='#d5c468')
        l_password.place(x=100, y=230)
        # ----------------------------------------------Enter phone-----------------------------------------
        self.E_password = Entry(self.new_window, bg='#FFF078', bd=2, width=15, justify='center', fg='#000000',font=('monospace', 14, 'bold'))
        self.E_password.place(x=115, y=260)

        btn_sgin = Button(self.new_window, background='#d5c468', command=self.process_create_account, text='sign up',font=('monospace', 17,'bold'), fg='#000000')
        btn_sgin.place(x=130, y=320, height=50, width=140)

    def process_create_account(self):
        name = self.E_name.get()
        phone = self.E_phone.get()
        password = self.E_password.get()
        if len(phone) == 11 and phone.isdigit():
            if len(password) == 4 and password.isdigit():
                while True:
                    visa_number = random.randint(10 ** 15, 10 ** 16 - 1)
                    if str(visa_number).startswith('507803'):
                        break

                try:
                    cvv = random.randint(100, 999)
                    cursor.execute(
                        f'''
                              INSERT INTO user(name,phone_number,visa_number,password,cvv,exp_date,money)VALUES(?,?,?,?,?,?,?)
                      ''', (name, phone, visa_number, password,cvv,
                            (datetime.today() - timedelta(days=365 * 5.)).strftime('%m/%y'), 0)
                    )
                    connect.commit()
                    messagebox.showinfo("success", f"Your account has been added successfully and this is your CVV: {cvv}")
                    connect.commit()

                except sqlite3.IntegrityError:
                    messagebox.showerror("Error", "This information exists")
            else:
                messagebox.showerror("ERROR", "The password must consist of 4 numbers")
        else:
            messagebox.showerror("ERROR", "The phone number must consist of 11 digits")

root = Tk()
login_APP = loginwindow(root)
root.mainloop()

connect.commit()
cursor.close()
connect.close()
