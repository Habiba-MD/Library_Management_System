import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Load the CSV files
books = pd.read_csv("books.csv")
loans = pd.read_csv("loans.csv")
transactions = pd.read_csv("transactions.csv")

loans['loan_date'] = pd.to_datetime(loans['loan_date'], errors='coerce')
loans['return_date'] = pd.to_datetime(loans['return_date'], errors='coerce')
transactions['Date'] = pd.to_datetime(transactions['Date'], errors='coerce')

invalid_loans = loans[loans['loan_date'].isna()]
invalid_transactions = transactions[transactions['Date'].isna()]

print("Invalid loan dates:")
print(invalid_loans)
print("Invalid transaction dates:")
print(invalid_transactions)
loans.dropna(subset=['loan_date', 'return_date'], inplace=True)
transactions.dropna(subset=['Date'], inplace=True)

#Loans Overview
def loans_overview():
    monthly_loans = loans.groupby(loans['loan_date'].dt.to_period('M')).size()
    fig, ax = plt.subplots(figsize=(10, 6))
    monthly_loans.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_title("Monthly Loan Count")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Loans")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    plt.tight_layout()
    return fig

#User Behavior
def user_behavior():
    user_loans = loans.groupby('user_name').size().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 6))
    user_loans.plot(kind='bar', color='lightgreen', ax=ax)
    ax.set_title("Number of Loans Per User")
    ax.set_xlabel("User")
    ax.set_ylabel("Loan Count")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    plt.tight_layout()
    return fig


#Book Popularity (Best-seller per Month)
def book_popularity():
    transactions['Date'] = pd.to_datetime(transactions['Date'])
    purchase_transactions = transactions[transactions['Transaction_Type'] == 'Purchase']
    purchase_transactions['Month'] = purchase_transactions['Date'].dt.to_period('M')
    monthly_book_sales = purchase_transactions.groupby(['Month', 'Book_Title']).size().reset_index(name='Sales')
    best_sellers = monthly_book_sales.loc[monthly_book_sales.groupby('Month')['Sales'].idxmax()]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='Month', y='Sales', hue='Book_Title', data=best_sellers, palette='coolwarm', ax=ax)
    ax.set_title("Best-Selling Books by Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Sales")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    plt.tight_layout()
    return fig


# Transaction Insights
def transaction_insights():
    transaction_types = transactions['Transaction_Type'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 6))
    transaction_types.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=['gold', 'lightcoral'], ax=ax)
    ax.set_title("Transaction Distribution")
    plt.tight_layout()
    return fig

# Fines and Overdue Books
def fines_and_overdue_books():
    overdue_loans = loans[loans['fine'] > 0]
    overdue_books = overdue_loans['user_name'].value_counts()
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=overdue_books.index, y=overdue_books.values, palette='mako', ax=ax)
    ax.set_title("Users with Fines (Overdue Books)")
    ax.set_xlabel("Username")
    ax.set_ylabel("Fine Count")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    plt.tight_layout()
    return fig

def display_plot_on_tab(tab_frame, plot_func):
    fig = plot_func()
    
    # Embed the plot into tkinter using FigureCanvasTkAgg
    canvas = FigureCanvasTkAgg(fig, master=tab_frame)  
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)