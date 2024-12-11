import customtkinter as ctk
from tkinter import messagebox , PhotoImage
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import pandas as pd
from statics import create_available_pie_chart, create_genre_pie_chart # Import figures
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sideButtonsFunc import *

def create_employee_window(username):
    ctk.set_appearance_mode('light')
    ctk.set_default_color_theme('blue')
    employee_window = ctk.CTk()  
    employee_window.title("Employee Window")
    employee_window.geometry("1000x700")

    # Create main frame
    main_frame = ctk.CTkFrame(employee_window)
    main_frame.pack(fill="both", expand=True)

    # Left section 
    left_frame = ctk.CTkFrame(main_frame)
    left_frame.pack(side="left", fill="y", padx=20, pady=20)
    
    # user_icon = Image.open("user.png")  
    # ctk_image = ctk.CTkImage(light_image=user_icon, size=(200, 200))
    
    # image_label = ctk.CTkLabel(left_frame, image=ctk_image, fg_color="transparent", text="")
    # image_label.pack(pady=(20,20), padx=(10,10))
    
    username_label = ctk.CTkLabel(left_frame, text= f"Welcome, {username}!", font=("Arial", 16, "bold"))
    username_label.pack(pady=(10, 20))

    #Buttons
    button1 = ctk.CTkButton(left_frame, text="Add Book",command=add_book,height=35,font=("Arial", 16, "bold"))
    button1.pack(pady=5, padx=10)
    
    button1 = ctk.CTkButton(left_frame, text="Edit Book",command=edit_book,height=35,font=("Arial", 16, "bold"))
    button1.pack(pady=5, padx=10)

    button2 = ctk.CTkButton(left_frame, text="Delete Book",command=delete_book, height=35,font=("Arial", 16, "bold"))
    button2.pack(pady=5, padx=10)

    button3 = ctk.CTkButton(left_frame, text="Issue Book",command= issue_book,height=35,font=("Arial", 16, "bold"))
    button3.pack(pady=5, padx=10)
    
    button4 = ctk.CTkButton(left_frame, text="Return Book",command=return_book,height=35,font=("Arial", 16, "bold"))
    button4.pack(pady=5, padx=10)
    
    button6 = ctk.CTkButton(left_frame, text="Add User",command=add_user, height=35,font=("Arial", 16, "bold"))
    button6.pack(pady=5, padx=10)
    
    button7 = ctk.CTkButton(left_frame, text="Delete User",command=delete_user, height=35,font=("Arial", 16, "bold"))
    button7.pack(pady=5, padx=10)
    
    # Right section 
    right_frame = ctk.CTkFrame(main_frame)
    right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    # Tabview 
    tabview = ctk.CTkTabview(right_frame, bg_color='transparent')
    tabview.pack(fill="both", expand=True)

    # Overview Tab
    tabview.add("Overview")
    overview_frame = ctk.CTkFrame(tabview.tab("Overview"),bg_color='transparent')
    overview_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
   # Create a frame for displaying the charts)
    chart_frame = ctk.CTkFrame(overview_frame)
    chart_frame.pack(side='right',fill="both", expand=True, padx=5, pady=10)

    chart_frame_1 = ctk.CTkFrame(chart_frame)
    chart_frame_1.pack(side="top", fill="both", expand=True)
    
    chart_frame_2 = ctk.CTkFrame(chart_frame)
    chart_frame_2.pack(side="bottom", fill="both", expand=True)
    
    create_available_pie_chart(chart_frame_1) 
    create_genre_pie_chart(chart_frame_2)  
    
    # Create the middle section for searching
    search_frame = ctk.CTkFrame(overview_frame, width=1000, height=300, bg_color='transparent')
    search_frame.pack(side="left", fill="both", expand=True, padx=5, pady=10)

    # Book Search Section
    book_search_label = ctk.CTkLabel(search_frame, text="Search for Book", bg_color='transparent')
    book_search_label.pack(pady=10)

    book_search_entry = ctk.CTkEntry(search_frame, placeholder_text="Enter Book Title")
    book_search_entry.pack(pady=10)

    book_search_button = ctk.CTkButton(search_frame, text="Search", command=lambda: search_book(book_search_entry.get()))
    book_search_button.pack(pady=10)
    
    books_data = pd.read_csv("books.csv")
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

    # User Search Section
    user_search_label = ctk.CTkLabel(search_frame, text="Search for User", bg_color='transparent')
    user_search_label.pack(pady=10)

    user_search_entry = ctk.CTkEntry(search_frame, placeholder_text="Enter Username")
    user_search_entry.pack(pady=10)

    user_search_button = ctk.CTkButton(search_frame, text="Search", command=lambda: search_user(user_search_entry.get()))
    user_search_button.pack(pady=10)
    
    def search_user(user_name):
        try:
            users_data = pd.read_csv("users.csv")
        except FileNotFoundError:
            messagebox.showerror("Error", "The file 'users.csv' does not exist.")
            return
        
        results = users_data[users_data['username'].str.contains(user_name, case=False, na=False)]
        if not results.empty:
            message = f"Found {len(results)} result(s):\n" + results[['username', 'email']].to_string(index=False)
        else:
            message = f"No results found for user name: '{user_name}'."
        messagebox.showinfo("Search Results", message)
        
    # All Books Tab
    def update_table_view(filter_genre=None, filter_availability=None, search_query=""):
        # Apply filtering
        filtered_data = books_data
        if filter_genre:
            filtered_data = filtered_data[filtered_data['Genre'] == filter_genre]
        if filter_availability:
            filtered_data = filtered_data[filtered_data['Available'] == filter_availability]
        if search_query:
            filtered_data = filtered_data[filtered_data['Title'].str.contains(search_query, case=False, na=False)]
        #clear
        for row in tree.get_children():
            tree.delete(row)
        
        for _, row in filtered_data.iterrows():
            tree.insert("", "end", values=(row['Title'], row['Author'], row['Genre'], row['Available']))

    tabview.add("All Books")
    books_frame = ctk.CTkFrame(tabview.tab("All Books"))
    books_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    books_label = ctk.CTkLabel(books_frame, text="Books List will be displayed here.")
    books_label.pack(pady=20)
    
    search_filter_frame = ctk.CTkFrame(books_frame)
    search_filter_frame.pack(pady=10)

    search_label = ctk.CTkLabel(search_filter_frame, text="Search by Title:")
    search_label.grid(row=0, column=0, padx=10)

    search_entry = ctk.CTkEntry(search_filter_frame, placeholder_text="Enter book title")
    search_entry.grid(row=0, column=1, padx=10)

    genre_label = ctk.CTkLabel(search_filter_frame, text="Filter by Genre:")
    genre_label.grid(row=0, column=2, padx=10)

    genre_options = ["All", *books_data['Genre'].unique()]
    genre_dropdown = ctk.CTkComboBox(search_filter_frame, values=genre_options, state="normal")
    genre_dropdown.set("All")  
    genre_dropdown.grid(row=0, column=3, padx=10)

    availability_label = ctk.CTkLabel(search_filter_frame, text="Filter by Availability:")
    availability_label.grid(row=0, column=4, padx=10)

    availability_options = ["All", "Yes", "No"]
    availability_dropdown = ctk.CTkComboBox(search_filter_frame, values=availability_options, state="normal")
    availability_dropdown.set("All")  
    availability_dropdown.grid(row=0, column=5, padx=10)

    filter_button = ctk.CTkButton(search_filter_frame, text="Search", command=lambda: update_table_view(
        filter_genre=genre_dropdown.get() if genre_dropdown.get() != "All" else None,
        filter_availability=availability_dropdown.get() if availability_dropdown.get() != "All" else None,
        search_query=search_entry.get()
    ))
    filter_button.grid(row=0, column=6, padx=10)

    #Table to display books data
    columns = ("Title", "Author", "Genre", "Availability")
    tree = ttk.Treeview(books_frame, columns=columns, show="headings", height=15)  # Increased height
    tree.pack(fill="both", expand=True, pady=20)
    for col in columns:
        tree.heading(col, text=col)
     #show all Books
    update_table_view()

    
    # All Users Tab
    users_data = pd.read_csv("users.csv")
    def update_users_table_view(search_query=""):
        # Filter users by role 'user'
        filtered_data = users_data[users_data['role'] == 'user']
        if search_query:
            filtered_data = filtered_data[filtered_data['username'].str.contains(search_query, case=False, na=False)]

        for row in tree.get_children():
            tree.delete(row)
        for _, row in filtered_data.iterrows():
            tree.insert("", "end", values=(row['user_id'],row['username'], row['email'], row['role']))
    
    tabview.add("All Users")
    users_frame = ctk.CTkFrame(tabview.tab("All Users"))
    users_frame.pack(fill="both", expand=True, padx=20, pady=20)

    users_label = ctk.CTkLabel(users_frame, text="Users List will be displayed here.")
    users_label.pack(pady=20)

    search_label = ctk.CTkLabel(users_frame, text="Search by Username:")
    search_label.pack(pady=10)

    search_entry = ctk.CTkEntry(users_frame, placeholder_text="Enter username")
    search_entry.pack(pady=10)
    
    search_button = ctk.CTkButton(users_frame, text="Search", command=lambda: update_users_table_view(search_query=search_entry.get()))
    search_button.pack(pady=10)

    columns = ("User_ID","Username", "Email", "Role")
    tree = ttk.Treeview(users_frame, columns=columns, show="headings")
    tree.pack(fill="both", expand=True, pady=20)

    for col in columns:
        tree.heading(col, text=col)
        
    update_users_table_view()

    # All Loans Tab
    loans_data = pd.read_csv('loans.csv')
    def update_loans_table_view(search_query=""):
        try:
            loans_data = pd.read_csv("loans.csv")
        except FileNotFoundError:
            messagebox.showerror("Error", "The 'loans.csv' file does not exist.")
            return
        
        if search_query:
            filtered_data = loans_data[loans_data['book_title'].str.contains(search_query, case=False, na=False) |
                                        loans_data['user_name'].str.contains(search_query, case=False, na=False)]
        else:
            filtered_data = loans_data

        for row in tree.get_children():
            tree.delete(row)

        for _, row in filtered_data.iterrows():
            tree.insert("", "end", values=(row['loan_id'], row['book_title'], row['user_name'], row['loan_date'], row['return_date'], row['status']))

    tabview.add("All Loans")
    loans_frame = ctk.CTkFrame(tabview.tab("All Loans"))
    loans_frame.pack(fill="both", expand=True, padx=20, pady=20)

    loans_label = ctk.CTkLabel(loans_frame, text="Loans List will be displayed here.")
    loans_label.pack(pady=20)

    search_label = ctk.CTkLabel(loans_frame, text="Search by Book Title or User:")
    search_label.pack(pady=10)

    search_entry = ctk.CTkEntry(loans_frame, placeholder_text="Enter book title or username")
    search_entry.pack(pady=10)

    search_button = ctk.CTkButton(loans_frame, text="Search", command=lambda: update_loans_table_view(search_query=search_entry.get()))
    search_button.pack(pady=10)

    columns = ("Loan ID", "Book Title", "User Name", "Loan Date", "Return Date", "Status")
    tree = ttk.Treeview(loans_frame, columns=columns, show="headings")
    tree.pack(fill="both", expand=True, pady=20)

    for col in columns:
        tree.heading(col, text=col)
        
    update_loans_table_view()
    employee_window.mainloop()
create_employee_window('habiba')
