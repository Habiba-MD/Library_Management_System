import tkinter.messagebox as messagebox
import customtkinter as ctk
import pandas as pd
from datetime import datetime, timedelta

def borrow_book():
    input_window = ctk.CTkToplevel()
    input_window.title("Borrow Book")
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
    
    def ask_delivery_option(book_title, user_name, loan_duration):
        """Ask the user whether they want to collect the book or get it delivered."""
        delivery_window = ctk.CTkToplevel()
        delivery_window.title("Delivery Options")
        delivery_window.geometry("400x300")
        delivery_window.attributes("-topmost", True)

        def choose_delivery():
            address_var = ctk.StringVar()
            phone_var = ctk.StringVar()

            def submit_delivery_details():
                address = address_var.get().strip()
                phone = phone_var.get().strip()

                if not address or not phone:
                    messagebox.showerror("Input Error", "Both address and phone number are required!")
                    return

                messagebox.showinfo(
                    "Delivery Confirmed",
                    f"Book '{book_title}' will be delivered to:\n{address}\nPhone: {phone}\nWithin three working days"
                )
                delivery_window.destroy()
                input_window.destroy()

            for widget in delivery_window.winfo_children():
                widget.destroy()

            ctk.CTkLabel(delivery_window, text="Enter Delivery Address:", font=("Arial", 14)).pack(pady=10)
            ctk.CTkEntry(delivery_window, textvariable=address_var).pack(pady=5)

            ctk.CTkLabel(delivery_window, text="Enter Phone Number:", font=("Arial", 14)).pack(pady=10)
            ctk.CTkEntry(delivery_window, textvariable=phone_var).pack(pady=5)

            ctk.CTkButton(delivery_window, text="Submit", command=submit_delivery_details).pack(pady=20)

        def choose_library_pickup():
            messagebox.showinfo(
                "Library Pickup Confirmed",
                f"Book '{book_title}' is ready for pickup at the library!\nPlease collect the book within 3 working days or the order will be canceled!"
            )
            delivery_window.destroy()
            input_window.destroy()

        # Delivery options
        ctk.CTkLabel(delivery_window, text="How would you like to receive the book?", font=("Arial", 14)).pack(pady=20)
        ctk.CTkButton(delivery_window, text="Pick Up at Library", command=choose_library_pickup).pack(pady=10)
        ctk.CTkButton(delivery_window, text="Home Delivery", command=choose_delivery).pack(pady=10)


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
                messagebox.showerror("Outstanding Fines", f"User '{user_name}' has unpaid fines totaling {total_fines} EGP. You must pay before borrowing a book.")
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

            messagebox.showinfo("Success", f"Book '{book_title}' borrowed successfully for {loan_duration} days!\n ")
            input_window.destroy()
            
            ask_delivery_option(book_title, user_name, loan_duration)

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

    ctk.CTkButton(input_window, text="Borrow Book", command=submit_inputs).pack(pady=20)
    
def buy_book():
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

        if not user_name or not user_id:
            messagebox.showerror("Error", "Please provide User Name and User ID.")
            return

        if not book_title or not quantity.isdigit():
            messagebox.showerror("Error", "Please provide a valid Book Title and Quantity.")
            return

        quantity = int(quantity)
        open_visa_window()
        

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
            ask_delivery_option(book_title_entry.get(),user_name_entry.get())
            finalize_purchase(user_name_entry.get(), user_id_entry.get(), book_title_entry.get(), int(quantity_entry.get()))

        submit_button = ctk.CTkButton(visa_window, text="Submit Payment", command=submit_visa_payment)
        submit_button.pack(pady=20)
        
    def ask_delivery_option(book_title, user_name):
        """Ask the user whether they want to collect the book or get it delivered."""
        delivery_window = ctk.CTkToplevel()
        delivery_window.title("Delivery Options")
        delivery_window.geometry("400x300")
        delivery_window.attributes("-topmost", True)

        def choose_delivery():
            address_var = ctk.StringVar()
            phone_var = ctk.StringVar()

            def submit_delivery_details():
                address = address_var.get().strip()
                phone = phone_var.get().strip()

                if not address or not phone:
                    messagebox.showerror("Input Error", "Both address and phone number are required!")
                    return

                messagebox.showinfo(
                    "Delivery Confirmed",
                    f"Book '{book_title}' will be delivered to:\n{address}\nPhone: {phone}\nWithin three working days"
                )
                delivery_window.destroy()
                input_window.destroy()

            for widget in delivery_window.winfo_children():
                widget.destroy()

            ctk.CTkLabel(delivery_window, text="Enter Delivery Address:", font=("Arial", 14)).pack(pady=10)
            ctk.CTkEntry(delivery_window, textvariable=address_var).pack(pady=5)

            ctk.CTkLabel(delivery_window, text="Enter Phone Number:", font=("Arial", 14)).pack(pady=10)
            ctk.CTkEntry(delivery_window, textvariable=phone_var).pack(pady=5)

            ctk.CTkButton(delivery_window, text="Submit", command=submit_delivery_details).pack(pady=20)

        def choose_library_pickup():
            messagebox.showinfo(
                "Library Pickup Confirmed",
                f"Book '{book_title}' is ready for pickup at the library!\nPlease collect the book within 3 working days or the order will be canceled!"
            )
            delivery_window.destroy()
            input_window.destroy()

        # Delivery options
        ctk.CTkLabel(delivery_window, text="How would you like to receive the book?", font=("Arial", 14)).pack(pady=20)
        ctk.CTkButton(delivery_window, text="Pick Up at Library", command=choose_library_pickup).pack(pady=10)
        ctk.CTkButton(delivery_window, text="Home Delivery", command=choose_delivery).pack(pady=10)


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
                'Remarks': [f"User: {user_name}, ID: {user_id}, Payment: Visa"],
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
    input_window.geometry("400x600")
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
    
    calculate_button = ctk.CTkButton(input_window, text="Calculate Total Price", command=calculate_total_price)
    calculate_button.pack(pady=10)

    total_price_label = ctk.CTkLabel(input_window, text="Total Price: $0.00")
    total_price_label.pack(pady=10)

    purchase_button = ctk.CTkButton(input_window, text="Complete Purchase", command=complete_purchase)
    purchase_button.pack(pady=20)
    
    
def request_book():
    input_window = ctk.CTkToplevel()
    input_window.title("Request Book")
    input_window.geometry("300x300")
    input_window.attributes("-topmost", True)

    book_title_var = ctk.StringVar()
    user_name_var = ctk.StringVar()

    def submit_request():
        try:
            book_title = book_title_var.get().strip().title()
            user_name = user_name_var.get().strip().title()

            if not book_title or not user_name:
                messagebox.showerror("Input Error", "Both Book Title and Username must be filled out!")
                return

            # Check if the book is already available in the library
            books_df = pd.read_csv("books.csv")
            existing_book = books_df[books_df["Title"].str.title() == book_title]

            if not existing_book.empty:
                book_id = existing_book.iloc[0]["Book_ID"]
                messagebox.showinfo("Book Already Available", f"The book '{book_title}' is already available with ID {book_id}.")
                return

            # If the book is not found, request it
            try:
                requests_df = pd.read_csv("book_requests.csv")
            except FileNotFoundError:
                requests_df = pd.DataFrame(columns=["Request_ID", "Book_Title", "Requested_By"])

            new_request_id = len(requests_df) + 1
            new_request = pd.DataFrame([{
                "Request_ID": new_request_id,
                "Book_Title": book_title,
                "Requested_By": user_name
            }])

            requests_df = pd.concat([requests_df, new_request], ignore_index=True)
            requests_df.to_csv("book_requests.csv", index=False)

            messagebox.showinfo("Request Submitted", f"Your request for the book '{book_title}' has been successfully submitted for review.")
            input_window.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # GUI Elements
    ctk.CTkLabel(input_window, text="Enter Book Title:", font=("Arial", 14)).pack(pady=10)
    ctk.CTkEntry(input_window, textvariable=book_title_var).pack(pady=5)

    ctk.CTkLabel(input_window, text="Enter User Name:", font=("Arial", 14)).pack(pady=10)
    ctk.CTkEntry(input_window, textvariable=user_name_var).pack(pady=5)

    ctk.CTkButton(input_window, text="Request Book", command=submit_request).pack(pady=20)
    
   
reviews_df = pd.read_csv("reviews.csv")  
books_df = pd.read_csv("books.csv")

def leave_review():
    input_window = ctk.CTkToplevel()
    input_window.title("Leave a Review")
    input_window.geometry("300x450")
    input_window.attributes("-topmost", True)

    book_title_var = ctk.StringVar()
    user_name_var = ctk.StringVar()
    review_text_var = ctk.StringVar()
    rating_var = ctk.IntVar(value=1)  
    
    def submit_review():
        global reviews_df  
        try:
            book_title = book_title_var.get().strip().title()
            user_name = user_name_var.get().strip().title()
            review_text = review_text_var.get().strip()
            rating = rating_var.get()

            if not book_title or not user_name or not review_text:
                messagebox.showerror("Input Error", "All fields must be filled out!")
                return

            if rating < 1 or rating > 5:
                messagebox.showerror("Input Error", "Rating must be between 1 and 5!")
                return

            # Find the book ID corresponding to the title
            book = books_df[books_df['Title'].str.title() == book_title]
            if book.empty:
                messagebox.showerror("Book Not Found", f"The book '{book_title}' is not found in the library!")
                return

            book_id = book.iloc[0]["Book_ID"]  
            review_id = len(reviews_df) + 1  
            # Create new review entry
            new_review = pd.DataFrame([{
                "review_id": review_id,
                "user_name": user_name,
                "book_id": book_id,
                "book_title": book_title,
                "review_text": review_text,
                "rating": rating
            }])

            # Append new review to reviews_df
            reviews_df = pd.concat([reviews_df, new_review], ignore_index=True)
            reviews_df.to_csv("reviews.csv", index=False)  

            messagebox.showinfo("Review Submitted", f"Your review for '{book_title}' has been submitted successfully.")
            input_window.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # GUI Elements
    ctk.CTkLabel(input_window, text="Enter Book Title:", font=("Arial", 14)).pack(pady=10)
    ctk.CTkEntry(input_window, textvariable=book_title_var).pack(pady=5)

    ctk.CTkLabel(input_window, text="Enter User Name:", font=("Arial", 14)).pack(pady=10)
    ctk.CTkEntry(input_window, textvariable=user_name_var).pack(pady=5)

    ctk.CTkLabel(input_window, text="Enter Review Text:", font=("Arial", 14)).pack(pady=10)
    ctk.CTkEntry(input_window, textvariable=review_text_var).pack(pady=5)

    ctk.CTkLabel(input_window, text="Rating (1-5):", font=("Arial", 14)).pack(pady=10)
    ctk.CTkComboBox(input_window, values=[str(i) for i in range(1, 6)], variable=rating_var, width=100).pack(pady=5)

    ctk.CTkButton(input_window, text="Submit Review", command=submit_review).pack(pady=20)