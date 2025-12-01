import customtkinter as ctk
from ui.base_page import BasePage
import json
import os
import tkinter as tk


class LessonPage(BasePage):
    def _init_(self, parent, controller):
        super()._init_(parent, controller)

        # Layout
        self.content.grid_columnconfigure(1, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

        # Left: Lesson List
        self.lesson_list = tk.Listbox(self.content, width=30, font=("Arial", 14))
        self.lesson_list.grid(row=0, column=0, sticky="nsw", padx=(0, 20), pady=10)

        # Right: Lesson Text Display (READ-ONLY)
        self.lesson_text = ctk.CTkTextbox(
            self.content, wrap="word", state="disabled", font=("Arial", 15)
        )
        self.lesson_text.grid(row=0, column=1, sticky="nsew", pady=10)

        # --- Styling Tags ---
        # Titles
        self.lesson_text.tag_config(
            "title",
            foreground="#00aaff",
        )

        # Subtitles
        self.lesson_text.tag_config(
            "subtitle",
            foreground="#ffaa00",
        )

        # Load lessons
        self.lessons_dir = os.path.join(
            os.path.dirname(os.path.realpath(_file_)), "..", "lessons"
        )
        self.lessons = {}
        self.load_lessons()

        # Populate list
        for lesson_title in self.lessons.keys():
            self.lesson_list.insert(ctk.END, lesson_title)

        self.lesson_list.bind("<<ListboxSelect>>", self.display_lesson_content)

        # Auto-select first
        if self.lesson_list.size() > 0:
            self.lesson_list.select_set(0)
            self.display_lesson_content()

    def load_lessons(self):
        """Load JSON lessons."""
        for filename in os.listdir(self.lessons_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(self.lessons_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        title = data.get("title", filename[:-5])
                        self.lessons[title] = data.get("sections", [])
                except:
                    print(f"Failed to load lesson file: {filename}")

    def display_lesson_content(self, event=None):
        selection = self.lesson_list.curselection()
        if not selection:
            return

        index = selection[0]
        lesson_title = self.lesson_list.get(index)
        sections = self.lessons.get(lesson_title, [])

        self.lesson_text.configure(state="normal")
        self.lesson_text.delete("1.0", ctk.END)

        # Insert Main Title
        self.lesson_text.insert("end", lesson_title.upper() + "\n\n", "title")

        # Insert Sections
        for section in sections:
            subtitle = section.get("subtitle", "")
            text = section.get("text", "")

            if subtitle:
                self.lesson_text.insert("end", subtitle + "\n", "subtitle")

            if text:
                self.lesson_text.insert("end", text + "\n\n")

        self.lesson_text.configure(state="disabled")