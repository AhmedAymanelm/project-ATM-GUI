import sqlite3
import random
from datetime import timedelta, datetime
connect = sqlite3.connect('Atm.db')
cursor = connect.cursor()
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS user(
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
def Withdraw():
    card_number = int(input("Please enter the card number: "))
    password = int(input("Please enter password: "))
    cursor.execute("SELECT money from user WHERE visa_number=? AND password=?",(card_number,password,))
    money= cursor.fetchone()
    if money:
        amount = int(input("Please enter the value: "))
        if amount <= money[0]:
            new_money=money[0]-amount
            cursor.execute('UPDATE user SET money = ? WHERE visa_number=?',(new_money,card_number,))
            print("The withdrawal process was completed successfully")
        else:
            print("Your balance is insufficient")
    else:
        print("Error in password or visa")

def Deposit():
    card_number = int(input("Please enter the card number: "))
    password = int(input("Please enter password: "))
    cursor.execute("SELECT money from user WHERE visa_number=? AND password=?",(card_number,password,))
    money = cursor.fetchone()
    if money:
        amount = int(input("Please enter the value: "))
        new_money = money[0] + amount
        cursor.execute('UPDATE user SET money = ? WHERE visa_number=?', (new_money, card_number,))
        print("The deposit was completed successfully")
    else:
        print("Error in password or visa")

def Show_the_money():
    card_number = int(input("Please enter the card number: "))
    password = int(input("Please enter password: "))
    cursor.execute("SELECT money from user WHERE visa_number=? AND password=?",(card_number,password,))

    money = cursor.fetchone()
    if money:
        print(
            f'''
            
            ------YOUR MONEY----
            |  money: {money[0]}  |
             -------------------

        '''
        )
    else:
        print("Error in password or visa")

def Change_the_password():
    password1 = int(input("Please enter password: "))
    card_number = input("Please enter your visa number: ")
    cursor.execute('SELECT password FROM user WHERE visa_number = ?', (card_number,))
    result = cursor.fetchone()
    if result and result[0] == password1:
       new_password = int(input("Please enter your new password: "))
       cursor.execute('UPDATE user SET password = ? WHERE visa_number = ?', (new_password, card_number))
       print("Password updated successfully!")
    else:
      print("Error in password or visa")


def Show_information():
    card_number = int(input("Please enter the card number: "))
    password = int(input("Please enter password: "))
    cursor.execute('SELECT * FROM user WHERE visa_number = ?', (card_number,))
    info = cursor.fetchone()
    if info:
       if info[4] == password:
          print(
            f'''
             ------YOUR info-------
            |  NAME : {info[1]}    
            |  PHONE: {info[2]}    
            |  visa_number: {info[3]}
            |  password: {info[4]}   
            |  cvv: {info[5]}        
            |  exp_date: {info[6]}   
            |   money: {info[7]}     
             -----------------------
            '''
          )
       else:
           print("Error in password.")
    else:
        print("An error occurred. You do not have an account")

def craet_acount():
    print("----------------------Hello sir, we are happy that you will be our client------------------------")
    name = input("Please enter your name: ")
    phone_number = int(input("Please enter phone number: "))
    password = int(input("Please enter password: "))
    while True:
        visa_number = random.randint(10 ** 15, 10 ** 16 - 1)
        if str(visa_number).startswith('507803'):
            break
    try:
        cursor.execute(f'''
                         INSERT INTO user (name,phone_number,visa_number,password,cvv,exp_date,money) VALUES(?,?,?,?,?,?,?)
                        ''',(name,phone_number,visa_number,password,random.randint(100,999),(datetime.today()+timedelta(days=365*5)).strftime("%m/%y"),0)
                       )
        print("Your account has been opened successfully")
    except:
        print("This information exists")
        exit()
your = input("do you have an account ?(Y/N)").lower().strip()
if your == 'y':
    print(
        '''
        Choose the service you want
        [1] Withdraw
        [2] Deposit
        [3] Show the money
        [4] Change the password
        [5] Show information
        '''
    )
    proccess = int(input("Please enter the service number : "))
    if proccess == 1:
        Withdraw()
    elif proccess == 2:
        Deposit()
    elif proccess == 3:
        Show_the_money()
    elif proccess == 4:
        Change_the_password()
    elif proccess == 5:
        Show_information()
    else:
        print("opps,Wrong choice")

elif your == 'n':
    craet = input("Do you want to create a new account? (Y/N)")
    if craet == 'y':
        craet_acount()

    else:
        print("Thank you bye")
else:
    print("opps,Wrong choice")

connect.commit()
cursor.close()
connect.close()
