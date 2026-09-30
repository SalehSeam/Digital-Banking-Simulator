"""
app.py
-------
Entry point of the Digital Banking Simulator.

Run this file to start the app:
    python app.py

This file sets up the main Tkinter window and switches between
screens (frames): Login -> Register / Dashboard -> Transactions / Profile.

IMPORTANT: This is a SIMULATED educational project. It does not
connect to any real bank, payment gateway, or financial institution.
"""

import tkinter as tk

from database import initialize_database
from gui import theme
from gui.login import LoginFrame
from gui.register import RegisterFrame
from gui.dashboard import DashboardFrame
from gui.transactions import TransactionsFrame
from gui.profile import ProfileFrame


class DigitalBankingApp(tk.Tk):
    """
    Main application window (controller).
    Keeps track of which screen is showing and who is currently logged in.
    """

    def __init__(self):
        super().__init__()

        self.title("Digital Banking Simulator")
        self.geometry("800x600")
        self.minsize(700, 550)
        self.configure(bg=theme.BG_DARK)

        # Holds the account number of the currently logged-in user (or None).
        self.current_account = None

        # A container frame that all screens are stacked into.
        container = tk.Frame(self, bg=theme.BG_DARK)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create every screen once and keep them ready in memory.
        self.frames = {}
        for FrameClass in (LoginFrame, RegisterFrame, DashboardFrame, TransactionsFrame, ProfileFrame):
            frame_name = FrameClass.__name__
            frame = FrameClass(parent=container, controller=self)
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginFrame")

    def show_frame(self, frame_name: str):
        """Raise the requested screen to the top and refresh its data."""
        frame = self.frames[frame_name]
        frame.tkraise()
        # If the screen defines an on_show() refresh method, call it.
        if hasattr(frame, "on_show"):
            frame.on_show()

    def log_in(self, account_number: str):
        """Called by the login screen after a successful login."""
        self.current_account = account_number
        self.show_frame("DashboardFrame")

    def log_out(self):
        """Called by the dashboard when the user logs out."""
        self.current_account = None
        self.show_frame("LoginFrame")


def main():
    # Make sure the database and its tables exist before the GUI opens.
    initialize_database()

    app = DigitalBankingApp()
    app.mainloop()


if __name__ == "__main__":
    main()
