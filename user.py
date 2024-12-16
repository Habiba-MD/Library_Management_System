import customtkinter as ctk
from tkinter import messagebox
import pandas as pd
import tkinter.ttk as ttk
from PIL import Image,ImageTk
from userFunc import *  
from sideButtonsFunc import pay_fines

books_data = pd.read_csv('books.csv')
books_data['Cover_Image_Path'] = books_data['Title'].apply(lambda title: f"book_covers/{title}.jpeg")
users_data = pd.read_csv('users.csv')
loans_data = pd.read_csv('loans.csv')


def create_user_window(username):
    ctk.set_appearance_mode('light')
    ctk.set_default_color_theme('blue')
    user_window = ctk.CTk()
    user_window.title("User Window")
    user_window.geometry("1000x700")

    # Create main frame
    main_frame = ctk.CTkFrame(user_window)
    main_frame.pack(fill="both", expand=True)

    # Left section 
    left_frame = ctk.CTkFrame(main_frame)
    left_frame.pack(side="left", fill="y", padx=20, pady=20)
    
    username_label = ctk.CTkLabel(left_frame, text=f"Welcome, {username}!", font=("Arial", 16, "bold"))
    username_label.pack(pady=(10, 20))

    # Buttons
    button1 = ctk.CTkButton(left_frame, text="Borrow Book", command=borrow_book, height=35, font=("Arial", 16, "bold"))
    button1.pack(pady=5, padx=10)
    
    button2 = ctk.CTkButton(left_frame, text="Buy Book", command=buy_book, height=35, font=("Arial", 16, "bold"))
    button2.pack(pady=5, padx=10)
    
    button3 = ctk.CTkButton(left_frame, text="Pay Fines", command=pay_fines, height=35, font=("Arial", 16, "bold"))
    button3.pack(pady=5, padx=10)
    
    button3 = ctk.CTkButton(left_frame, text="Request Book", command=request_book, height=35, font=("Arial", 16, "bold"))
    button3.pack(pady=5, padx=10)
    
    button4 = ctk.CTkButton(left_frame, text="Leave a Review", command=leave_review, height=35, font=("Arial", 16, "bold"))
    button4.pack(pady=5, padx=10)
    
    # Right section 
    right_frame = ctk.CTkFrame(main_frame)
    right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)
    
    # Tabview
    tabview = ctk.CTkTabview(right_frame, bg_color='transparent')
    tabview.pack(fill="both", expand=True)
    
    # Browse Tab
    tabview.add("Browse Books")
    
    browse_frame = ctk.CTkFrame(tabview.tab("Browse Books"))
    browse_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Scrollable Canvas for Books
    canvas = ctk.CTkCanvas(browse_frame)
    scroll_y = ctk.CTkScrollbar(browse_frame, orientation="vertical", command=canvas.yview)
    scroll_y.pack(side="right", fill="y")

    scrollable_frame = ctk.CTkFrame(canvas)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.config(yscrollcommand=scroll_y.set)
    canvas.pack(side="left", fill="both", expand=True)

    # Update the scroll region when content is added
    def update_scroll_region():
        canvas.update_idletasks()  
        canvas.config(scrollregion=canvas.bbox("all"))  

    # Populate Books
    def resize_image(image_path, new_width=150, new_height=200):
        """Resize the image while maintaining quality."""
        try:
            img = Image.open(image_path)
            img_resized = img.resize((new_width, new_height), Image.LANCZOS)
            return ImageTk.PhotoImage(img_resized)
        except Exception as e:
            print(f"Error loading {image_path}: {e}")
            return None

    def populate_books():
        """Populate the books in a scrollable layout."""
        row, col = 0, 0
        columns = 8  # Number of columns in grid layout

        for _, book in books_data.iterrows():
            frame = ctk.CTkFrame(scrollable_frame, width=180, height=300, bg_color="transparent", fg_color="transparent", border_width=0, corner_radius=10)
            frame.grid(row=row, column=col, padx=10, pady=10)

            # Book Image
            img_path = book["Cover_Image_Path"]
            img = resize_image(img_path)
            if img:
                img_label = ctk.CTkLabel(frame, image=img, bg_color="transparent")
                img_label.image = img 
                img_label.pack(pady=5)

            # Book Title and Author
            title_label = ctk.CTkLabel(frame, text=book["Title"], font=("Arial", 12, "bold"), bg_color="transparent", wraplength=150)
            title_label.pack(pady=5)

            author_label = ctk.CTkLabel(frame, text=f"by {book['Author']}", font=("Arial", 10), bg_color="transparent")
            author_label.pack(pady=5)

            # Adjust grid position
            col += 1
            if col >= columns:
                col = 0
                row += 1
        update_scroll_region() 

    populate_books()

    
    
    # Overview Tab
    tabview.add("Search")
    overview_frame = ctk.CTkFrame(tabview.tab("Search"), bg_color='transparent')
    overview_frame.pack(fill="both", expand=True, padx=20, pady=20)

   
    # Search Section for books and users
    search_frame = ctk.CTkFrame(overview_frame, width=1000, height=300, bg_color='transparent')
    search_frame.pack(side="left", fill="both", expand=True, padx=5, pady=10)

    book_search_label = ctk.CTkLabel(search_frame, text="Search for Book", bg_color='transparent')
    book_search_label.pack(pady=10)

    book_search_entry = ctk.CTkEntry(search_frame, placeholder_text="Enter Book Title")
    book_search_entry.pack(pady=10)

    book_search_button = ctk.CTkButton(search_frame, text="Search", command=lambda: search_book(book_search_entry.get()))
    book_search_button.pack(pady=10)
    
    def search_book(book_title):
        try:
            books_data = pd.read_csv("books.csv")
        except FileNotFoundError:
            messagebox.showerror("Error", "The file 'books.csv' does not exist.")
            return

        results = books_data[books_data['Title'].str.contains(book_title, case=False, na=False)]
        
        if not results.empty:
            message = f"Found {len(results)} result(s):\n" + results[['Title', 'Author', 'Genre', 'Available']].to_string(index=False)
        else:
            message = f"No results found for book title: '{book_title}'."
        messagebox.showinfo("Search Results", message)
        
    #All Books Tan
    def update_table_view(filter_genre=None, filter_availability=None, search_query=""):
        # Apply filtering
        filtered_data = books_data
        if filter_genre and filter_genre != "All":
            filtered_data = filtered_data[filtered_data['Genre'] == filter_genre]
        if filter_availability and filter_availability != "All":
            filtered_data = filtered_data[filtered_data['Available'] == filter_availability]
        if search_query:
            filtered_data = filtered_data[filtered_data['Title'].str.contains(search_query, case=False, na=False)]

        for row in tree.get_children():
            tree.delete(row)

        for _, row in filtered_data.iterrows():
            tree.insert("", "end", values=(
                row['Book_ID'],
                row['Title'],
                row['Author'],
                row['Genre'],
                row['Available'],
                row['Rating'],
                row['Price'],
                row['AvailableCopies']
            ))

    tabview.add("All Books")

    books_frame = ctk.CTkFrame(tabview.tab("All Books"))
    books_frame.pack(fill="both", expand=True, padx=20, pady=20)

    books_label = ctk.CTkLabel(books_frame, text="Table View of All The Books in The Library")
    books_label.pack(pady=20)

    search_filter_frame = ctk.CTkFrame(books_frame)
    search_filter_frame.pack(pady=10)

    # Search by Title
    search_label = ctk.CTkLabel(search_filter_frame, text="Search by Title:")
    search_label.grid(row=0, column=0, padx=10)

    search_entry = ctk.CTkEntry(search_filter_frame, placeholder_text="Enter book title")
    search_entry.grid(row=0, column=1, padx=10)

    # Filter by Genre
    genre_label = ctk.CTkLabel(search_filter_frame, text="Filter by Genre:")
    genre_label.grid(row=0, column=2, padx=10)

    genre_options = ["All", *books_data['Genre'].unique()]
    genre_dropdown = ctk.CTkComboBox(search_filter_frame, values=genre_options, state="normal")
    genre_dropdown.set("All")
    genre_dropdown.grid(row=0, column=3, padx=10)

    # Filter by Availability
    availability_label = ctk.CTkLabel(search_filter_frame, text="Filter by Availability:")
    availability_label.grid(row=0, column=4, padx=10)

    availability_options = ["All", "Yes", "No"]
    availability_dropdown = ctk.CTkComboBox(search_filter_frame, values=availability_options, state="normal")
    availability_dropdown.set("All")
    availability_dropdown.grid(row=0, column=5, padx=10)

    # Filter Button
    filter_button = ctk.CTkButton(search_filter_frame, text="Search", command=lambda: update_table_view(
        filter_genre=genre_dropdown.get(),
        filter_availability=availability_dropdown.get(),
        search_query=search_entry.get()
    ))
    filter_button.grid(row=0, column=6, padx=10)

    # Table for displaying books
    columns = ("Book_ID", "Title", "Author", "Genre", "Availability", "Rating", "Price","Available Copies")
    tree = ttk.Treeview(books_frame, columns=columns, show="headings")
    tree.pack(fill="both", expand=True, pady=20)
    
    for col in columns:
        tree.heading(col, text=col)

    update_table_view()
    
    #Loans tab
    def update_loans_table_view(username="", search_query="", filter_status=""):
        filtered_data = loans_data
        if username:
            filtered_data = filtered_data[filtered_data['user_name'] == username] 
        
        if search_query:
            filtered_data = filtered_data[filtered_data['book_title'].str.contains(search_query, case=False, na=False)]
            
        if filter_status and filter_status != "All":
            filtered_data = filtered_data[filtered_data['status'] == filter_status]

        for row in loan_tree.get_children():
            loan_tree.delete(row)

        for _, row in filtered_data.iterrows():
            loan_tree.insert("", "end", values=(
                row['loan_id'],
                row['book_title'],
                row['user_name'],
                row['loan_date'],
                row['return_date'],
                row['loan_duration'],
                row['status'],
                row['fine']
            ))

    tabview.add("Your Loans")

    loans_frame = ctk.CTkFrame(tabview.tab("Your Loans"))
    loans_frame.pack(fill="both", expand=True, padx=20, pady=20)

    loans_label = ctk.CTkLabel(loans_frame, text="Table View of All Your Loans in The Library")
    loans_label.pack(pady=20)

    search_filter_frame = ctk.CTkFrame(loans_frame)
    search_filter_frame.pack(pady=10)

    # Search by Book Title
    search_label = ctk.CTkLabel(search_filter_frame, text="Search by Book Title:")
    search_label.grid(row=0, column=0, padx=10)

    search_entry = ctk.CTkEntry(search_filter_frame, placeholder_text="Enter book title")
    search_entry.grid(row=0, column=1, padx=10)

    # Filter by Loan Status
    status_label = ctk.CTkLabel(search_filter_frame, text="Filter by Status:")
    status_label.grid(row=0, column=2, padx=10)

    status_options = ["All", "Pending", "Returned", "Overdue"]
    status_dropdown = ctk.CTkComboBox(search_filter_frame, values=status_options, state="normal")
    status_dropdown.set("All")
    status_dropdown.grid(row=0, column=3, padx=10)

    # Filter Button
    filter_button = ctk.CTkButton(search_filter_frame, text="Search", command=lambda: update_loans_table_view(
        username=username,
        search_query=search_entry.get(),
        filter_status=status_dropdown.get()
    ))
    filter_button.grid(row=0, column=4, padx=10)

    # Table for displaying loans
    columns = ("loan_id", "book_title", "user_name", "loan_date", "return_date", 'loan_duration',"status", "fine")
    loan_tree = ttk.Treeview(loans_frame, columns=columns, show="headings")
    loan_tree.pack(fill="both", expand=True, pady=20)

    for col in columns:
        loan_tree.heading(col, text=col)

    update_loans_table_view(username=username)
    
    
    
    
    
    
    user_window.mainloop()
create_user_window("rawan")
