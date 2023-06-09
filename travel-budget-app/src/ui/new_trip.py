from tkinter import ttk, StringVar, constants
from services.trip_service import trip_service
from services.user_service import user_service
from errors.errors_handling import EmptyInputError, NotIntegerError
import datetime


class NewTrip:
    """Class for creating a new trip ui."""

    def __init__(self, root, trips_list):
        """
        Class contructor.

        Args:
            root: tkinter root
            trips_list: trips list view window
        """

        self._root = root
        self.trips_list_handle = trips_list
        self._window = None
        self.name_entry = None
        self.duration_entry = None
        self.error_variable = None
        self.error_label = None
        self.current_time = datetime.datetime.now()

        self.start()

    def start(self):
        self._window = ttk.Frame(master=self._root)
        style = ttk.Style()

        current_date_label = ttk.Label(master=self._window, text=self.current_time.strftime(
            '%H:%M, %A, %dth %B %Y'), foreground="#5A5A5A", font=('consolas', 10))
        current_date_label.grid(padx=5, pady=5, column=1)

        header_label = ttk.Label(
            master=self._window, text="CREATE A NEW TRIP", font=('consolas', 15, "bold"))
        header_label.grid(padx=5, pady=5, column=1)

        name_label = ttk.Label(master=self._window,
                               text="Name:", font=('consolas', 10, "bold"))
        name_label.grid(padx=5, pady=5, column=1)
        self.name_entry = ttk.Entry(master=self._window)
        self.name_entry.grid(padx=5, pady=5, column=1, sticky=constants.EW)

        duration_label = ttk.Label(
            master=self._window, text="Duration (days):", font=('consolas', 10, "bold"))
        duration_label.grid(padx=5, pady=5, column=1)
        self.duration_entry = ttk.Entry(master=self._window)
        self.duration_entry.grid(padx=5, pady=5, column=1, sticky=constants.EW)

        self.error_variable = StringVar(self._window)
        self.error_label = ttk.Label(
            master=self._window, textvariable=self.error_variable, foreground="red", font=('consolas', 10, "bold"))
        self.error_label.grid(padx=5, pady=5, column=1)

        save_button = ttk.Button(
            master=self._window, text="Save", command=self.handle_new_trip, style="save.TButton")
        save_button.grid(padx=5, pady=5, column=1, sticky=constants.EW)
        style.configure("save.TButton", font=('consolas', 10),
                        background="#5A5A5A", foreground="white")

        cancel_button = ttk.Button(
            master=self._window, text="Cancel", command=self.trips_list_handle, style="cancel.TButton")
        cancel_button.grid(padx=5, pady=5, column=1, sticky=constants.EW)
        style.configure("cancel.TButton", font=('consolas', 10),
                        background="#5A5A5A", foreground="white")

        self.hide_error()

        self._window.grid_columnconfigure(0, minsize=190)
        self._window.grid_columnconfigure(1, minsize=330)

    def pack(self):
        """Diplays the current view."""
        self._window.pack(fill=constants.X)

    def destroy(self):
        """Resets the current view."""
        self._window.destroy()

    def handle_new_trip(self):
        username = user_service.get_username()
        trip_name = self.name_entry.get()
        duration = self.duration_entry.get()

        self.hide_error()

        try:
            trip_service.new_trip(trip_name, username, duration)
            self.trips_list_handle()
        except EmptyInputError:
            self.show_error("Trip name and duration cannot be empty.")
        except NotIntegerError:
            self.show_error("Trip duration must be an integer.")

    def show_error(self, text):
        self.error_variable.set(text)
        self.error_label.grid()

    def hide_error(self):
        self.error_label.grid_remove()
