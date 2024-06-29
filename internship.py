import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class InternshipTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Internship Tracker")
        
        self.conn = sqlite3.connect('internship_tracker.db')
        self.c = self.conn.cursor()
        
        self.create_table()
        
        self.apply_dark_mode()
        
        self.company_frame = ttk.LabelFrame(root, text="Internship company", padding=(10, 5))
        self.company_frame.grid(row=0, column=0, padx=(11, 10), pady=(10, 5), sticky="nsew")  

        self.company_name_label = ttk.Label(self.company_frame, text="Company Name:")
        self.company_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.company_name_entry = ttk.Entry(self.company_frame, width=30)
        self.company_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.checkboxes_frame = ttk.LabelFrame(root, text="Internship details", padding=(10, 5))
        self.checkboxes_frame.grid(row=1, column=0, padx=(11, 10), pady=(0, 5), sticky="nsew")  

        self.email_sent = tk.IntVar()
        self.email_received_positive = tk.IntVar()
        self.email_received_negative = tk.IntVar()
        self.conversation_round = tk.IntVar()
        self.internship_test = tk.IntVar()
        self.approved = tk.IntVar()
        self.contract_signed = tk.IntVar()

        self.create_checkbox("Email Sent", self.email_sent, 0, 0)
        self.create_checkbox("Email Received (Positive)", self.email_received_positive, 0, 1)
        self.create_checkbox("Email Received (Negative)", self.email_received_negative, 0, 2)
        self.create_checkbox("Conversation Round", self.conversation_round, 1, 0)
        self.create_checkbox("Internship Test", self.internship_test, 1, 1)
        self.create_checkbox("Approved", self.approved, 1, 2)
        self.create_checkbox("Contract Signed", self.contract_signed, 1, 3)

        self.buttons_frame = ttk.LabelFrame(root, text="CRUD", padding=(10, 5))
        self.buttons_frame.grid(row=2, column=0, padx=(11, 10), pady=(0, 5), sticky="nsew")  

        self.add_button = ttk.Button(self.buttons_frame, text="Add Company", command=self.add_company)
        self.add_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.edit_button = ttk.Button(self.buttons_frame, text="Edit Selected Company", command=self.edit_company)
        self.edit_button.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.delete_button = ttk.Button(self.buttons_frame, text="Delete Selected Company", command=self.delete_company)
        self.delete_button.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        self.apply_button = ttk.Button(self.buttons_frame, text="Apply Edit", command=self.apply_edit)
        self.apply_button.grid(row=0, column=3, padx=5, pady=5, sticky="w")


        self.tree_frame = ttk.LabelFrame(root, text="Company List", padding=(10, 5))
        self.tree_frame.grid(row=3, column=0, padx=(11, 10), pady=(0, 10), sticky="nsew")  

        self.tree = ttk.Treeview(self.tree_frame, columns=('Name', 'Email Sent', 'Positive', 'Negative', 'Conversation', 'Test', 'Approved', 'Contract'), show='headings')
        self.tree.heading('Name', text='Company Name')
        self.tree.heading('Email Sent', text='Email Sent')
        self.tree.heading('Positive', text='Email Received Positive')
        self.tree.heading('Negative', text='Email Received Negative')
        self.tree.heading('Conversation', text='Conversation Round')
        self.tree.heading('Test', text='Internship Test')
        self.tree.heading('Approved', text='Approved')
        self.tree.heading('Contract', text='Contract Signed')
        self.tree.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.load_data()
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(3, weight=1)

    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS companies
                     (name TEXT PRIMARY KEY,
                      email_sent INTEGER,
                      positive_received INTEGER,
                      negative_received INTEGER,
                      conversation_round INTEGER,
                      internship_test INTEGER,
                      approved INTEGER,
                      contract_signed INTEGER)''')
        self.conn.commit()

    def create_checkbox(self, text, variable, row, col):
        checkbox = ttk.Checkbutton(self.checkboxes_frame, text=text, variable=variable)
        checkbox.grid(row=row, column=col, padx=5, pady=5, sticky="w")

    def add_company(self):
        company_name = self.company_name_entry.get()
        if company_name:
            self.c.execute('''INSERT INTO companies (name, email_sent, positive_received, negative_received,
                                                    conversation_round, internship_test, approved, contract_signed)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                           (company_name,
                            1 if self.email_sent.get() else 0,
                            1 if self.email_received_positive.get() else 0,
                            1 if self.email_received_negative.get() else 0,
                            1 if self.conversation_round.get() else 0,
                            1 if self.internship_test.get() else 0,
                            1 if self.approved.get() else 0,
                            1 if self.contract_signed.get() else 0))
            self.conn.commit()
            self.load_data() 
            self.clear_fields()
        else:
            messagebox.showwarning("Input Error", "Please enter a company name.")

    def edit_company(self):
        selected_item = self.tree.focus() 
        if selected_item:
            current_values = self.tree.item(selected_item, "values")
            if current_values:
                self.company_name_entry.delete(0, tk.END)
                self.company_name_entry.insert(0, current_values[0])  
                self.email_sent.set(int(current_values[1] == "Yes"))
                self.email_received_positive.set(int(current_values[2] == "Yes"))
                self.email_received_negative.set(int(current_values[3] == "Yes"))
                self.conversation_round.set(int(current_values[4] == "Yes"))
                self.internship_test.set(int(current_values[5] == "Yes"))
                self.approved.set(int(current_values[6] == "Yes"))
                self.contract_signed.set(int(current_values[7] == "Yes"))
            else:
                messagebox.showwarning("Data Error", "No data found for selected company.")
        else:
            messagebox.showwarning("Selection Error", "Please select a company to edit.")

    def delete_company(self):
        selected_item = self.tree.selection()
        if selected_item:
            company_name = self.tree.item(selected_item, "values")[0]
            self.c.execute("DELETE FROM companies WHERE name=?", (company_name,))
            self.conn.commit()
            self.load_data()
        else:
            messagebox.showwarning("Selection Error", "Please select a company to delete.")

    def clear_fields(self):
        self.company_name_entry.delete(0, tk.END)
        self.email_sent.set(0)
        self.email_received_positive.set(0)
        self.email_received_negative.set(0)
        self.conversation_round.set(0)
        self.internship_test.set(0)
        self.approved.set(0)
        self.contract_signed.set(0)

    def apply_edit(self):
        selected_item = self.tree.selection()
        if selected_item:
            company_name = self.company_name_entry.get()
            if company_name:
                self.c.execute('''UPDATE companies SET name=?, email_sent=?, positive_received=?, negative_received=?,
                                                 conversation_round=?, internship_test=?, approved=?, contract_signed=?
                                  WHERE name=?''',
                               (company_name,
                                1 if self.email_sent.get() else 0,
                                1 if self.email_received_positive.get() else 0,
                                1 if self.email_received_negative.get() else 0,
                                1 if self.conversation_round.get() else 0,
                                1 if self.internship_test.get() else 0,
                                 1 if self.approved.get() else 0,
                                1 if self.contract_signed.get() else 0,
                                self.tree.item(selected_item, "values")[0])) 
                self.conn.commit()
                self.load_data() 
                self.clear_fields()
            else:
                messagebox.showwarning("Input Error", "Please enter a company name.")
        else:
            messagebox.showwarning("Selection Error", "Please select a company to apply edits.")

    def load_data(self):
        self.tree.delete(*self.tree.get_children()) 
        self.c.execute("SELECT * FROM companies")
        rows = self.c.fetchall()
        for row in rows:
            data = (row[0], "Yes" if row[1] == 1 else "No", "Yes" if row[2] == 1 else "No",
                    "Yes" if row[3] == 1 else "No", "Yes" if row[4] == 1 else "No",
                    "Yes" if row[5] == 1 else "No", "Yes" if row[6] == 1 else "No",
                    "Yes" if row[7] == 1 else "No")
            self.tree.insert('', 'end', values=data)

    def apply_dark_mode(self):
        style = ttk.Style()
        self.root.tk_setPalette(background="#2E2E2E", foreground="#FFFFFF", activeBackground="#3E3E3E", activeForeground="#FFFFFF")
        style.theme_use("clam")
        style.configure("TLabel", background="#2E2E2E", foreground="#FFFFFF")
        style.configure("TEntry", background="#3E3E3E", foreground="#000000")
        style.configure("TButton", background="#3E3E3E", foreground="#FFFFFF")
        style.configure("TCheckbutton", background="#2E2E2E", foreground="#FFFFFF")
        style.configure("Treeview", background="#3E3E3E", foreground="#FFFFFF", fieldbackground="#3E3E3E")
        style.configure("Treeview.Heading", background="#2E2E2E", foreground="#FFFFFF")

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = InternshipTrackerApp(root)
    root.mainloop()
