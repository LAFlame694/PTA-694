import customtkinter as ctk
from ui.base_page import BasePage
import sqlite3
import os


class ReportCard(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.content.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            self.content,
            text="Your Progress Report",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=(20, 40))

        # Connect to DB
        db_path = os.path.join(os.path.dirname(__file__), "..", "database", "progress.db")
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

        # Fetch progress data
        self.progress_data = self.fetch_progress()

        # Display progress stats
        self.display_progress()

    def fetch_progress(self):
        # Example table queries — adapt based on your DB schema

        data = {}

        # Lessons completed count
        self.cursor.execute("SELECT COUNT(DISTINCT lesson_title) FROM lesson_progress WHERE completed=1")
        data["lessons_completed"] = self.cursor.fetchone()[0] or 0

        # Total lessons count (from lessons folder or DB)
        self.cursor.execute("SELECT COUNT(DISTINCT lesson_title) FROM lesson_progress")
        data["total_lessons"] = self.cursor.fetchone()[0] or 0

        # Quiz scores average
        self.cursor.execute("SELECT AVG(score) FROM quiz_scores")
        avg_score = self.cursor.fetchone()[0]
        data["quiz_average"] = round(avg_score, 2) if avg_score else 0

        # Code challenges completed
        self.cursor.execute("SELECT COUNT(*) FROM code_challenges WHERE completed=1")
        data["challenges_completed"] = self.cursor.fetchone()[0] or 0

        return data

    def display_progress(self):
        lessons_done = self.progress_data.get("lessons_completed", 0)
        total_lessons = self.progress_data.get("total_lessons", 1)
        quiz_avg = self.progress_data.get("quiz_average", 0)
        challenges_done = self.progress_data.get("challenges_completed", 0)

        # Lessons progress
        lesson_label = ctk.CTkLabel(
            self.content, text=f"Lessons Completed: {lessons_done} / {total_lessons}",
            font=("Arial", 18)
        )
        lesson_label.pack(pady=(10, 5))

        lesson_progress = ctk.CTkProgressBar(self.content)
        lesson_progress.set(lessons_done / total_lessons if total_lessons else 0)
        lesson_progress.pack(fill="x", padx=50, pady=(0, 20))

        # Quiz average score
        quiz_label = ctk.CTkLabel(
            self.content, text=f"Average Quiz Score: {quiz_avg} %",
            font=("Arial", 18)
        )
        quiz_label.pack(pady=(10, 5))

        quiz_progress = ctk.CTkProgressBar(self.content)
        quiz_progress.set(quiz_avg / 100)
        quiz_progress.pack(fill="x", padx=50, pady=(0, 20))

        # Challenges completed
        challenges_label = ctk.CTkLabel(
            self.content, text=f"Code Challenges Completed: {challenges_done}",
            font=("Arial", 18)
        )
        challenges_label.pack(pady=(10, 5))
