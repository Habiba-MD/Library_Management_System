import customtkinter as ctk

def create_user_window(username):
    user_window = ctk.CTk()
    user_window.geometry('1000x700')
    user_window.title("User Window")
    
    # Display a personalized welcome message using the passed username
    welcome_message = f"Welcome to the Library System, {username}!"
    ctk.CTkLabel(user_window, text=welcome_message).pack(pady=20)

   
    user_window.mainloop()
