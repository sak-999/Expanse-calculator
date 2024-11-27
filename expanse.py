import tkinter as tk
from tkinter import messagebox
import pandas as pd
from datetime import datetime
# File where expenses are saved
filename = "expenses.csv"
# Load existing data or create a new DataFrame if the file doesn't exist
try:
    expenses_df = pd.read_csv(filename)
except FileNotFoundError:
    expenses_df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
# Save data to CSV
def save_data():
    expenses_df.to_csv(filename, index=False)
# Add an expense
def add_expense():
    date = entry_date.get()
    category = entry_category.get()
    amount = entry_amount.get()
    description = entry_description.get()
    if not (date and category and amount and description):
        messagebox.showwarning("Warning", "All fields must be filled out.")
        return
    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number.")
        return
    global expenses_df
    new_data = pd.DataFrame([[date, category, amount, description]], columns=["Date", "Category", "Amount", "Description"])
    expenses_df = pd.concat([expenses_df, new_data], ignore_index=True)
    save_data()
    clear_entries()
    show_expenses()
    messagebox.showinfo("Success", "Expense added successfully!")
# Delete selected expense
def delete_expense():
    selected_item = listbox_expenses.curselection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select an expense to delete.")
        return
    
    global expenses_df
    expenses_df = expenses_df.drop(selected_item[0]).reset_index(drop=True)
    save_data()
    show_expenses()
    messagebox.showinfo("Success", "Expense deleted successfully!")
# Display expenses in the listbox
def show_expenses():
    listbox_expenses.delete(0, tk.END)
    for index, row in expenses_df.iterrows():
        expense_info = f"{row['Date']} - {row['Category']} - ₹{row['Amount']:.2f} - {row['Description']}"
        listbox_expenses.insert(tk.END, expense_info)
# Clear entry fields
def clear_entries():
    entry_date.delete(0, tk.END)
    entry_category.delete(0, tk.END)
    entry_amount.delete(0, tk.END)
    entry_description.delete(0, tk.END)
# Set default date to today
def set_today_date():
    entry_date.delete(0, tk.END)
    entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
# GUI Setup
app = tk.Tk()
app.title("Expense Tracker")
app.geometry("600x400")
app.config(bg="lightgray")
# Labels and Entries for Input
tk.Label(app, text="Date (YYYY-MM-DD):", bg="lightgray").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_date = tk.Entry(app, width=30)
entry_date.grid(row=0, column=1, padx=10, pady=5)
set_today_date()  # Set date to today's date by default
tk.Label(app, text="Category:", bg="lightgray").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_category = tk.Entry(app, width=30)
entry_category.grid(row=1, column=1, padx=10, pady=5)
tk.Label(app, text="Amount:", bg="lightgray").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_amount = tk.Entry(app, width=30)
entry_amount.grid(row=2, column=1, padx=10, pady=5)
tk.Label(app, text="Description:", bg="lightgray").grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_description = tk.Entry(app, width=30)
entry_description.grid(row=3, column=1, padx=10, pady=5)
# Buttons for Adding and Deleting Expenses
tk.Button(app, text="Add Expense", command=add_expense, bg="blue", fg="white", width=15).grid(row=4, column=0, padx=10, pady=10)
tk.Button(app, text="Delete Expense", command=delete_expense, bg="red", fg="white", width=15).grid(row=4, column=1, padx=10, pady=10)
# Listbox to Display Expenses
listbox_expenses = tk.Listbox(app, width=80, height=10)
listbox_expenses.grid(row=5, column=0, columnspan=3, padx=10, pady=10)
# Populate the listbox with expenses on startup
show_expenses()
# Run the Application
app.mainloop()
