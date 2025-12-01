import customtkinter as ctk
from ui.base_page import BasePage
import json
import os


class QuizPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        # Quiz state
        self.questions = []
        self.current_question_index = 0
        self.score = 0

        # Layout
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=1)

        # Question label
        self.question_label = ctk.CTkLabel(
            self.content, text="", font=("Arial", 20), wraplength=900, justify="left"
        )
        self.question_label.grid(row=0, column=0, pady=(10, 20), sticky="w")

        # Variable for selected answer
        self.selected_answer = ctk.StringVar(value="")

        # Frame for radio buttons
        self.options_frame = ctk.CTkFrame(self.content)
        self.options_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 20))

        # Submit button
        self.submit_btn = ctk.CTkButton(
            self.content, text="Submit Answer", command=self.submit_answer
        )
        self.submit_btn.grid(row=2, column=0, sticky="e")

        # Load questions from JSON
        self.load_questions()

        # Display the first question
        if self.questions:
            self.show_question(0)
        else:
            self.question_label.configure(text="No quiz questions available.")

    def load_questions(self):
        """Load quiz questions from JSON file."""
        quiz_file = os.path.join(os.path.dirname(__file__), "..", "challenges", "quiz_questions.json")
        if not os.path.exists(quiz_file):
            print("Quiz questions file not found:", quiz_file)
            return

        with open(quiz_file, "r", encoding="utf-8") as f:
            try:
                self.questions = json.load(f)
            except json.JSONDecodeError:
                print("Error decoding quiz questions JSON.")

    def show_question(self, index):
        """Display question and options for the given index."""
        self.current_question_index = index
        question_data = self.questions[index]

        self.question_label.configure(text=f"Q{index + 1}: {question_data['question']}")

        # Clear previous options
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        self.selected_answer.set("")  # Reset selection

        # Create radio buttons for options
        for option in question_data["options"]:
            rbtn = ctk.CTkRadioButton(
                self.options_frame,
                text=option,
                variable=self.selected_answer,
                value=option
            )
            rbtn.pack(anchor="w", pady=5)

    def submit_answer(self):
        """Check answer and move to next question or finish quiz."""
        if not self.selected_answer.get():
            # No option selected
            return

        correct_answer = self.questions[self.current_question_index]["answer"]
        if self.selected_answer.get() == correct_answer:
            self.score += 1

        # Move to next question or show results
        if self.current_question_index + 1 < len(self.questions):
            self.show_question(self.current_question_index + 1)
        else:
            self.show_results()

    def show_results(self):
        """Show the final quiz score."""
        for widget in self.content.winfo_children():
            widget.destroy()

        result_text = f"Quiz Completed!\nYour score: {self.score} / {len(self.questions)}"

        result_label = ctk.CTkLabel(self.content, text=result_text, font=("Arial", 24, "bold"))
        result_label.pack(pady=50)

        restart_btn = ctk.CTkButton(self.content, text="Restart Quiz", command=self.restart_quiz)
        restart_btn.pack()

    def restart_quiz(self):
        """Reset the quiz state and restart."""
        self.score = 0
        self.selected_answer.set("")
        self.content.destroy()
        self.content = ctk.CTkFrame(self, corner_radius=10)
        self.content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Rebuild quiz layout
        self.__init__(self.master, self.controller)
