import os
import tkinter as tk

class ExerciseEditor(tk.Toplevel):
    def __init__(self, parent, exercise_text, save_callback):
        super().__init__(parent)
        self.parent = parent
        self.exercise_text = exercise_text
        self.save_callback = save_callback
        self.title("Editare exerciții")
        self.geometry("400x300")
        self.create_widgets()

    def create_widgets(self):
        self.exercise_entry = tk.Text(self, font=("Arial", 12), width=40, height=10)
        self.exercise_entry.insert(tk.END, self.exercise_text)
        self.exercise_entry.pack()

        btn_save = tk.Button(self, text="Salvează", command=self.save_exercise, width=10, height=2, font=("Arial", 12), bg='#3498db', fg='white')
        btn_save.pack()

    def save_exercise(self):
        exercise_text = self.exercise_entry.get("1.0", tk.END).strip()
        self.save_callback(exercise_text)
        self.parent.update_exercise_display()
        if exercise_text:
            self.parent.btn_view.config(text="Editare")
        else:
            self.parent.btn_view.config(text="Adaugare")
        self.destroy()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.username = ""
        self.current_page = None
        self.title("Aplicație Fitness Tracker")
        self.geometry("500x400")
        self.configure(bg='#f0f0f0')
        self.attributes('-fullscreen', True)
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Bine ai venit! Te rugăm să introduci un cont:", font=("Arial", 14), bg='#f0f0f0')
        self.label.pack()
        self.label.place(relx=0.5, rely=0.37, anchor=tk.CENTER)
        self.entry = tk.Entry(self, font=("Arial", 12))
        self.entry.pack()
        self.entry.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.button = tk.Button(self, text="Începem", command=self.save_user, width=15, height=2, font=("Arial", 12), bg='#3498db', fg='white')
        self.button.pack()
        self.button.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

    def save_user(self):
        self.username = self.entry.get()
        self.label.pack_forget()
        self.entry.pack_forget()
        self.button.pack_forget()
        user_profile_file = f"C:\\Users\\Florentin\\Desktop\\python\\profile\\{self.username}_profile.txt"
        profile_exists = os.path.exists(user_profile_file)
        if not profile_exists:
            with open(user_profile_file, "w", encoding="utf-8") as file:
                file.write(f"Nume utilizator: {self.username}\n")
                file.write("Greutate: kg\n")
                file.write("Înălțime: m\n")
                file.write("Vârstă: ani\n")
                file.write("Greutate dorita: kg\n")
        else:
            self.show_page("welcome")

    def save_exercises(self, exercise_text):
        with open(f"C:\\Users\\Florentin\\Desktop\\python\\exercises\\{self.username}_exercises.txt", "w") as file:
            file.write(exercise_text)

    def load_exercises(self):
        try:
            with open(f"C:\\Users\\Florentin\\Desktop\\python\\exercises\\{self.username}_exercises.txt", "r") as file:
                exercises = file.read()
                return exercises
        except FileNotFoundError:
            return ""

    def save_profile_data(self, profile_list_content):
        user_profile_file = f"C:\\Users\\Florentin\\Desktop\\python\\profile\\{self.username}_profile.txt"
        with open(user_profile_file, "w", encoding="utf-8") as file:
            file.write("\n".join(profile_list_content))

    def save_profile_input(self, profile_input):
        with open(f"C:\\Users\\Florentin\\Desktop\\python\\profile\\{self.username}_profile.txt", "a") as file:
            file.write(profile_input)
            file.write("\n")

    def load_profile_data(self):
        user_profile_file = f"C:\\Users\\Florentin\\Desktop\\python\\profile\\{self.username}_profile.txt"
        try:
            with open(user_profile_file, "r", encoding="utf-8") as file:
                profile_data = file.read().splitlines()
                return profile_data
        except FileNotFoundError:
            return []

    def toggle_edit_save(self):
        if self.btn_view.cget("text") == "Editare" or self.btn_view.cget("text") == "Adaugare":
            exercise_text = self.load_exercises()
            self.exercise_editor = ExerciseEditor(self, exercise_text, self.save_exercises)
        else:
            self.create_exercises_page()

    def show_page(self, page):
        if self.current_page is not None:
            self.current_page.pack_forget()
        if page == "welcome":
            self.current_page = self.create_welcome_page()
        elif page == "exercises":
            self.current_page = self.create_exercises_page()
        elif page == "profile":
            self.current_page = self.create_profile_page()
        self.current_page.pack(fill=tk.BOTH, expand=True)

    def create_welcome_page(self):
        welcome_frame = tk.Frame(self, bg='#f0f0f0')
        welcome_label = tk.Label(welcome_frame, text=f"Bun venit, {self.username}!", font=("Arial", 18), bg='#f0f0f0')
        welcome_label.pack()
        btn_frame = tk.Frame(welcome_frame, bg='#f0f0f0')
        btn_frame.pack()
        btn_width = 20
        btn_height = 3
        btn_exercises = tk.Button(btn_frame, text="Exercițiile mele", command=lambda: self.show_page("exercises"), width=btn_width, height=btn_height, font=("Arial", 12), bg='#3498db', fg='white')
        btn_exercises.grid(row=1, column=0, pady=10)
        btn_profile = tk.Button(btn_frame, text="Profilul Utilizatorului", command=lambda: self.show_page("profile"), width=btn_width, height=btn_height, font=("Arial", 12), bg='#3498db', fg='white')
        btn_profile.grid(row=1, column=1, pady=10)
        btn_close = tk.Button(welcome_frame, text="Închide", command=self.destroy, width=10, height=2, font=("Arial", 12), bg='red', fg='white')
        btn_close.pack()
        return welcome_frame

    def create_exercises_page(self):
        exercises_frame = tk.Frame(self, bg='#330066')
        exercises_label = tk.Label(exercises_frame, text="Exercițiile Mele", font=("Arial", 22), bg='#330068', fg='white')
        exercises_label.pack(side=tk.TOP, pady=10)
        saved_exercises = self.load_exercises()
        self.exercise_display = tk.Label(exercises_frame, text=saved_exercises, font=("Arial", 18), wraplength=400, justify=tk.LEFT, bg='#330068', fg='white')
        self.exercise_display.pack(side=tk.TOP, padx=10, pady=10)
        if(saved_exercises.strip()):
            self.btn_view = tk.Button(exercises_frame, text="Editare", command=self.toggle_edit_save, width=10, height=2, font=("Arial", 12), bg='#3498db', fg='white')
        else:
            self.btn_view = tk.Button(exercises_frame, text="Adaugare", command=self.toggle_edit_save, width=10, height=2, font=("Arial", 12), bg='#3498db', fg='white')
        self.btn_view.pack(side=tk.BOTTOM, pady=20)
        self.btn_view.place(relx=0.495, rely=0.98, anchor=tk.SE)
        btn_back = tk.Button(exercises_frame, text="Înapoi", command=lambda: self.show_page("welcome"), width=10, height=2, font=("Arial", 12), bg='orange', fg='white')
        btn_back.pack(side=tk.BOTTOM, pady=20)
        btn_back.place(relx=0.555, rely=0.98, anchor=tk.SE)
        return exercises_frame

    def edit_item(self, profile_list):
        selected_index = profile_list.curselection()
        if selected_index:
            edit_window = tk.Toplevel()
            edit_window.title("Editare element")
            selected_value = profile_list.get(selected_index)
            edit_entry = tk.Entry(edit_window, font=("Arial", 14), bg='#555555', fg='white')
            edit_entry.insert(tk.END, selected_value)
            edit_entry.pack()
            def save_edit():
                new_value = edit_entry.get()
                profile_list.delete(selected_index)
                profile_list.insert(selected_index, new_value)
                profile_list_content = []
                for i in range(profile_list.size()):
                    profile_list_content.append(profile_list.get(i))
                self.save_profile_data(profile_list_content)
                edit_window.destroy()
            btn_save = tk.Button(edit_window, text="Salvează", command=save_edit, width=10, height=2, font=("Arial", 12), bg='green', fg='white')
            btn_save.pack()

    def create_profile_page(self):
        profile_frame = tk.Frame(self, bg='#333333')
        profile_label = tk.Label(profile_frame, text="Profilul Utilizatorului", font=("Arial", 18), bg='#333333', fg='white')
        profile_label.pack(fill=tk.BOTH, expand=True)
        list_frame = tk.Frame(profile_frame, bg='#333333', highlightthickness=0)
        list_frame.pack(fill=tk.BOTH, expand=True)
        profile_list = tk.Listbox(list_frame, font=("Arial", 22), bg='#555555', fg='white', height=10, selectbackground='#555555')
        profile_list.pack(fill=tk.BOTH, expand=True)
        profile_list_content = self.load_profile_data()
        for item in profile_list_content:
            profile_list.insert(tk.END, item)
        btn_edit = tk.Button(profile_frame, text="Editează", command=lambda: self.edit_item(profile_list), width=10, height=2, font=("Arial", 12), bg='blue', fg='white')
        btn_edit.pack()
        btn_back = tk.Button(profile_frame, text="Înapoi", command=lambda: self.show_page("welcome"), width=10, height=2, font=("Arial", 12), bg='orange', fg='white')
        btn_back.pack()
        return profile_frame

    def update_exercise_display(self):
        saved_exercises = self.load_exercises()
        if self.exercise_display is not None:
            self.exercise_display.config(text=saved_exercises)
        if self.btn_view is not None:
            if saved_exercises.strip():
                self.btn_view.config(text="Editare")
            else:
                self.btn_view.config(text="Adaugare")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
