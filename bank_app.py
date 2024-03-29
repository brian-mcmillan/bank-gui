import sqlite3
from tkinter import *
from datetime import datetime

# |-------------------------------------------------------------------------------------| #
# |  This program replicates a bank account application.                                | #
# |  It allows a user to create an account and login.                                   | #
# |  Upon login, the user can view credentials, balance, and account history.           | #
# |  The user can also update the balance by either withdrawing or depositing.          | #
# |  This is accomplished using a SQL database, to store user credentials.              | #
# |  The application visuals are displayed to the user through the use of tkinter GUI.  | #
# |-------------------------------------------------------------------------------------| #


# connect to database: account_info
con = sqlite3.connect("account_info.db")

cur = con.cursor()

# creates all_accounts table if it does not already exist.
# username is denoted as the PRIMARY KEY
cur.execute('''CREATE TABLE IF NOT EXISTS all_accounts(username text PRIMARY KEY, name text, password text, 
            balance real, gender text, age real)''')

# sample insertion of user data
# cur.execute('''INSERT OR IGNORE INTO all_accounts VALUES
           # ('brianmickey', 'Brian McMillan', 'coding', '10000', 'Male', '2000')''')

# creates all_withdrawals and all_deposits if they do not already exist.
cur.execute("""CREATE TABLE IF NOT EXISTS withdrawals(username text, withdrawn text, time text)""")
cur.execute("""CREATE TABLE IF NOT EXISTS deposits(username text, deposits text, time text)""")

con.commit()


# Main Menu
main_menu = Tk()
main_menu.title("Online Banking")


def view_withdrawal():
    """Displays all previous withdrawals to user. Includes amount and time of transaction."""

    withdrawal_view = Toplevel(main_menu)

    # for each iteration through db-withdrawals, append amount,time.
    str1 = ""
    for row in cur.execute(f"SELECT * FROM withdrawals where username = '{temp_username2}'"):
        str1 += "\n" + "$" + row[1] + "\t" + "|" + "\t" + row[2] + '\n' + "____________________________________________________"

    # Labels
    Label(withdrawal_view, text="Withdrawals", font="time 15").grid(row=1, sticky=N)
    Label(withdrawal_view, text="AMOUNT", font="time 12").grid(row=2, stick=W)
    Label(withdrawal_view, text="TIME", font="time 12").grid(row=2, stick=E)
    Label(withdrawal_view, text=str1, font="times 10").grid(row=3, sticky=W)


def view_deposit():
    """Displays all previous deposits to user. Includes amount and time of transaction."""

    deposit_view = Toplevel(main_menu)

    # for each iteration through db-deposits, append amount,time.
    str1 = ""
    for row in cur.execute(f"SELECT * FROM deposits where username = '{temp_username2}'"):
        str1 += "\n" + "$" + row[1] + "\t" + "|" + "\t" + row[2] + '\n' + "____________________________________________________"

    # Labels
    Label(deposit_view, text="Deposits", font="time 15").grid(row=1, sticky=N)
    Label(deposit_view, text="AMOUNT", font="time 12").grid(row=2, stick=W)
    Label(deposit_view, text="TIME", font="time 12").grid(row=2, stick=E)
    Label(deposit_view, text=str1, font="times 10").grid(row=3, sticky=W)


def view_transactions():
    """Parent menu to view_deposit and view_withdrawals. Displays view deposit and view withdrawal buttons."""
    transaction_menu = Toplevel(main_menu)

    Label(transaction_menu, text="Which transactions would you like to view?", font="time 12").grid(row=1, sticky=N)

    Button(transaction_menu, text="Deposits", command=view_deposit, font="Times 12 bold").grid(row=5, sticky=SE)
    Button(transaction_menu, text="Withdrawals", command=view_withdrawal, font="Times 12 bold").grid(row=5, sticky=SW)


def update_deposit():
    """Updates deposits table and all_accounts table with the proper information upon a user submitted deposit."""

    global user_info, deposit_menu

    temp_deposit = deposit_amount.get()
    deposit_time = datetime.now()

    # format time to day-month-year at hour:minutes
    deposit_time = deposit_time.strftime("%d-%m-%Y @ %H:%M")

    cur.execute(f"SELECT balance FROM all_accounts WHERE username = '{temp_username2}'")
    balance_check = cur.fetchone()

    cur.execute(f'''INSERT OR IGNORE INTO deposits VALUES('{temp_username2}','{temp_deposit}','{deposit_time}') ''')
    con.commit()

    cur.execute(f'''SELECT deposits FROM deposits WHERE username = '{temp_username2}' ''')
    deposit_check = cur.fetchone()

    # Add deposit amount to user balance in all_accounts
    updated_balance = balance_check[0] + temp_deposit
    #print(updated_balance)

    # Set the balance for the corresponding username as the updated_balance
    cur.execute(f'''UPDATE all_accounts 
                    SET balance = '{updated_balance}'
                    WHERE username = '{temp_username2}' ''')
    con.commit()

    format_balance = "{:,.2f}".format(updated_balance)
    updated_balance = format_balance

    # Label
    Label(user_info, text=f"Balance: ${updated_balance}", font="times 15").grid(row=3, sticky=W, pady=4, padx=5)


def update_withdraw():
    """Updated withdrawals table and all_accounts table with the proper information upon a user submitted withdrawal."""

    global user_info

    temp_withdraw = withdraw_amount.get()

    deposit_time = datetime.now()
    deposit_time = deposit_time.strftime("%d-%m-%Y @ %H:%M")

    cur.execute(f"SELECT balance FROM all_accounts WHERE username = '{temp_username2}'")
    balance_check = cur.fetchone()

    cur.execute(f'''INSERT OR IGNORE INTO withdrawals VALUES('{temp_username2}','{temp_withdraw}','{deposit_time}') ''')
    con.commit()

    cur.execute(f'''SELECT withdrawn FROM withdrawals WHERE username = '{temp_username2}' ''')
    deposit_check = cur.fetchone()

    # Subtract withdrawal amount from user balance in all_accounts
    updated_balance = balance_check[0] - temp_withdraw
    #print(updated_balance)

    # Set the balance for the corresponding username as the updated_balance
    cur.execute(f'''UPDATE all_accounts
                    SET balance = '{updated_balance}'
                    WHERE username = '{temp_username2}' ''')
    con.commit()

    format_balance = "{:,.2f}".format(updated_balance)
    updated_balance = format_balance

    # Label
    Label(user_info, text=f"Balance: ${updated_balance}", font="times 15").grid(row=3, sticky=W, pady=4, padx=5)


def withdraw():
    """Displays the withdrawal menu and allows user to enter and confirm a prospective withdrawal."""

    global withdraw_amount

    withdraw_amount = IntVar()
    withdraw_menu = Toplevel(main_menu)

    # Labels
    Label(withdraw_menu, text="Withdraw Funds", font="times 16").grid(row=1, stick=N, pady=0, padx=10)
    Label(withdraw_menu, text="How much would you like to withdraw?", font='times 12').grid(row=2, stick=N, pady=5)
    Label(withdraw_menu, text="$", font='times 12').grid(row=3, stick=W)

    # Entry
    Entry(withdraw_menu, textvariable=withdraw_amount).grid(row=3, column=0, sticky=N)

    # Button
    Button(withdraw_menu, text="Confirm", command=update_withdraw, font="Times 12 bold").grid(row=5, sticky=SE)


def deposit():
    """Displays the deposit menu and allows user to enter and confirm a prospective deposit."""

    global deposit_amount

    deposit_amount = IntVar()
    deposit_menu = Toplevel(main_menu)

    # Labels
    Label(deposit_menu, text="Deposit Funds", font="times 16").grid(row=1, stick=N, pady=0, padx=10)
    Label(deposit_menu, text="How much would you like to deposit?", font='times 12').grid(row=2, stick=N, pady=5)
    Label(deposit_menu, text="$").grid(row=3, column=0, sticky=W)

    # Entry
    Entry(deposit_menu, textvariable=deposit_amount).grid(row=3, column=0, sticky=N)

    # Button
    Button(deposit_menu, text="Confirm", command=update_deposit, font="Times 12 bold").grid(row=5, sticky=SE)



def user_account():
    """Allows user to view relevant account information upon successful login."""

    global balancecheck, display_bal, user_info

    user_info = Toplevel(main_menu)

    # Label
    Label(user_info, text="Account Information", font="times 16").grid(row=1, stick=N, pady=0, padx=10)

    # display name to user
    cur.execute(f"SELECT name FROM all_accounts WHERE username = '{temp_username2}'")
    namecheck = cur.fetchone()
    if namecheck:
        Label(user_info, text=f"Name: {namecheck[0]}", font="times 14").grid(row=2, sticky=W, pady=4, padx=5)
    else:
        print("error.")

    # display balance to user
    cur.execute(f"SELECT balance FROM all_accounts WHERE username = '{temp_username2}'")
    balancecheck = cur.fetchone()
    if balancecheck:
        display_bal = Label(user_info, text=f"Balance: ${balancecheck[0]}", font="times 14").grid(row=3, sticky=W, pady=4, padx=5)
    else:
        print("error.")

    # Buttons
    # Withdraw
    Button(user_info, text="Withdraw", command=withdraw, font="Times 9 bold").grid(row=5, sticky=SW)
    # Deposit
    Button(user_info, text="Deposit", command=deposit, font="Times 9 bold").grid(row=5, sticky=N)
    # view transactions
    Button(user_info, text="History", command=view_transactions, font = "Times 9 bold").grid(row=5, stick=SE)


def finish_login():
    """Retrieves login information from login() and checks if login is successful or not."""

    global temp_username2

    temp_username2 = user_name2.get()
    temp_password2 = password2.get()

    # Checks if a username and password combo exists
    check2 = f"SELECT username from all_accounts WHERE password='{temp_password2}' and username='{temp_username2}'"
    cur.execute(check2)

    # If it does, notify the user they have logged in successfully and bring them to the account info page
    if cur.fetchall():
        notif.config(fg="green", text="Login Successful")
        user_account()
    else:
        # If it does not, notify the user they have entered something wrong
        notif.config(fg="red", text="Wrong Username or Password")



def finish_reg():
    """Retrieves user information from register() and checks if registration fields have been filled out correctly."""

    global temp_name

    temp_name = user_name.get()
    temp_username = user_username.get()
    temp_password = user_password.get()
    temp_age = user_age.get()
    temp_gender = user_gender.get()

    # checks if any fields are left blank and notifies the user
    if temp_name == "" or temp_username == "" or temp_password == "" or temp_age == "" or temp_gender == "":
        notif.config(fg="red", text="Fields required", font="times")

    # checks if the entered username already exists
    check = f"SELECT username from all_accounts WHERE username='{temp_username}'"
    cur.execute(check)

    # if it does, the user is notified
    if cur.fetchone():
        notif.config(fg="red", text="Username is taken")
    else:
        # if it does not, the user is notified that their account has been successfully created
        notif.config(fg="green", text="Account Created")

        # user info is inserted into database
        cur.execute(f'''INSERT OR IGNORE INTO all_accounts VALUES
        ('{temp_username}', '{temp_name}', '{temp_password}', '0', '{temp_gender}', '{temp_age}')''')

        con.commit()


def register():
    """Allows a user to submit account information."""

    global user_name, user_username, user_password
    global user_age, user_gender, notif

    user_name = StringVar()
    user_username = StringVar()
    user_password = StringVar()
    user_age = StringVar()
    user_gender = StringVar()

    # Registration Menu
    register_menu = Toplevel(main_menu)
    register_menu.title("Register")

    # Labels
    Label(register_menu, text="Create your new account", font="times 16").grid(row=0, sticky=NW, pady=10, padx=30)
    Label(register_menu, text="Name", font="times 12 ").grid(row=2, sticky=W, padx=20)
    Label(register_menu, text="Username", font="times 12").grid(row=3, sticky=W, padx=20)
    Label(register_menu, text="Password", font="times 12 ").grid(row=4, sticky=W, padx=20)
    Label(register_menu, text="Age", font="times 12").grid(row=5, sticky=W, padx=20)
    Label(register_menu, text="Gender", font="times 12").grid(row=6, sticky=W, padx=20)
    notif = Label(register_menu, font="times 12")
    notif.grid(row=9, sticky=N, pady=10)

    # Entries
    Entry(register_menu, textvariable=user_name).grid(row=2, column=0, sticky=E)
    Entry(register_menu, textvariable=user_username).grid(row=3, column=0, sticky=E)
    Entry(register_menu, textvariable=user_password, show="*").grid(row=4, column=0, sticky=E)
    Entry(register_menu, textvariable=user_age).grid(row=5, column=0, sticky=E)
    Entry(register_menu, textvariable=user_gender).grid(row=6, column=0, sticky=E)

    # Buttons
    Button(register_menu, text="Register", command=finish_reg, font="Times 12").grid(row=8, sticky=N)


def login():
    """Allows a user to submit login information."""

    global user_name2, password2, notif, login_menu, login_button

    user_name2 = StringVar()
    password2 = StringVar()

    # Login Menu
    login_menu = Toplevel(main_menu)
    login_menu.title("Login")

    # Labels
    Label(login_menu, text="Login to your account", font="Times 16").grid(row=1, sticky=NW, pady=10, padx=30)
    Label(login_menu, text="Username", font="times 12").grid(row=3, sticky=W)
    Label(login_menu, text="Password", font="times 12").grid(row=4, sticky=W)
    notif = Label(login_menu, font="times 12")
    notif.grid(row=9, sticky=N, pady=10)

    # Entries
    Entry(login_menu, textvariable=user_name2, font="Times 12").grid(row=3, column=0, sticky=E)
    Entry(login_menu, textvariable=password2, show="*", font="Times 12").grid(row=4, column=0, sticky=E)

    # Button
    login_button = Button(login_menu, text="Login", command=finish_login, font="Times 12 ").grid(row=8, sticky=NS)



# Main Menu Buttons
create_account_button = Button(main_menu, text="Create Account", font=("Times 15"), activeforeground="royal blue",
                               width=20, command=register).grid(row=1, sticky=N, pady=10)
login_button = Button(main_menu, text="Login", font=("Times 15 "), command=login, width=20).grid(row=2, sticky=N,
                                                                                                 pady=10)


main_menu.mainloop()
con.close()


# Screen widths for formatting GUI
# print(main_menu.winfo_screenwidth())
# print(main_menu.winfo_screenwidth())
