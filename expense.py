import tkinter as tk
from tkinter import ttk
import csv
from datetime import datetime

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.configure(bg="gray")

        # Initialize variables
        self.expenses = []

        # Create UI elements
        self.label_title = tk.Label(root, text="Expense Tracker", font=("Helvetica", 16), fg="black", bg="gray")
        self.label_title.grid(row=0, column=0, columnspan=4, pady=10)

        self.label_amount = tk.Label(root, text="Amount:", fg="black", bg="gray")
        self.label_amount.grid(row=1, column=0, padx=10)

        self.entry_amount = tk.Entry(root)
        self.entry_amount.grid(row=1, column=1, padx=10)

        self.label_category = tk.Label(root, text="Category:", fg="black", bg="gray")
        self.label_category.grid(row=1, column=2, padx=10)

        self.combobox_category = ttk.Combobox(root, values=["Food", "Transportation", "Entertainment"])
        self.combobox_category.grid(row=1, column=3, padx=10)

        self.label_description = tk.Label(root, text="Description:", fg="black", bg="gray")
        self.label_description.grid(row=2, column=0, padx=10)

        self.entry_description = tk.Entry(root, width=30)
        self.entry_description.grid(row=2, column=1, columnspan=3, padx=10, pady=5, sticky="ew")

        self.btn_add_expense = tk.Button(root, text="Add Expense", command=self.add_expense, bg="black", fg="white")
        self.btn_add_expense.grid(row=3, column=0, columnspan=4, pady=10)

        self.tree = ttk.Treeview(root, columns=("Amount", "Category", "Description", "Date"), show="headings")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Date", text="Date")
        self.tree.grid(row=4, column=0, columnspan=4, pady=10)

        self.btn_delete = tk.Button(root, text="Delete Selected", command=self.delete_selected, bg="black", fg="white")
        self.btn_delete.grid(row=5, column=0, columnspan=4, pady=10)

        # Load expenses from CSV
        self.load_expenses()

    def add_expense(self):
        amount = self.entry_amount.get()
        category = self.combobox_category.get()
        description = self.entry_description.get()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if amount and category and description:
            self.expenses.append((amount, category, description, date))
            self.save_expenses_to_csv()
            self.update_treeview()
            self.entry_amount.delete(0, tk.END)
            self.combobox_category.set("")
            self.entry_description.delete(0, tk.END)

    def delete_selected(self):
        selected_item = self.tree.selection()[0]
        self.tree.delete(selected_item)
        index = int(selected_item[1:]) - 1
        del self.expenses[index]
        self.save_expenses_to_csv()

    def load_expenses(self):
        try:
            with open("Expense Tracker/expenses.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    self.expenses.append((row[0], row[1], row[2], row[3]))
            self.update_treeview()
        except FileNotFoundError:
            pass

    def save_expenses_to_csv(self):
        with open("Expense Tracker/expenses.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(self.expenses)

    def update_treeview(self):
        self.tree.delete(*self.tree.get_children())
        for idx, (amount, category, description, date) in enumerate(self.expenses, start=1):
            self.tree.insert("", "end", values=(amount, category, description, date))

def main():
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()