import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Load the CSV files
books = pd.read_csv("books.csv")
loans = pd.read_csv("loans.csv")
transactions = pd.read_csv("transactions.csv")

def books_loaned_per_user():
    user_loans = loans.groupby('user_name').size().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    user_loans.plot(kind='bar', color='lightcoral', ax=ax)
    ax.set_title('Books Loaned per User')
    ax.set_xlabel('User')
    ax.set_ylabel('Number of Books Loaned')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    plt.tight_layout()
    return fig


def transaction_insights():
    transaction_types = transactions['Transaction_Type'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 6))
    transaction_types.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=['gold', 'lightcoral'], ax=ax)
    ax.set_title("Transaction Distribution")
    plt.tight_layout()
    return fig

def genre_distribution():
    genre_counts = books['Genre'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(genre_counts, labels=genre_counts.index, autopct='%1.1f%%', startangle=90)
    ax.set_title('Book Genre Distribution')
    ax.axis('equal')
    return fig

#Books per author
def books_per_author():
    author_counts = books['Author'].value_counts()
    fig, ax = plt.subplots(figsize=(10, 6))
    author_counts.plot(kind='bar', color='lightblue', ax=ax)
    ax.set_title('Books per Author')
    ax.set_xlabel('Author')
    ax.set_ylabel('Number of Books')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    plt.tight_layout()
    return fig

def loan_status_distribution():
    loan_status_counts = loans['status'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 6))
    loan_status_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=['skyblue', 'lightgreen'], ax=ax)
    ax.set_title('Loan Status Distribution')
    plt.tight_layout()
    return fig

def book_popularity():
    purchase_counts = transactions.groupby('Book_Title').size().reset_index(name='Transaction_Count')
    loan_counts = loans.groupby('book_title').size().reset_index(name='Loan_Count')
    popularity = pd.merge(purchase_counts, loan_counts, left_on='Book_Title', right_on='book_title', how='outer')
   
    popularity['Total_Popularity'] = popularity['Transaction_Count'] + popularity['Loan_Count']
    popularity = popularity.sort_values(by='Total_Popularity', ascending=False).head(10)

    # Create a bar chart to show the most popular books
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='Total_Popularity', y='Book_Title', data=popularity, palette='viridis', ax=ax)
    ax.set_title('Top 10 Most Popular Books (Based on Transactions and Loans)')
    ax.set_xlabel('Total Popularity (Transactions + Loans)')
    ax.set_ylabel('Book Title')
    plt.tight_layout()

    return fig

    

def display_plot_on_tab(tab_frame, plot_func):
    fig = plot_func()
    
    # Embed the plot into tkinter using FigureCanvasTkAgg
    canvas = FigureCanvasTkAgg(fig, master=tab_frame)  
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)