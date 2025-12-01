import customtkinter as ctk
import tkinter as tk
from ui.base_page import BasePage
import subprocess
import sys
import threading
import queue


class CodeEditor(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        # Layout grid setup
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        # Code Text widget
        self.code_text = ctk.CTkTextbox(self.content, width=80, height=20, font=("Consolas", 14))
        self.code_text.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Run button
        self.run_button = ctk.CTkButton(self.content, text="Run Code", command=self.run_code)
        self.run_button.grid(row=1, column=0, sticky="e", padx=10, pady=(0,10))

        # Output area
        self.output_text = ctk.CTkTextbox(self.content, height=10, font=("Consolas", 12), state="disabled")
        self.output_text.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0,10))

        self.content.grid_rowconfigure(2, weight=0)

        # Queue to handle threading output
        self.output_queue = queue.Queue()

    def run_code(self):
        """Run the code in a separate thread to avoid freezing the UI."""
        code = self.code_text.get("1.0", "end-1c")

        # Clear previous output
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.configure(state="disabled")

        # Start thread to run code
        thread = threading.Thread(target=self.execute_code, args=(code,))
        thread.start()

        # Check thread output periodically
        self.after(100, self.process_queue)

    def execute_code(self, code):
        """Execute Python code safely and capture output."""
        import io
        import contextlib

        output = io.StringIO()
        error = None

        try:
            with contextlib.redirect_stdout(output):
                with contextlib.redirect_stderr(output):
                    exec(code, {})
        except Exception as e:
            error = str(e)

        self.output_queue.put((output.getvalue(), error))

    def process_queue(self):
        """Process the output queue to display output/errors."""
        try:
            output, error = self.output_queue.get_nowait()
        except queue.Empty:
            self.after(100, self.process_queue)
            return

        self.output_text.configure(state="normal")
        if error:
            self.output_text.insert(tk.END, f"Error:\n{error}")
        else:
            self.output_text.insert(tk.END, output)
        self.output_text.configure(state="disabled")
