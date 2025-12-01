from ui.base_page import BasePage
import customtkinter as ctk


class HomePage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        # HOME PAGE CONTENT
        label = ctk.CTkLabel(
            self.content,
            text="Welcome to the Programming Tutor App!",
            font=("Arial", 28, "bold")
        )
        label.pack(pady=40)

        desc = ctk.CTkLabel(
            self.content,
            text="Learn programming offline with lessons, quizzes, challenges,\nand a built-in code editor.",
            font=("Arial", 18),
            justify="center"
        )
        desc.pack(pady=20)
