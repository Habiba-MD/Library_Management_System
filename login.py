import customtkinter as ctk
import tkinter as tk
import tkinter.messagebox as tkmb
import pandas as pd
from PIL import Image
from user import create_user_window  
from employee import create_employee_window  
from manager import create_admin_window

# Theme, color, and app window
ctk.set_appearance_mode('light')
ctk.set_default_color_theme('blue')
app = ctk.CTk()
app.geometry('500x500')
app.title('Login')

# Login function
def login():
    try:
        users_data = pd.read_csv('users.csv')
    except FileNotFoundError:
        tkmb.showerror(title="File Not Found", message="The user data file 'users.csv' does not exist.")
        return

    usernames = users_data.get('username', [])
    emails = users_data.get('email', [])
    passwords = users_data.get('password', [])
    roles = users_data.get('role', [])

    username_input = user_entry.get()
    email_input = user_email.get()
    password_input = user_pass.get()

    if username_input in usernames.values:
        row_index = usernames[usernames == username_input].index[0]
        if passwords[row_index] == password_input and emails[row_index] == email_input:
            tkmb.showinfo(title="Login Successful", message="You have logged in successfully")
            role = roles[row_index]
            if role == 'user':
                create_user_window(username_input)
                app.destroy()
            elif role == 'employee':
                create_employee_window(username_input)
                app.destroy()
            elif role == 'admin':
                create_admin_window(username_input)
                app.destroy
        else:
            tkmb.showwarning(title='Invalid Credentials', message='Please check your email or password.')
    else:
        tkmb.showerror(title="Login Failed", message="Invalid Username.")
        
# User registration
def register():
    username_input = user_entry.get()
    password_input = user_pass.get()
    email_input = user_email.get()  
    
    if username_input and password_input and email_input:
        try:
            users_data = pd.read_csv('users.csv')
        except FileNotFoundError:
            users_data = pd.DataFrame(columns=['username', 'email', 'password', 'role'])

        if username_input in users_data['username'].values:
            tkmb.showwarning(title="Username Taken", message="The username is already taken. Please choose a different one.")
            return
 
        new_user = pd.DataFrame({'username': [username_input], 'email': [email_input], 'password': [password_input], 'role': 'user'})
        users_data = pd.concat([users_data, new_user], ignore_index=True)
        users_data.to_csv('users.csv', index=False)

        tkmb.showinfo(title="Registration Successful", message="You have registered successfully.")
        
        user_entry.delete(0, tk.END)
        user_email.delete(0, tk.END)
        user_pass.delete(0, tk.END)
    else:
        tkmb.showwarning(title="Input Error", message="Please fill in all fields.")

# Main UI components
label = ctk.CTkLabel(app, text="Welcome there, Please enter you username and password to access the library system")
label.pack(pady=20)

frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=40, fill='both', expand=True)

label = ctk.CTkLabel(master=frame, text='Login')
label.pack(pady=12, padx=10)

user_entry = ctk.CTkEntry(master=frame, placeholder_text="Username")
user_entry.pack(pady=12, padx=10)

user_email = ctk.CTkEntry(master=frame, placeholder_text="email")
user_email.pack(pady=12, padx=10)

user_pass = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*")
user_pass.pack(pady=12, padx=10)

button_login = ctk.CTkButton(master=frame, text='Login', command=login)
button_login.pack(pady=12, padx=10)

button_register = ctk.CTkButton(master=frame, text='Register', command=register)
button_register.pack(pady=12, padx=10)

checkbox = ctk.CTkCheckBox(master=frame, text='Remember Me')
checkbox.pack(pady=12, padx=10)

app.mainloop()
