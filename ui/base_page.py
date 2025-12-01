import customtkinter as ctk


class BasePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        self.controller = controller
        # ----------- GRID SETUP -----------
        self.grid_columnconfigure(0, weight=0)   # sidebar column stays fixed
        self.grid_columnconfigure(1, weight=1)   # content column expands
        self.grid_rowconfigure(0, weight=1)      # row expands vertically

        # ----------- SIDEBAR -----------
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsw")

        title = ctk.CTkLabel(self.sidebar, text="Tutor App",
                             font=("Arial", 22, "bold"))
        title.pack(pady=(40, 20))

        # Navigation Buttons
        ctk.CTkButton(
            self.sidebar, text="🏠 Home",
            command=lambda: controller.show_frame(controller.pages["home"])
        ).pack(pady=10, fill="x")

        ctk.CTkButton(
            self.sidebar, text="📘 Lessons",
            command=lambda: controller.show_frame(controller.pages["lessons"])
        ).pack(pady=10, fill="x")

        ctk.CTkButton(
            self.sidebar, text="📝 Quizzes",
            command=lambda: controller.show_frame(controller.pages["quizzes"])
        ).pack(pady=10, fill="x")

        ctk.CTkButton(
            self.sidebar, text="💻 Code Editor",
            command=lambda: controller.show_frame(controller.pages["editor"])
        ).pack(pady=10, fill="x")

        ctk.CTkButton(
            self.sidebar, text="📊 Report Card",
            command=lambda: controller.show_frame(controller.pages["report"])
        ).pack(pady=10, fill="x")

        # Appearance Mode Switch
        self.theme_switch = ctk.CTkSwitch(
            self.sidebar,
            text="Dark Mode",
            command=self.toggle_theme
        )
        self.theme_switch.pack(pady=20)

        # ----------- MAIN CONTENT AREA -----------
        self.content = ctk.CTkFrame(self, corner_radius=10)
        self.content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def toggle_theme(self):
        current = ctk.get_appearance_mode()
        new_mode = "light" if current == "Dark" else "dark"
        ctk.set_appearance_mode(new_mode)
