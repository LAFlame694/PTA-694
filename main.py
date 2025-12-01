import customtkinter as ctk
from ui.home_page import HomePage
from ui.lesson_page import LessonPage
from ui.quiz_page import QuizPage
from ui.code_editor import CodeEditor
from ui.report_card import ReportCard


class ProgrammingTutorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Programming Tutor App")
        self.geometry("1200x700")

        # store pages in a dictionary
        self.pages = {}

        # main container
        self.container = ctk.CTkFrame(self, corner_radius=0)
        self.container.pack(fill="both", expand=True)

        # In ProgrammingTutorApp.__init__ after creating self.container
        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)

        self.register_pages()
        self.show_frame(self.pages["home"])

    def register_pages(self):
        # All pages
        pages_dict = {
            "home": HomePage,
            "lessons": LessonPage,
            "quizzes": QuizPage,
            "editor": CodeEditor,
            "report": ReportCard
        }

        for key, PageClass in pages_dict.items():
            frame = PageClass(self.container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.pages[key] = PageClass

            # Store instance separately
            setattr(self, f"{key}_page", frame)

    def show_frame(self, page_class):
        frame = None

        # find the instance by class
        for key in self.pages:
            pg_class = self.pages[key]
            inst = getattr(self, f"{key}_page")
            if isinstance(inst, pg_class):
                if pg_class == page_class:
                    frame = inst
                    break

        frame.tkraise()


if __name__ == "__main__":
    app = ProgrammingTutorApp()
    app.mainloop()
