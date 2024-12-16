import tkinter.messagebox as messagebox
import customtkinter as ctk
import pandas as pd
from datetime import datetime, timedelta

def add_book():
    input_window = ctk.CTkToplevel()
    input_window.title("Add Book")
    input_window.geometry("400x600") 
    input_window.attributes("-topmost", True)  
    book_id_var = ctk.StringVar()
    book_title_var = ctk.StringVar()
    book_author_var = ctk.StringVar()
    book_genre_var = ctk.StringVar()
    book_price_var = ctk.StringVar()
    book_quantity_var = ctk.StringVar()

    def submit_inputs():
        try:
            book_id = book_id_var.get().strip().title()
            book_title = book_title_var.get().strip().title()
            book_author = book_author_var.get().strip().title()
            book_genre = book_genre_var.get().strip().title()
            book_price = book_price_var.get().strip()
            book_quantity = book_quantity_var.get().strip()
            
            
            if not all([book_id, book_title, book_author, book_genre,book_price,book_quantity]):
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
                "Price": book_price,
                "AvailableCopies":book_quantity,
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
    
    ctk.CTkLabel(input_window, text="Price:", font=("Arial", 14)).pack(pady=5)
    ctk.CTkEntry(input_window, textvariable=book_price_var).pack(pady=5)
    
    ctk.CTkLabel(input_window, text="Available Copies", font=("Arial", 14)).pack(pady=5)
    ctk.CTkEntry(input_window, textvariable=book_quantity_var).pack(pady=5)

    ctk.CTkButton(input_window, text="Submit", command=submit_inputs).pack(pady=20)


def edit_book():
    input_window = ctk.CTkToplevel()
    input_window.title("Edit Book")
    input_window.geometry("400x500")  
    input_window.attributes("-topmost", True)

    book_title_var = ctk.StringVar()
    new_book_title_var = ctk.StringVar()
    new_genre_var = ctk.StringVar()
    new_price_var = ctk.StringVar()
    new_quantity_var = ctk.StringVar()
    
    def submit_edit():
        try:
            book_title = book_title_var.get().strip().title()
            new_book_title = new_book_title_var.get().strip().title()
            new_genre = new_genre_var.get().strip().title()
            new_price = new_price_var.get().strip()
            new_quantity = new_quantity_var.get().strip()

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
            books_df.loc[books_df["Price"].astype(str) == new_book_title, "Price"] = new_price
            
            books_df.loc[books_df["Available Copies"].astype(str) == new_book_title, "AvailableCopies"] = new_quantity

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
    
    ctk.CTkLabel(input_window, text="Enter New Price:", font=("Arial", 14)).pack(pady=5)
    ctk.CTkEntry(input_window, textvariable=new_price_var).pack(pady=5)
    
    ctk.CTkLabel(input_window, text="Enter Quantity:", font=("Arial", 14)).pack(pady=5)
    ctk.CTkEntry(input_window, textvariable=new_quantity_var).pack(pady=5)

    ctk.CTkButton(input_window, text="Submit Changes", command=submit_edit).pack(pady=20)

    
def delete_book():
    input_window = ctk.CTkToplevel()
    input_window.title("Delete Book")
    input_window.geometry("400x200") 
    input_window.attributes("-topmost", True)
     
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

    
   
def loan_book():
    input_window = ctk.CTkToplevel()
    input_window.title("Loan Book")
    input_window.geometry("400x500")
    input_window.attributes("-topmost", True)

    book_title_var = ctk.StringVar()
    user_id_var = ctk.StringVar()
    user_name_var = ctk.StringVar()
    loan_duration_var = ctk.IntVar(value=14)  # Default loan duration is 14 days

    def check_user_fines(user_id):
        """Check if the user has unpaid fines exceeding the allowed limit."""
        try:
            loans_df = pd.read_csv("loans.csv")
            user_loans = loans_df[loans_df["user_id"] == int(user_id)]
            total_fines = user_loans["fine"].sum()
            return total_fines
        except Exception as e:
            messagebox.showerror("Error", f"Error while checking fines: {e}")
            return 0

    def submit_inputs():
        try:
            book_title = book_title_var.get().strip().title()
            user_id = user_id_var.get().strip()
            user_name = user_name_var.get().strip().title()
            loan_duration = loan_duration_var.get()

            if not book_title or not user_id or not user_name:
                messagebox.showerror("Input Error", "All fields must be filled out!")
                return

            books_df = pd.read_csv("books.csv")
            book_row = books_df[books_df["Title"].str.title() == book_title]

            if book_row.empty:
                messagebox.showerror("Not Found", f"Book '{book_title}' not found!")
                return

            # Check available copies
            available_copies = book_row["AvailableCopies"].values[0]
            if available_copies <= 0:
                messagebox.showerror("Unavailable", f"No available copies of '{book_title}' to issue!")
                return

            users_df = pd.read_csv("users.csv")
            user_row = users_df[
                (users_df["user_id"] == int(user_id)) & 
                (users_df["username"].str.title() == user_name)
            ]

            if user_row.empty:
                messagebox.showerror("User Not Found", f"User '{user_name}' with ID {user_id} not found!")
                return

            # Check for fines
            total_fines = check_user_fines(user_id)
            if total_fines > 100:
                messagebox.showerror("Outstanding Fines", f"User '{user_name}' has unpaid fines totaling {total_fines} EGP. They must pay before borrowing a book.")
                return

            # Decrease available copies
            books_df.loc[books_df["Title"].str.title() == book_title, "AvailableCopies"] = available_copies - 1
            books_df.to_csv("books.csv", index=False)

            loan_date = datetime.now().strftime("%Y-%m-%d")
            return_date = (datetime.now() + timedelta(days=loan_duration)).strftime("%Y-%m-%d")

            try:
                loans_df = pd.read_csv("loans.csv")
            except FileNotFoundError:
                loans_df = pd.DataFrame(columns=["loan_id", "book_title", "user_name", "user_id", "loan_date", "return_date", "loan_duration", "status", "fine"])

            next_loan_id = loans_df["loan_id"].max() + 1 if not loans_df.empty else 1

            new_loan = pd.DataFrame([{
                "loan_id": next_loan_id,
                "book_title": book_title,
                "user_name": user_name,
                "user_id": user_id,
                "loan_date": loan_date,
                "return_date": return_date,
                "loan_duration": loan_duration,  
                "status": "Borrowed",
                "fine": 0
            }])
            
            loans_df = pd.concat([loans_df, new_loan], ignore_index=True)
            loans_df.to_csv("loans.csv", index=False)

            messagebox.showinfo("Success", f"Book '{book_title}' loaned successfully to {user_name} (ID: {user_id}) for {loan_duration} days!")
            input_window.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # GUI Elements
    ctk.CTkLabel(input_window, text="Enter Book Title:", font=("Arial", 14)).pack(pady=10)
    ctk.CTkEntry(input_window, textvariable=book_title_var).pack(pady=5)

    ctk.CTkLabel(input_window, text="Enter User ID:", font=("Arial", 14)).pack(pady=10)
    ctk.CTkEntry(input_window, textvariable=user_id_var).pack(pady=5)

    ctk.CTkLabel(input_window, text="Enter User Name:", font=("Arial", 14)).pack(pady=10)
    ctk.CTkEntry(input_window, textvariable=user_name_var).pack(pady=5)

    ctk.CTkLabel(input_window, text="Select Loan Duration (days):", font=("Arial", 14)).pack(pady=10)
    ctk.CTkOptionMenu(
        input_window, 
        values=["7", "14", "21", "30"], 
        variable=loan_duration_var
    ).pack(pady=5)

    ctk.CTkButton(input_window, text="Loan Book", command=submit_inputs).pack(pady=20)


def return_book():
    input_window = ctk.CTkToplevel()
    input_window.title("Return Book")
    input_window.geometry("400x300")
    input_window.attributes("-topmost", True)

    loan_id_var = ctk.StringVar()
    book_title_var = ctk.StringVar()

    def calculate_damage_fine(book_price):
        damage_window = ctk.CTkToplevel()
        damage_window.title("Calculate Damage Fine")
        damage_window.geometry("400x200")

        damage_var = ctk.StringVar(value="Simple")
        damage_fine = ctk.DoubleVar(value=0)

        def submit_damage():
            damage_type = damage_var.get()
            fine_percentage = {
                "Simple": 0.1,
                "Medium": 0.5,
                "Unfixable": 1.0,
            }.get(damage_type, 0)

            calculated_fine = book_price * fine_percentage
            damage_fine.set(calculated_fine)
            messagebox.showinfo("Damage Fine", f"Damage Fine: {calculated_fine} EGP")
            damage_window.destroy()

        # GUI Elements for Damage Window
        ctk.CTkLabel(damage_window, text="Select Damage Severity:", font=("Arial", 14)).pack(pady=10)

        for damage in ["Simple", "Medium", "Unfixable"]:
            ctk.CTkRadioButton(
                damage_window, text=damage, variable=damage_var, value=damage
            ).pack(anchor="w", padx=20)

        ctk.CTkButton(damage_window, text="Submit", command=submit_damage).pack(pady=20)

        damage_window.wait_window()
        return damage_fine.get()

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

            # Increase available copies
            books_df.loc[books_df["Title"].str.title() == book_title, "AvailableCopies"] += 1

            # Calculate fine if the book is overdue
            return_date = datetime.now().strftime("%Y-%m-%d")
            loan_date = datetime.strptime(loan_row["loan_date"].values[0], "%Y-%m-%d")
            return_date_obj = datetime.strptime(return_date, "%Y-%m-%d")

            # Get the loan period from the loan data
            loan_duration = loan_row["loan_duration"].values[0]  # Assume the column is 'loan_period'
            overdue_days = (return_date_obj - loan_date).days - loan_duration  # Calculate overdue days based on loan period

            overdue_fine = 0
            overdue_message = ""

            if overdue_days > 0:
                overdue_fine = overdue_days * 5  # 5 pounds fine per day overdue
                overdue_message = f"\nThis book is {overdue_days} days overdue. Fine: {overdue_fine} EGP."

            # Ask if the book is damaged
            total_fine = overdue_fine
            is_damaged = messagebox.askyesno("Damage Check", "Is the book damaged?")
            if is_damaged:
                book_price = book_row["Price"].values[0]
                damage_fine = calculate_damage_fine(book_price)
                total_fine += damage_fine

            loans_df.loc[loans_df["loan_id"] == int(loan_id), "status"] = "Returned"
            loans_df.loc[loans_df["loan_id"] == int(loan_id), "return_date"] = return_date
            loans_df.loc[loans_df["loan_id"] == int(loan_id), "fine"] = total_fine

            books_df.to_csv("books.csv", index=False)
            loans_df.to_csv("loans.csv", index=False)

            fine_message = f"Book '{book_title}' returned successfully!{overdue_message}"
            if total_fine > 0:
                fine_message += f"\nTotal Fine: {total_fine} EGP."

            messagebox.showinfo("Success", fine_message)
            input_window.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # GUI Elements for Return Book Window
    ctk.CTkLabel(input_window, text="Enter Loan ID:", font=("Arial", 14)).pack(pady=10)
    ctk.CTkEntry(input_window, textvariable=loan_id_var).pack(pady=5)

    ctk.CTkLabel(input_window, text="Enter Book Title:", font=("Arial", 14)).pack(pady=10)
    ctk.CTkEntry(input_window, textvariable=book_title_var).pack(pady=5)

    ctk.CTkButton(input_window, text="Return Book", command=submit_inputs).pack(pady=20)



def purchase_book():
    def calculate_total_price():
        book_title = book_title_entry.get()
        quantity = quantity_entry.get()

        if not book_title or not quantity.isdigit():
            messagebox.showerror("Error", "Please provide a valid Book Title and Quantity.")
            return

        quantity = int(quantity)

        # Load book data
        try:
            books_df = pd.read_csv('books.csv')
            books_df['Price'] = pd.to_numeric(books_df['Price'], errors='coerce')
            books_df['AvailableCopies'] = pd.to_numeric(books_df['AvailableCopies'], errors='coerce')
        except FileNotFoundError:
            messagebox.showerror("Error", "Books database not found.")
            return

        # Check if the book exists
        book_row = books_df[books_df['Title'].str.lower() == book_title.lower()]
        if not book_row.empty:
            available_quantity = book_row.iloc[0]['AvailableCopies']
            if quantity > available_quantity:
                messagebox.showinfo("Info", f"Only {available_quantity} copies are available.")
                total_price_label.configure(text="Total Price: $0.00")
                return

            price_per_unit = book_row.iloc[0]['Price']
            total_price = price_per_unit * quantity
            total_price_label.configure(text=f"Total Price: ${total_price:.2f}")
        else:
            messagebox.showerror("Error", "Book Title not found.")

    def complete_purchase():
        user_name = user_name_entry.get()
        user_id = user_id_entry.get()
        book_title = book_title_entry.get()
        quantity = quantity_entry.get()
        payment_method = payment_method_var.get()

        if not user_name or not user_id:
            messagebox.showerror("Error", "Please provide User Name and User ID.")
            return

        if not book_title or not quantity.isdigit():
            messagebox.showerror("Error", "Please provide a valid Book Title and Quantity.")
            return

        if not payment_method:
            messagebox.showerror("Error", "Please select a payment method.")
            return

        quantity = int(quantity)

        if payment_method == "Visa":
            open_visa_window()
        else:
            finalize_purchase(user_name, user_id, book_title, quantity)

    def open_visa_window():
        visa_window = ctk.CTkToplevel()
        visa_window.title("Visa Payment")
        visa_window.geometry("500x400")
        visa_window.attributes("-topmost", True)

        ctk.CTkLabel(visa_window, text="Visa Card Number:").pack(pady=10)
        visa_card_entry = ctk.CTkEntry(visa_window)
        visa_card_entry.pack(pady=10)

        ctk.CTkLabel(visa_window, text="Expiry Date (MM/YY):").pack(pady=10)
        expiry_date_entry = ctk.CTkEntry(visa_window)
        expiry_date_entry.pack(pady=10)

        ctk.CTkLabel(visa_window, text="CVV:").pack(pady=10)
        cvv_entry = ctk.CTkEntry(visa_window, show="*")
        cvv_entry.pack(pady=10)

        def submit_visa_payment():
            visa_card = visa_card_entry.get()
            expiry_date = expiry_date_entry.get()
            cvv = cvv_entry.get()

            if not visa_card or not expiry_date or not cvv:
                messagebox.showerror("Error", "Please fill in all Visa details.")
                return

            if not visa_card.isdigit() or len(visa_card) != 16:
                messagebox.showerror("Error", "Visa card number must be exactly 16 digits.")
                return

            if not cvv.isdigit() or len(cvv) != 3:
                messagebox.showerror("Error", "CVV must be exactly 3 digits.")
                return

            visa_window.destroy()
            finalize_purchase(user_name_entry.get(), user_id_entry.get(), book_title_entry.get(), int(quantity_entry.get()))

        submit_button = ctk.CTkButton(visa_window, text="Submit Payment", command=submit_visa_payment)
        submit_button.pack(pady=20)

    def finalize_purchase(user_name, user_id, book_title, quantity):
        try:
            books_df = pd.read_csv('books.csv')
            books_df['Price'] = pd.to_numeric(books_df['Price'], errors='coerce')
            books_df['AvailableCopies'] = pd.to_numeric(books_df['AvailableCopies'], errors='coerce')
        except FileNotFoundError:
            messagebox.showerror("Error", "Books database not found.")
            return

        book_row = books_df[books_df['Title'].str.lower() == book_title.lower()]
        if not book_row.empty:
            available_quantity = book_row.iloc[0]['AvailableCopies']
            if quantity > available_quantity:
                messagebox.showinfo("Info", f"Only {available_quantity} copies are available.")
                return

            total_price = book_row.iloc[0]['Price'] * quantity
            new_quantity = available_quantity - quantity
            books_df.loc[books_df['Title'].str.lower() == book_title.lower(), 'AvailableCopies'] = new_quantity
            books_df.to_csv('books.csv', index=False)

            transaction_data = {
                'Transaction_ID': [len(pd.read_csv('transactions.csv', on_bad_lines="skip")) + 1],
                'Date': [datetime.now().strftime("%Y-%m-%d")],
                'Amount': [total_price],
                'Transaction_Type': ['Purchase'],
                'Book_Title': [book_title],
                'Remarks': [f"User: {user_name}, ID: {user_id}, Payment: {payment_method_var.get()}"],
                'user_id': [user_id],
                'user_name': [user_name]
            }

            try:
                transactions_df = pd.read_csv('transactions.csv')
            except FileNotFoundError:
                transactions_df = pd.DataFrame(columns=transaction_data.keys())

            transactions_df = pd.concat([transactions_df, pd.DataFrame(transaction_data)])
            transactions_df.to_csv('transactions.csv', index=False)

            messagebox.showinfo("Success", f"Purchase completed!\nTotal Price: ${total_price:.2f}")
            input_window.destroy()
        else:
            messagebox.showerror("Error", "Book Title not found.")

    # Create purchase window
    input_window = ctk.CTkToplevel()
    input_window.title("Purchase Book")
    input_window.geometry("400x700")
    input_window.attributes("-topmost", True)

    ctk.CTkLabel(input_window, text="User Name:").pack(pady=10)
    user_name_entry = ctk.CTkEntry(input_window)
    user_name_entry.pack(pady=10)

    ctk.CTkLabel(input_window, text="User ID:").pack(pady=10)
    user_id_entry = ctk.CTkEntry(input_window)
    user_id_entry.pack(pady=10)

    ctk.CTkLabel(input_window, text="Book Title:").pack(pady=10)
    book_title_entry = ctk.CTkEntry(input_window)
    book_title_entry.pack(pady=10)

    ctk.CTkLabel(input_window, text="Quantity:").pack(pady=10)
    quantity_entry = ctk.CTkEntry(input_window)
    quantity_entry.pack(pady=10)

    ctk.CTkLabel(input_window, text="Payment Method:").pack(pady=10)
    payment_method_var = ctk.StringVar()
    payment_method_dropdown = ctk.CTkComboBox(input_window, values=["Cash", "Visa"], variable=payment_method_var)
    payment_method_dropdown.pack(pady=10)

    calculate_button = ctk.CTkButton(input_window, text="Calculate Total Price", command=calculate_total_price)
    calculate_button.pack(pady=10)

    total_price_label = ctk.CTkLabel(input_window, text="Total Price: $0.00")
    total_price_label.pack(pady=10)

    purchase_button = ctk.CTkButton(input_window, text="Complete Purchase", command=complete_purchase)
    purchase_button.pack(pady=20)

def pay_fines():
    input_window = ctk.CTkToplevel()
    input_window.title("Pay Fines")
    input_window.geometry("400x400")
    input_window.attributes("-topmost", True)

    user_id_var = ctk.StringVar()
    user_name_var = ctk.StringVar()
    payment_var = ctk.DoubleVar()

    def submit_payment():
        try:
            user_id = user_id_var.get().strip()
            user_name = user_name_var.get().strip().title()
            payment_amount = payment_var.get()

            if not user_id or not user_name:
                messagebox.showerror("Input Error", "User ID and Name must be provided!")
                return

            if payment_amount <= 0:
                messagebox.showerror("Input Error", "Payment amount must be greater than 0!")
                return

            loans_df = pd.read_csv("loans.csv")
            user_loans = loans_df[(loans_df["user_id"] == int(user_id)) & (loans_df["user_name"].str.title() == user_name)]

            if user_loans.empty:
                messagebox.showerror("Not Found", f"No loans found for User ID '{user_id}' and Name '{user_name}'!")
                return

            total_fines = user_loans["fine"].sum()

            if total_fines <= 0:
                messagebox.showinfo("No Fines", f"User '{user_name}' (ID: {user_id}) has no outstanding fines.")
                return

            if payment_amount > total_fines:
                messagebox.showerror("Overpayment", "Payment amount exceeds the total outstanding fines!")
                return

            # Update fines
            remaining_payment = payment_amount
            for index, row in user_loans.iterrows():
                if remaining_payment <= 0:
                    break

                current_fine = row["fine"]
                if current_fine > 0:
                    if remaining_payment >= current_fine:
                        loans_df.loc[index, "fine"] = 0
                        remaining_payment -= current_fine
                    else:
                        loans_df.loc[index, "fine"] -= remaining_payment
                        remaining_payment = 0

            # Record transaction with required columns
            transactions_df = pd.read_csv("transactions.csv")
            new_transaction = pd.DataFrame([{
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Amount": payment_amount,
                "Transaction_Type": "Fine Payment",
                "Remarks": "Payment for outstanding fines",
                "Transaction_ID":[len(pd.read_csv('transactions.csv', on_bad_lines="skip")) + 1],
                "Book_Title": None,
                "user_id": user_id,
                "user_name": user_name,
            }])

            # Concatenate new transaction to the existing DataFrame
            transactions_df = pd.concat([transactions_df, new_transaction], ignore_index=True)

            loans_df.to_csv("loans.csv", index=False)
            transactions_df.to_csv("transactions.csv", index=False)

            messagebox.showinfo(
                "Payment Success", f"Payment of {payment_amount} EGP recorded for User '{user_name}' (ID: {user_id})."
            )
            input_window.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def check_fines():
        try:
            user_id = user_id_var.get().strip()
            user_name = user_name_var.get().strip().title()

            if not user_id or not user_name:
                messagebox.showerror("Input Error", "User ID and Name must be provided!")
                return

            loans_df = pd.read_csv("loans.csv")
            user_loans = loans_df[(loans_df["user_id"] == int(user_id)) & (loans_df["user_name"].str.title() == user_name)]

            if user_loans.empty:
                messagebox.showerror("Not Found", f"No loans found for User ID '{user_id}' and Name '{user_name}'!")
                return

            total_fines = user_loans["fine"].sum()

            if total_fines > 0:
                messagebox.showinfo(
                    "Outstanding Fines", f"User '{user_name}' (ID: {user_id}) has total fines of {total_fines} EGP."
                )
            else:
                messagebox.showinfo("No Fines", f"User '{user_name}' (ID: {user_id}) has no outstanding fines.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # GUI Elements for Pay Fines Window
    ctk.CTkLabel(input_window, text="Enter User ID:", font=("Arial", 14)).pack(pady=10)
    ctk.CTkEntry(input_window, textvariable=user_id_var).pack(pady=5)

    ctk.CTkLabel(input_window, text="Enter User Name:", font=("Arial", 14)).pack(pady=10)
    ctk.CTkEntry(input_window, textvariable=user_name_var).pack(pady=5)

    ctk.CTkButton(input_window, text="Check Fines", command=check_fines).pack(pady=10)

    ctk.CTkLabel(input_window, text="Enter Payment Amount:", font=("Arial", 14)).pack(pady=10)
    ctk.CTkEntry(input_window, textvariable=payment_var).pack(pady=5)

    ctk.CTkButton(input_window, text="Submit Payment", command=submit_payment).pack(pady=20)
  

def add_user():
    input_window = ctk.CTkToplevel()
    input_window.title("Add User")
    input_window.geometry("400x400")
    input_window.attributes("-topmost", True)

    user_id_var = ctk.StringVar()
    username_var = ctk.StringVar()
    email_var = ctk.StringVar()
    password_var = ctk.StringVar()
    
    def submit_inputs():
        try:
            user_id = user_id_var.get().strip()
            username = username_var.get().strip()
            email = email_var.get().strip().lower()
            password = password_var.get().strip()

            if not all([user_id, username, email, password]):
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
                "role":"user"
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

    ctk.CTkButton(input_window, text="Add User", command=submit_inputs).pack(pady=20)



    
def delete_user():
    input_window = ctk.CTkToplevel()
    input_window.title("Delete User")
    input_window.geometry("400x250")
    input_window.attributes("-topmost", True)
    
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


def add_employee():    
    input_window = ctk.CTkToplevel()
    input_window.title("Add Employee")
    input_window.geometry("400x400")
    input_window.attributes("-topmost", True)

    user_id_var = ctk.StringVar()
    username_var = ctk.StringVar()
    email_var = ctk.StringVar()
    password_var = ctk.StringVar()

    def submit_inputs():
        try:
            user_id = user_id_var.get().strip()
            username = username_var.get().strip()
            email = email_var.get().strip().lower()
            password = password_var.get().strip()

            if not all([user_id, username, email, password]):
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
                "role": "employee"
            }
            users_df = pd.concat([users_df, pd.DataFrame([new_row])], ignore_index=True)
            users_df.to_csv("users.csv", index=False)

            # Success message
            messagebox.showinfo("Success", f"Employee '{username}' added successfully!")
            input_window.destroy()
        except FileNotFoundError:
            messagebox.showerror("File Error", "The file 'users.csv' was not found!")
        except pd.errors.EmptyDataError:
            messagebox.showerror("File Error", "The file 'users.csv' is empty!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # GUI Elements
    ctk.CTkLabel(input_window, text="Employee ID:", font=("Arial", 14)).pack(pady=5)
    ctk.CTkEntry(input_window, textvariable=user_id_var).pack(pady=5)

    ctk.CTkLabel(input_window, text="Employee Name:", font=("Arial", 14)).pack(pady=5)
    ctk.CTkEntry(input_window, textvariable=username_var).pack(pady=5)

    ctk.CTkLabel(input_window, text="Email:", font=("Arial", 14)).pack(pady=5)
    ctk.CTkEntry(input_window, textvariable=email_var).pack(pady=5)

    ctk.CTkLabel(input_window, text="Password:", font=("Arial", 14)).pack(pady=5)
    ctk.CTkEntry(input_window, textvariable=password_var).pack(pady=5)

    ctk.CTkButton(input_window, text="Add Employee", command=submit_inputs).pack(pady=20)


def delete_employee():
    input_window = ctk.CTkToplevel()
    input_window.title("Delete Employee")
    input_window.geometry("400x250")
    input_window.attributes("-topmost", True)
    
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
            messagebox.showinfo("Success", f"Employee '{username}' deleted successfully!")
            input_window.destroy()

        except FileNotFoundError:
            messagebox.showerror("File Error", "The file 'users.csv' was not found!")
        except pd.errors.EmptyDataError:
            messagebox.showerror("File Error", "The file 'users.csv' is empty!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    ctk.CTkLabel(input_window, text="Employee ID (optional):", font=("Arial", 14)).pack(pady=5)
    ctk.CTkEntry(input_window, textvariable=user_id_var).pack(pady=5)

    ctk.CTkLabel(input_window, text="Employee Name (optional):", font=("Arial", 14)).pack(pady=5)
    ctk.CTkEntry(input_window, textvariable=username_var).pack(pady=5)

    ctk.CTkButton(input_window, text="Delete Employee", command=submit_inputs).pack(pady=20)
    
def order_books():
    # Create a new window for ordering books
    order_window = ctk.CTkToplevel()
    order_window.title("Order New Books")
    order_window.geometry("500x400")
    
    # Define a list to store books to order
    books_to_order = []

    def add_book_to_order():
        book_title = book_title_var.get().strip().title()
        book_quantity = quantity_var.get()

        if not book_title or book_quantity <= 0:
            messagebox.showerror("Input Error", "Please enter a valid book title and quantity!")
            return

        # Add the book title and quantity to the list
        books_to_order.append({"title": book_title, "quantity": book_quantity})

        # Clear the input fields
        book_title_var.set("")
        quantity_var.set(1)

        # Update the display of added books
        order_textbox.insert("end", f"{book_title} - {book_quantity} copies\n")

    def submit_order():
        try:
            # Check if there are any books in the order
            if not books_to_order:
                messagebox.showerror("Input Error", "No books to order!")
                return

            # Load the books inventory
            books_df = pd.read_csv("books.csv")

            for book in books_to_order:
                book_title = book["title"]
                quantity = book["quantity"]

                # Check if the book exists in the inventory
                book_row = books_df[books_df["Title"].str.title() == book_title]
                
                if book_row.empty:
                    messagebox.showwarning("Book Not Found", f"Book '{book_title}' not found in inventory!")
                    continue  # Skip this book

                # Update the available copies of the existing book
                available_copies = book_row["AvailableCopies"].values[0]
                books_df.loc[books_df["Title"].str.title() == book_title, "AvailableCopies"] = available_copies + quantity

            # Save the updated books inventory
            books_df.to_csv("books.csv", index=False)

            messagebox.showinfo("Order Success", "Books ordered successfully and inventory updated!")
            order_window.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Create input fields for book title and quantity
    book_title_var = ctk.StringVar()
    quantity_var = ctk.IntVar(value=1)

    ctk.CTkLabel(order_window, text="Enter Book Title:", font=("Arial", 14)).pack(pady=10)
    ctk.CTkEntry(order_window, textvariable=book_title_var).pack(pady=5)

    ctk.CTkLabel(order_window, text="Enter Quantity:", font=("Arial", 14)).pack(pady=10)
    ctk.CTkEntry(order_window, textvariable=quantity_var).pack(pady=5)

    # Button to add the book to the order list
    add_button = ctk.CTkButton(order_window, text="Add Book to Order", command=add_book_to_order)
    add_button.pack(pady=10)

    # Replace the Listbox with a Textbox to display added books
    order_textbox = ctk.CTkTextbox(order_window, height=10, width=50)
    order_textbox.pack(fill="both", expand=True, pady=20)

    # Button to submit the order
    submit_button = ctk.CTkButton(order_window, text="Submit Order", command=submit_order)
    submit_button.pack(pady=20)
