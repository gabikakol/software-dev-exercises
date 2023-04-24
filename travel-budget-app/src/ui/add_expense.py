from tkinter import ttk, StringVar
from services.expense_service import expense_service
from services.trip_service import trip_service

class AddExpense:
    def __init__(self, root, trip_view):
        self._root = root
        self._window = None
        self.save_handle = trip_view
        self.description_entry = None
        self.amount_entry = None
        self.cat_var = None
        self.start()

    def start(self):
        self._window = ttk.Frame(master=self._root)

        header_label = ttk.Label(master=self._window, text="Add an expense:")
        header_label.grid(padx=5,pady=5)

        description_label = ttk.Label(master=self._window, text="Description:")
        description_label.grid(padx=5,pady=5)

        self.description_entry = ttk.Entry(master=self._window)
        self.description_entry.grid(padx=5,pady=5)

        amount_label = ttk.Label(master=self._window, text="Cost (EUR):")
        amount_label.grid(padx=5,pady=5)

        self.amount_entry = ttk.Entry(master=self._window)
        self.amount_entry.grid(padx=5,pady=5)

        category_label = ttk.Label(master=self._window, text="Category:")
        category_label.grid(padx=5, pady=5)

        categories = ['select an option', 'groceries', 'restaurants', 'cafes', 'bars', 'laundry',
                      'transportation', 'accommodation', 'tickets', 'currency exchange commissions', 'activities', 'other']
        self.cat_var = StringVar(self._root)
        # tkvar.set('Select an option')
        category_menu = ttk.OptionMenu(self._window, self.cat_var, *categories)
        category_menu.grid(padx=5, pady=5)

        save_button = ttk.Button(
            master=self._window, text="Save", command=self.handle_add_expense)
        save_button.grid(padx=5, pady=5)

        self._window.grid_columnconfigure(0, weight=1, minsize=400)

        #description, amount, category

    def pack(self):
        self._window.pack()
        
    def destroy(self):
        self._window.destroy()

    def handle_add_expense(self):
        description = self.description_entry.get()
        amount = self.amount_entry.get()
        category = self.cat_var.get()
        trip_id = "X"
        expense_service.add_expense(description, trip_id, amount, category)
        self.save_handle()