from tkinter import *
import os

# Helper function to destroy all widgets in a parent widget
def destroyPackWidget(parent):
    for e in parent.pack_slaves():
        e.destroy()

# Function to handle registration
def register():
    global root, register_screen, username, password, username_entry, password_entry
    destroyPackWidget(root)
    
    register_screen = Toplevel(root)
    register_screen.title("Register")
    register_screen.geometry("300x250")

    username = StringVar()
    password = StringVar()

    Label(register_screen, text="Please enter the details below", bg="blue").pack()
    Label(register_screen, text="").pack()
    Label(register_screen, text="Username").pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    Label(register_screen, text="Password").pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    Label(register_screen, text="").pack()
    Button(register_screen, text="Register", width=10, height=1, bg="blue", command=register_user).pack()

# Function to handle login
def login():
    global login_screen, username_verify, password_verify, username_login_entry, password_login_entry
    login_screen = Toplevel(root)
    login_screen.title("Login")
    login_screen.geometry("300x250")

    username_verify = StringVar()
    password_verify = StringVar()

    Label(login_screen, text="Please enter details below to login").pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Username * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show='*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1, command=login_verify).pack()

# Function to handle user registration
def register_user():
    username_info = username.get()
    password_info = password.get()

    if username_info and password_info:
        with open(username_info, "w") as file:
            file.write(username_info + "\n")
            file.write(password_info)

        username_entry.delete(0, END)
        password_entry.delete(0, END)

        Label(register_screen, text="Registration is successful", fg="green", font=("calibri", 14)).pack()
        Button(register_screen, text="Click Here to proceed", command=destroyPackWidget(register_screen)).pack()

# Function to verify login credentials
def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()

    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

    if os.path.isfile(username1):
        with open(username1, "r") as file:
            verify = file.read().splitlines()
            if password1 == verify[1]:  # Check if the entered password matches the stored one
                login_success()
            else:
                password_not_recognised()
    else:
        user_not_found()

# Function to handle successful login
def login_success():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("150x100")
    Label(login_success_screen, text="Login Success").pack()
    Button(login_success_screen, text="OK", command=delete_login_success).pack()

# Function to handle incorrect password
def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Error")
    password_not_recog_screen.geometry("150x100")
    Label(password_not_recog_screen, text="Invalid Password").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()

# Function to handle user not found
def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Error")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text="User Not Found").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()

# Helper functions to close popup windows
def delete_login_success():
    login_success_screen.destroy()

def delete_password_not_recognised():
    password_not_recog_screen.destroy()

def delete_user_not_found_screen():
    user_not_found_screen.destroy()

# Function to design the main window
def main_account_screen():
    global root
    root.geometry("300x250")
    root.title("Account Login")
    Label(root, text="HealthBot", bg="yellow", width="300", height="2", font=("Calibri", 14)).pack()
    Label(root, text="").pack()
    Button(root, text="Login", bg="light green", height="2", width="30", command=login).pack()
    Label(root, text="").pack()
    Button(root, text="Register", bg="light green", height="2", width="30", command=register).pack()

root = Tk()
main_account_screen()
root.mainloop()
