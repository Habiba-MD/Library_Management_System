import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

books_data = pd.read_csv("books.csv")
loans_data = pd.read_csv("loans.csv")

# Borrowed vs On Shelves Pie Chart
def create_available_pie_chart(frame):
    available_books = books_data[books_data['Available'] == 'Yes']
    borrowed_books = books_data[books_data['Available'] == 'No']

    labels = ['On Shelves', 'Borrowed']
    sizes = [len(available_books), len(borrowed_books)]

    fig, ax = plt.subplots(figsize=(2, 2))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff'])
    ax.axis('equal')  
    ax.set_facecolor("#F2F9FF")

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

# Genre Distribution Pie Chart
def create_genre_pie_chart(frame):
    genre_counts = books_data['Genre'].value_counts()

    fig, ax = plt.subplots(figsize=(2, 2))
    wedges, texts, autotexts = ax.pie(
        genre_counts.values,
        labels=genre_counts.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=plt.cm.tab20.colors
    )
    ax.axis('equal')  
    ax.set_title('Books by Genre')
    ax.set_facecolor("#F2F9FF")

    
    for text in texts:
        text.set_fontsize(10)
    for autotext in autotexts:
        autotext.set_fontsize(8)

    
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
