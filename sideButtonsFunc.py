import tkinter.messagebox as messagebox
import customtkinter as ctk
import pandas as pd
from datetime import datetime, timedelta

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
    input_window = ctk.CTkToplevel()
    input_window.title("Edit Book")
    input_window.geometry("400x300")  

    book_title_var = ctk.StringVar()
    new_book_title_var = ctk.StringVar()
    new_genre_var = ctk.StringVar()
    
    def submit_edit():
        try:
            book_title = book_title_var.get().strip().title()
            new_book_title = new_book_title_var.get().strip().title()
            new_genre = new_genre_var.get().strip().title()

            if not book_title or not new_book_title or not new_genre:
                messagebox.showerror("Input Error", "All fields must be filled out!")
                return
            
            books_df = pd.read_csv("books.csv")

            book_row = books_df[books_df["Title"].astype(str) == book_title]
            if book_row.empty:
                messagebox.showerror("Not Found", f"Book '{book_title}' not found!")
                return

            books_df.loc[books_df["Title"].astype(str) == book_title, "Title"] = new_book_title
            books_df.loc[books_df["Title"].astype(str) == new_book_title, "Genre"] = new_genre

            next_book_id = books_df["book_id"].max() + 1 if not books_df.empty else 1
            books_df.loc[books_df["Title"].astype(str) == new_book_title, "book_id"] = next_book_id

            books_df.to_csv("books.csv", index=False)

            messagebox.showinfo("Success", f"Book '{new_book_title}' details updated successfully!")
            input_window.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # GUI Elements
    ctk.CTkLabel(input_window, text="Enter Book Title to Edit:", font=("Arial", 14)).pack(pady=5)
    ctk.CTkEntry(input_window, textvariable=book_title_var).pack(pady=5)

    ctk.CTkLabel(input_window, text="Enter New Book Auther:", font=("Arial", 14)).pack(pady=5)
    ctk.CTkEntry(input_window, textvariable=new_book_title_var).pack(pady=5)

    ctk.CTkLabel(input_window, text="Enter New Genre:", font=("Arial", 14)).pack(pady=5)
    ctk.CTkEntry(input_window, textvariable=new_genre_var).pack(pady=5)

    ctk.CTkButton(input_window, text="Submit Changes", command=submit_edit).pack(pady=20)

    
def delete_book():
    input_window = ctk.CTkToplevel()
    input_window.title("Delete Book")
    input_window.geometry("400x200")  
    book_title_var = ctk.StringVar()  

    def submit_inputs():
        try:
            book_title = book_title_var.get().strip().title()  
            
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
    ctk.CTkEntry(input_window, textvariable=book_title_var).pack(pady=5)  

    ctk.CTkButton(input_window, text="Delete", command=submit_inputs).pack(pady=20)

    
   
def issue_book():
    input_window = ctk.CTkToplevel()
    input_window.title("Issue Book")
    input_window.geometry("400x300")

    book_title_var = ctk.StringVar()
    user_id_var = ctk.StringVar()

    def submit_inputs():
        try:
            book_title = book_title_var.get().strip().title()
            user_id = user_id_var.get().strip()

            if not book_title or not user_id:
                messagebox.showerror("Input Error", "All fields must be filled out!")
                return

            books_df = pd.read_csv("books.csv")
            book_row = books_df[books_df["Title"].str.title() == book_title]

            if book_row.empty:
                messagebox.showerror("Not Found", f"Book '{book_title}' not found!")
                return

            if book_row["Available"].values[0].lower() == "no":
                messagebox.showerror("Unavailable", f"Book '{book_title}' is already issued!")
                return
            
            users_df = pd.read_csv("users.csv")
            user_row = users_df[users_df["user_id"] == int(user_id)]

            if user_row.empty:
                messagebox.showerror("User Not Found", f"User with ID {user_id} not found!")
                return

            books_df.loc[books_df["Title"].str.title() == book_title, "Available"] = "no"
            books_df.to_csv("books.csv", index=False)

            issue_date = datetime.now().strftime("%Y-%m-%d")
            return_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")  # 2-week loan period

            try:
                loans_df = pd.read_csv("loans.csv")
            except FileNotFoundError:
                loans_df = pd.DataFrame(columns=["loan_id", "book_title", "user_name", "user_id", "loan_date", "return_date", "status"])

            next_loan_id = loans_df["loan_id"].max() + 1 if not loans_df.empty else 1

            new_loan = pd.DataFrame([{
                "loan_id": next_loan_id,
                "book_title": book_title,
                "user_name": user_row["username"].values[0],
                "user_id": user_id,
                "loan_date": issue_date,
                "return_date": return_date,
                "status": "Borrowed",
            }])
            
            loans_df = pd.concat([loans_df, new_loan], ignore_index=True)
            loans_df.to_csv("loans.csv", index=False)

            messagebox.showinfo("Success", f"Book '{book_title}' issued successfully to {user_row['username'].values[0]} (ID: {user_id})!")
            input_window.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # GUI Elements
    ctk.CTkLabel(input_window, text="Enter Book Title:", font=("Arial", 14)).pack(pady=10)
    ctk.CTkEntry(input_window, textvariable=book_title_var).pack(pady=5)

    ctk.CTkLabel(input_window, text="Enter User ID:", font=("Arial", 14)).pack(pady=10)
    ctk.CTkEntry(input_window, textvariable=user_id_var).pack(pady=5)

    ctk.CTkButton(input_window, text="Issue Book", command=submit_inputs).pack(pady=20)


def return_book():
    input_window = ctk.CTkToplevel()
    input_window.title("Return Book")
    input_window.geometry("400x300")

    loan_id_var = ctk.StringVar()
    book_title_var = ctk.StringVar()

    def submit_inputs():
        try:
            loan_id = loan_id_var.get().strip()
            book_title = book_title_var.get().strip().title()

            if not loan_id or not book_title:
                messagebox.showerror("Input Error", "Loan ID and Book Title must be provided!")
                return

            loans_df = pd.read_csv("loans.csv")
            loan_row = loans_df[loans_df["loan_id"] == int(loan_id)]

            if loan_row.empty:
                messagebox.showerror("Not Found", f"Loan ID '{loan_id}' not found!")
                return

            if loan_row["status"].values[0].lower() == "returned":
                messagebox.showinfo("Already Returned", f"Loan ID '{loan_id}' has already been returned.")
                return

            if loan_row["book_title"].values[0].strip().title() != book_title:
                messagebox.showerror("Mismatch", f"The book title '{book_title}' does not match the loan record.")
                return

            books_df = pd.read_csv("books.csv")
            book_row = books_df[books_df["Title"].str.title() == book_title]
            if book_row.empty:
                messagebox.showerror("Book Not Found", f"Book '{book_title}' not found in inventory!")
                return
            
            books_df.loc[books_df["Title"].str.title() == book_title, "Available"] = "yes"

            # Calculate fine if the book is overdue
            return_date = datetime.now().strftime("%Y-%m-%d")
            loan_date = datetime.strptime(loan_row["loan_date"].values[0], "%Y-%m-%d")
            return_date_obj = datetime.strptime(return_date, "%Y-%m-%d")
            overdue_days = (return_date_obj - loan_date).days - 14  # Assume 14 days loan period

            fine = 0
            if overdue_days > 0:
                fine = overdue_days * 5  # 5 pounds fine per day overdue 

            loans_df.loc[loans_df["loan_id"] == int(loan_id), "status"] = "Returned"
            loans_df.loc[loans_df["loan_id"] == int(loan_id), "return_date"] = return_date
            loans_df.loc[loans_df["loan_id"] == int(loan_id), "fine"] = fine

            books_df.to_csv("books.csv", index=False)
            loans_df.to_csv("loans.csv", index=False)
            
            fine_message = f"Book '{book_title}' returned successfully!"
            if fine > 0:
                fine_message += f"\nFine: {fine}egp for {overdue_days} day(s) overdue."

            messagebox.showinfo("Success", fine_message)
            input_window.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # GUI Elements
    ctk.CTkLabel(input_window, text="Enter Loan ID:", font=("Arial", 14)).pack(pady=10)
    ctk.CTkEntry(input_window, textvariable=loan_id_var).pack(pady=5)

    ctk.CTkLabel(input_window, text="Enter Book Title:", font=("Arial", 14)).pack(pady=10)
    ctk.CTkEntry(input_window, textvariable=book_title_var).pack(pady=5)

    ctk.CTkButton(input_window, text="Return Book", command=submit_inputs).pack(pady=20)

    
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
