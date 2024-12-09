import tkinter.messagebox as messagebox
import customtkinter as ctk
import pandas as pd

def add_book():
    
    input_window = ctk.CTkToplevel()
    input_window.title("Add Book")
    input_window.geometry("400x600")  
    book_id_var = ctk.StringVar()
    book_title_var = ctk.StringVar()
    book_author_var = ctk.StringVar()
    book_genre_var = ctk.StringVar()

    def submit_inputs():
        try:
            book_id = book_id_var.get().strip().title()
            book_title = book_title_var.get().strip().title()
            book_author = book_author_var.get().strip().title()
            book_genre = book_genre_var.get().strip().title()
            
            if not all([book_id, book_title, book_author, book_genre]):
                messagebox.showerror("Input Error", "All fields must be filled!")
                return
            
            books_df = pd.read_csv("books.csv")
            if book_id in books_df["Book_ID"].astype(str).values:
                messagebox.showerror("Duplicate ID", f"Book ID '{book_id}' already exists!")
                return
      
            new_row = {
                "Book_ID": book_id,
                "Title": book_title,
                "Author": book_author,
                "Genre": book_genre,
                "Year_Published": "Unknown", 
                "Pages": "Unknown",
                "ISBN": "Unknown",
                "Language": "Unknown",
                "Rating": "Unknown",
                "Available": "Yes"
            }
            books_df = pd.concat([books_df, pd.DataFrame([new_row])], ignore_index=True)
            books_df.to_csv("books.csv", index=False)
            
            messagebox.showinfo("Success", f"Book '{book_title}' added successfully!")
            input_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # GUI Elements
    ctk.CTkLabel(input_window, text="Book ID:", font=("Arial", 14)).pack(pady=5)
    ctk.CTkEntry(input_window, textvariable=book_id_var).pack(pady=5)

    ctk.CTkLabel(input_window, text="Book Title:", font=("Arial", 14)).pack(pady=5)
    ctk.CTkEntry(input_window, textvariable=book_title_var).pack(pady=5)

    ctk.CTkLabel(input_window, text="Author:", font=("Arial", 14)).pack(pady=5)
    ctk.CTkEntry(input_window, textvariable=book_author_var).pack(pady=5)

    ctk.CTkLabel(input_window, text="Genre:", font=("Arial", 14)).pack(pady=5)
    ctk.CTkEntry(input_window, textvariable=book_genre_var).pack(pady=5)

    ctk.CTkButton(input_window, text="Submit", command=submit_inputs).pack(pady=20)


def edit_book():
    book_title = input("Enter the title of the book to edit: ")
    books = read_books()
    for book in books:
        if book["title"] == book_title:
            new_title = input("Enter the new title: ")
            new_author = input("Enter the new author: ")
            book["title"], book["author"] = new_title, new_author
            write_books(books)
            messagebox.showinfo("Edit Book", f"Book updated to '{new_title}' by {new_author}.")
            return
    messagebox.showwarning("Edit Book", "Book not found!")
    
def delete_book():
    input_window = ctk.CTkToplevel()
    input_window.title("Delete Book")
    input_window.geometry("400x200")  
    book_title_var = ctk.StringVar()  # Corrected to use book_title_var

    def submit_inputs():
        try:
            book_title = book_title_var.get().strip().title()  # Corrected to use book_title_var
            
            if not book_title:
                messagebox.showerror("Input Error", "Book title must be provided!")
                return
            
            books_df = pd.read_csv("books.csv")
            
            if book_title not in books_df["Title"].astype(str).values:
                messagebox.showerror("Not Found", f"Book '{book_title}' not found!")
                return
            
            books_df = books_df[books_df["Title"].astype(str) != book_title]
            
            books_df.to_csv("books.csv", index=False)
            
            messagebox.showinfo("Success", f"Book '{book_title}' deleted successfully!")
            input_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # GUI Elements
    ctk.CTkLabel(input_window, text="Enter Book Title to Delete:", font=("Arial", 14)).pack(pady=5)
    ctk.CTkEntry(input_window, textvariable=book_title_var).pack(pady=5)  # Corrected to use book_title_var

    ctk.CTkButton(input_window, text="Delete", command=submit_inputs).pack(pady=20)

    
   
def issue_book():
   return
    
def return_book():
    return
    

def calculate_fine():
    days_late = int(input("Enter the number of days the book is late: "))
    fine_per_day = 5  
    total_fine = days_late * fine_per_day
    messagebox.showinfo("Calculate Fine", f"Total fine is ${total_fine}.")
    
def add_user():
    input_window = ctk.CTkToplevel()
    input_window.title("Add User")
    input_window.geometry("400x400")

    user_id_var = ctk.StringVar()
    username_var = ctk.StringVar()
    email_var = ctk.StringVar()
    password_var = ctk.StringVar()
    role_var = ctk.StringVar()

    def submit_inputs():
        try:
            user_id = user_id_var.get().strip()
            username = username_var.get().strip()
            email = email_var.get().strip().lower()
            password = password_var.get().strip()
            role = role_var.get().strip().lower()

            if not all([user_id, username, email, password, role]):
                messagebox.showerror("Input Error", "All fields must be filled!")
                return

            users_df = pd.read_csv("users.csv")
            if user_id in users_df["user_id"].astype(str).values:
                messagebox.showerror("Duplicate ID", f"User ID '{user_id}' already exists!")
                return
            if username in users_df["username"].astype(str).values:
                messagebox.showerror("Duplicate Username", f"Username '{username}' already exists!")
                return
            
            new_row = {
                "user_id": user_id,
                "username": username,
                "email": email,
                "password": password,
                "role": role
            }
            users_df = pd.concat([users_df, pd.DataFrame([new_row])], ignore_index=True)
            users_df.to_csv("users.csv", index=False)

            # Success message
            messagebox.showinfo("Success", f"User '{username}' added successfully!")
            input_window.destroy()
        except FileNotFoundError:
            messagebox.showerror("File Error", "The file 'users.csv' was not found!")
        except pd.errors.EmptyDataError:
            messagebox.showerror("File Error", "The file 'users.csv' is empty!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # GUI Elements
    ctk.CTkLabel(input_window, text="User ID:", font=("Arial", 14)).pack(pady=5)
    ctk.CTkEntry(input_window, textvariable=user_id_var).pack(pady=5)

    ctk.CTkLabel(input_window, text="Username:", font=("Arial", 14)).pack(pady=5)
    ctk.CTkEntry(input_window, textvariable=username_var).pack(pady=5)

    ctk.CTkLabel(input_window, text="Email:", font=("Arial", 14)).pack(pady=5)
    ctk.CTkEntry(input_window, textvariable=email_var).pack(pady=5)

    ctk.CTkLabel(input_window, text="Password:", font=("Arial", 14)).pack(pady=5)
    ctk.CTkEntry(input_window, textvariable=password_var).pack(pady=5)

    ctk.CTkLabel(input_window, text="Role:", font=("Arial", 14)).pack(pady=5)
    ctk.CTkEntry(input_window, textvariable=role_var).pack(pady=5)

    ctk.CTkButton(input_window, text="Add User", command=submit_inputs).pack(pady=20)



    
def delete_user():
    input_window = ctk.CTkToplevel()
    input_window.title("Delete User")
    input_window.geometry("400x250")
    
    user_id_var = ctk.StringVar()
    username_var = ctk.StringVar()

    def submit_inputs():
        try:
            user_id = user_id_var.get().strip()
            username = username_var.get().strip()
            if not user_id and not username:
                messagebox.showerror("Input Error", "Either User ID or Username must be provided!")
                return
            
            users_df = pd.read_csv("users.csv")
            users_df["user_id"] = users_df["user_id"].astype(str).str.strip()
            users_df["username"] = users_df["username"].astype(str).str.strip()

      
            if user_id and user_id in users_df["user_id"].values:
                users_df = users_df[users_df["user_id"] != user_id]
            elif username and username in users_df["username"].values:
                users_df = users_df[users_df["username"] != username]
            else:
                messagebox.showerror("Not Found", f"No user with ID '{user_id}' or Username '{username}' found!")
                return

            users_df.to_csv("users.csv", index=False)
            messagebox.showinfo("Success", f"User with ID '{user_id}' or Username '{username}' deleted successfully!")
            input_window.destroy()

        except FileNotFoundError:
            messagebox.showerror("File Error", "The file 'users.csv' was not found!")
        except pd.errors.EmptyDataError:
            messagebox.showerror("File Error", "The file 'users.csv' is empty!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    ctk.CTkLabel(input_window, text="User ID (optional):", font=("Arial", 14)).pack(pady=5)
    ctk.CTkEntry(input_window, textvariable=user_id_var).pack(pady=5)

    ctk.CTkLabel(input_window, text="Username (optional):", font=("Arial", 14)).pack(pady=5)
    ctk.CTkEntry(input_window, textvariable=username_var).pack(pady=5)

    ctk.CTkButton(input_window, text="Delete User", command=submit_inputs).pack(pady=20)
