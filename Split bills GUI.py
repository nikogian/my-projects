import tkinter as tk
from tkinter import messagebox
import numpy as np


#sorting dict func
def sort(k,v):
    sorted_value_index = np.argsort(v)
    desc_value_index = sorted_value_index[::-1]
    keys_list = list(k[i] for i in desc_value_index)
    values_list = list(round(v[i],2) for i in desc_value_index)
    #sorted_dictonary = {k[i]:v[i] for i in desc_value_index}
    return keys_list,values_list



class UserInputWindow:
    def __init__(self, master):
        self.master = master
        self.master.title('User Input')
        self.master.geometry('520x500')
        self.master.tk.call('tk','scaling', 1.5)

        font_size = 18
        label_font = ('Helvetica', font_size)
        entry_font = ('Helvetica', font_size)

        self.label = tk.Label(master, text='Enter username:', font = label_font)
        self.label.grid(column=2,row=0)
        #pad is for the space
        
        self.username_entry = tk.Entry(master, font = entry_font)
        self.username_entry.grid(column=2,row=1)
        #sticky is to expand
        
        self.new_user_button = tk.Button(master, text='Add User', command=self.add_new_user)
        self.new_user_button.grid(column=1,row=2)

        self.next_button = tk.Button(master, text='Continue', command=self.continue_code)
        self.next_button.grid(column=3,row=2)

        
        self.usernames = []

    def add_new_user(self):
        try:
            username = self.username_entry.get()
            self.username_entry.delete(0, tk.END)
            if username in self.usernames:
                raise ValueError    
            else:
                self.usernames.append(username)
        except:
            messagebox.showerror('Error','Username already exists')

    def continue_code(self):
        messagebox.showinfo('Usernames', self.usernames)
        
        self.label.grid_forget()
        self.username_entry.grid_forget()
        self.new_user_button.grid_forget()
        self.next_button.grid_forget()

        user_payments_app = UserPayments(self.master, self.usernames)



class UserPayments():
    def __init__(self, master, usernames):
        self.master = master
        self.master.title('User Payments')
        self.usernames = usernames

        self.usernames_listbox = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=False, font=('Helvetica', 16))
        for username in self.usernames:
            self.usernames_listbox.insert(tk.END, username)
        self.usernames_listbox.grid(column=1, row=3, pady=20, sticky='ew')

        self.payment_label = tk.Label(master, text='Enter payment:', font=('Helvetica', 16))
        self.payment_label.grid(column=0, row=4, pady=20, sticky='e')

        self.payment_entry = tk.Entry(master, font=('Helvetica', 16))
        self.payment_entry.grid(column=1, row=4, pady=20, sticky='ew')

        self.add_payment_button = tk.Button(master, text='Add Payment', command=self.add_payment)
        self.add_payment_button.grid(column=0, row=5, pady=20)

        self.finish_button = tk.Button(master, text='Settle depts', command=self.finish_code)
        self.finish_button.grid(column=2, row=5, pady=20)

        self.payments = {}
        for u in self.usernames:
            self.payments[u] = 0


    def add_payment(self):
        selected_index = self.usernames_listbox.curselection()
        
        if selected_index:
            username = self.usernames_listbox.get(selected_index)
            payment = self.payment_entry.get()
            try:
                payment = float(payment)
                if username in self.payments:
                    self.payments[username] += payment
                

                self.payment_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror('Error', 'Invalid payment value. Please enter a number.')
        else:
            messagebox.showerror('Error', 'Please select a username.')


    def finish_code(self):
        messagebox.showinfo('Payments', self.payments)
        payments_total = sum(self.payments.values())
        users_count = len(self.usernames)
        user_part = payments_total / users_count
        messagebox.showinfo("Each user's part", user_part)

        dept_dict = {}
        for y in self.usernames:
            dept_dict.update({y:0})

        for user_dept in dept_dict.keys():
            dept_dict[user_dept] = self.payments[user_dept] - user_part
        
        #sort dictionary
        keys = list(dept_dict.keys())
        values = list(dept_dict.values())
        sorted_keys_list,sorted_values_list = sort(keys,values)

        #settle depts
        final_message = []
        try:
            while sorted_values_list[0] > 0:
                if sorted_values_list[0] < 0.01:
                    sorted_values_list *= -1
                
                final_message.append(f'User {sorted_keys_list[-1]} owes user {sorted_keys_list[0]}: {round(-1*sorted_values_list[-1],2)} Euro')
                
                sorted_values_list[0] += sorted_values_list[-1]
                sorted_keys_list.pop()
                sorted_values_list.pop()
            
                sorted_keys_list,sorted_values_list = sort(sorted_keys_list,sorted_values_list)
        except IndexError:
            final_message.pop()
        
        messagebox.showinfo('Depts', final_message)



if __name__ == '__main__':
    root = tk.Tk()
    app = UserInputWindow(root)
    root.mainloop()
