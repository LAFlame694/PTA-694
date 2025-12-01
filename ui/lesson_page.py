import customtkinter as ctk
from ui.base_page import BasePage
import json
import os
import tkinter as tk


class LessonPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        # Setup the content layout: left listbox + right text area
        self.content.grid_columnconfigure(1, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

        # Left: Lesson List
        self.lesson_list = tk.Listbox(self.content, width=30, font=("Arial", 14))
        self.lesson_list.grid(row=0, column=0, sticky="nsw", padx=(0, 20), pady=10)

        # Right: Lesson Text Display
        self.lesson_text = ctk.CTkTextbox(self.content, wrap="word", state="disabled")
        self.lesson_text.grid(row=0, column=1, sticky="nsew", pady=10)

        # Load lessons from JSON files
        self.lessons_dir = os.path.join(os.path.dirname(__file__), "..", "lessons")
        self.lessons = {}
        self.load_lessons()

        # Populate listbox with lesson titles
        for lesson_title in self.lessons.keys():
            self.lesson_list.insert(ctk.END, lesson_title)

        # Bind selection event
        self.lesson_list.bind("<<ListboxSelect>>", self.display_lesson_content)

        # Select first lesson by default
        if self.lesson_list.size() > 0:
            self.lesson_list.select_set(0)
            self.display_lesson_content()

    def load_lessons(self):
        """Load all JSON lesson files into self.lessons dict."""
        for filename in os.listdir(self.lessons_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(self.lessons_dir, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                        title = data.get("title", filename.replace(".json", ""))
                        content = data.get("content", "")
                        self.lessons[title] = content
                    except json.JSONDecodeError:
                        print(f"Failed to load lesson {filename}")

    def display_lesson_content(self, event=None):
        """Display the selected lesson content in the textbox."""
        selection = self.lesson_list.curselection()
        if not selection:
            return
        index = selection[0]
        lesson_title = self.lesson_list.get(index)

        # Clear text box
        self.lesson_text.configure(state="normal")
        self.lesson_text.delete("1.0", ctk.END)

        # Insert new content
        lesson_content = self.lessons.get(lesson_title, "No content available.")
        self.lesson_text.insert(ctk.END, lesson_content)
        self.lesson_text.configure(state="disabled")
