import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from habit_tracker import HabitTracker, Analytics
import json
from datetime import datetime


class HabitTrackerApp:
    def __init__(self, root):
        """
        Initializes the HabitTrackerApp.

        Parameters:
            - root (tk.Tk): The root Tkinter window.
        """
        self.root = root
        self.root.title("Habit Tracker")

        # Configure style
        self.style = ttk.Style()

        # Configure TButton style
        self.style.configure('TButton', font=('Helvetica', 12), padding=(10, 5), foreground='white',
                             background='#4CAF50')  # Green button

        # Configure TLabel style
        self.style.configure('TLabel', font=('Helvetica', 14), foreground='#333')

        # Configure TCombobox style
        self.style.configure('TCombobox', font=('Helvetica', 12), padding=(10, 5), foreground='#333',
                             background='#DDD')  # Light gray background

        # Configure TNotebook style
        self.style.configure('TNotebook', font=('Helvetica', 16), background='#F0F0F0')  # Light gray background

        # Configure TNotebook.Tab style
        self.style.map('TNotebook.Tab', background=[('selected', '#4CAF50')])  # Green background for selected tab

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        self.tracker = HabitTracker()
        self.analytics = Analytics(self.tracker)

        self.create_create_tab()
        self.create_delete_tab()
        self.create_complete_tab()
        self.create_list_tab()
        self.create_analytics_tab()
        self.create_streak_tab()

        reset_button = tk.Button(self.root, text="Reset App", command=self.reset_app, font=('Helvetica', 12),
                                 bg='#FF5722', fg='white')  # Orange button
        reset_button.pack(side="bottom", pady=10)

        root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_create_tab(self):
        """
        Creates the 'Create Habit' tab in the notebook.
        """
        create_tab = ttk.Frame(self.notebook)
        self.notebook.add(create_tab, text="Create Habit")

        # Widgets for create tab
        tk.Label(create_tab, text="Task:").grid(row=0, column=0, padx=5, pady=5)
        self.create_task_entry = tk.Entry(create_tab)
        self.create_task_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(create_tab, text="Periodicity:").grid(row=1, column=0, padx=5, pady=5)
        self.create_periodicity_combobox = ttk.Combobox(create_tab, values=["daily", "weekly"])
        self.create_periodicity_combobox.grid(row=1, column=1, padx=5, pady=5)

        create_button = tk.Button(create_tab, text="Create", command=self.create_habit)
        create_button.grid(row=2, column=0, columnspan=2, pady=10)

    def create_delete_tab(self):
        """
        Creates the 'Delete Habit' tab in the notebook.
        """
        delete_tab = ttk.Frame(self.notebook)
        self.notebook.add(delete_tab, text="Delete Habit")

        # Widgets for delete tab
        tk.Label(delete_tab, text="Select Habit:").grid(row=0, column=0, padx=5, pady=5)
        self.delete_habit_combobox = ttk.Combobox(delete_tab, values=self.get_habit_names())
        self.delete_habit_combobox.grid(row=0, column=1, padx=5, pady=5)

        delete_button = tk.Button(delete_tab, text="Delete", command=self.delete_habit)
        delete_button.grid(row=1, column=0, columnspan=2, pady=10)

    def create_complete_tab(self):
        """
        Creates the 'Complete Habit' tab in the notebook.
        """
        complete_tab = ttk.Frame(self.notebook)
        self.notebook.add(complete_tab, text="Complete Habit")

        # Widgets for complete tab
        tk.Label(complete_tab, text="Select Habit:").grid(row=0, column=0, padx=5, pady=5)
        self.complete_habit_combobox = ttk.Combobox(complete_tab, values=self.get_habit_names())
        self.complete_habit_combobox.grid(row=0, column=1, padx=5, pady=5)

        complete_button = tk.Button(complete_tab, text="Complete", command=self.complete_task)
        complete_button.grid(row=1, column=0, columnspan=2, pady=10)

    def create_streak_tab(self):
        """
        Creates the 'Streaks' tab in the notebook.
        """
        streak_tab = ttk.Frame(self.notebook)
        self.notebook.add(streak_tab, text="Streaks")

        # Widgets for streak tab
        tk.Label(streak_tab, text="Select Habit (optional):").grid(row=0, column=0, padx=5, pady=5)
        self.streak_habit_combobox = ttk.Combobox(streak_tab, values=[""] + self.get_habit_names())
        self.streak_habit_combobox.grid(row=0, column=1, padx=5, pady=5)

        streak_button = tk.Button(streak_tab, text="Get Streak", command=self.get_streak)
        streak_button.grid(row=1, column=0, columnspan=2, pady=10)

    def create_list_tab(self):
        """
        Creates the 'List Habit' tab in the notebook.
        """
        list_tab = ttk.Frame(self.notebook)
        self.notebook.add(list_tab, text="List Habit")

        # Widgets for list tab
        tk.Label(list_tab, text="Select Habit:").grid(row=0, column=0, padx=5, pady=5)
        self.list_habit_combobox = ttk.Combobox(list_tab, values=self.get_habit_names())
        self.list_habit_combobox.grid(row=0, column=1, padx=5, pady=5)

        list_button = tk.Button(list_tab, text="List Habit", command=self.list_habit)
        list_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Display area for the selected habit
        self.list_habit_text = tk.Text(list_tab, height=5, width=50)
        self.list_habit_text.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def create_analytics_tab(self):
        """
        Creates the 'Analytics' tab in the notebook.
        """
        analytics_tab = ttk.Frame(self.notebook)
        self.notebook.add(analytics_tab, text="Analytics")

        # Widgets for analytics tab
        analytics_button = tk.Button(analytics_tab, text="Get All Tracked Habits", command=self.get_all_tracked_habits)
        analytics_button.grid(row=0, column=0, padx=5, pady=5)

        periodicity_button = tk.Button(analytics_tab, text="Get Habits by Periodicity",
                                       command=self.get_habits_by_periodicity)
        periodicity_button.grid(row=1, column=0, padx=5, pady=5)

        streak_button = tk.Button(analytics_tab, text="Get Longest Run Streak", command=self.get_longest_run_streak_all)
        streak_button.grid(row=2, column=0, padx=5, pady=5)

        broken_habits_button = tk.Button(analytics_tab, text="Get Broken Habits", command=self.get_broken_habits)
        broken_habits_button.grid(row=3, column=0, padx=5, pady=5)

        # Display area for analytics results
        self.analytics_text = tk.Text(analytics_tab, height=10, width=50)
        self.analytics_text.grid(row=4, column=0, padx=5, pady=5)

    def get_all_tracked_habits(self):
        """
        Displays all tracked habits in the 'Analytics' tab.
        """
        habits = self.analytics.get_all_tracked_habits()
        self.display_analytics_results("All Tracked Habits", habits)

    def get_habits_by_periodicity(self):
        """
        Displays habits by periodicity in the 'Analytics' tab.
        """
        periodicity = simpledialog.askstring("Input", "Enter periodicity (e.g., 'daily', 'weekly'):")
        if periodicity:
            habits = self.analytics.get_habits_by_periodicity(periodicity)
            self.display_analytics_results(f"Habits with Periodicity '{periodicity}'", habits)

    def get_longest_run_streak_all(self):
        """
        Displays the habit with the longest run streak in the 'Analytics' tab.
        """
        streak = self.tracker.get_longest_run_streak_all()
        self.display_analytics_results(
            "The habit that has the Longest Run Streak compared to all other habits is shown with its streak", streak)

    def get_broken_habits(self):
        """
        Displays broken habits or a success message in the 'Analytics' tab.
        """
        broken_habits = self.tracker.get_broken_habits()
        if broken_habits == [] or None:
            self.display_analytics_results(
                "GREAT JOB!!! YOU ARE ON THE RIGHT TRACK. YOU HAVE COMPLETED ALL YOUR TASKS TODAY!",
                broken_habits)
        else:
            self.display_analytics_results(
                "You missed completing these habits, and so the streak is broken.\nADVICE: You should delete this habit if it is difficult to follow.\n The streak for this habit will now be reset to 0!",
                broken_habits)

    def display_analytics_results(self, title, data):
        """
        Displays analytics results in the 'Analytics' tab.

        Parameters:
            - title (str): The title of the analytics results.
            - data (list or str): The analytics data to display.
        """
        result_text = f"{title}:\n\n"
        if isinstance(data, list):
            for item in data:
                result_text += f"{item}\n"
        else:
            result_text += f"{data}\n"

        self.analytics_text.delete(1.0, tk.END)
        self.analytics_text.insert(tk.END, result_text)

    def create_habit(self):
        """
        Creates a habit based on user input in the 'Create Habit' tab.
        """
        task = self.create_task_entry.get()
        periodicity = self.create_periodicity_combobox.get()

        # Check if a habit with the same name already exists
        if any(habit.lower() == task.lower() for habit in self.get_habit_names()):
            tk.messagebox.showerror("Error", f"Habit with the name '{task}' already exists.")
        else:
            self.tracker.create_habit(task, periodicity)
            self.create_task_entry.delete(0, tk.END)
            self.update_list_text()
            self.update_combobox_values()

    def delete_habit(self):
        """
        Deletes a habit based on user selection in the 'Delete Habit' tab.
        """
        selected_habit = self.delete_habit_combobox.get()
        if selected_habit:
            self.tracker.delete_habit(selected_habit)
            self.update_list_text()
            self.update_combobox_values()
        else:
            tk.messagebox.showinfo("Error", "Please select a habit.")

    def complete_task(self):
        """
        Completes a habit based on user selection in the 'Complete Habit' tab.
        """
        task = self.complete_habit_combobox.get()
        self.tracker.complete_task(task)
        self.update_list_text()

    def get_streak(self):
        """
        Gets and displays the streak for a habit in the 'Streaks' tab.
        """
        task = self.streak_habit_combobox.get()
        if task:
            streak = self.tracker.get_longest_run_streak_for_habit(task)
            result = f"Longest run streak for habit '{task}': {streak}"
        else:
            streak = self.tracker.get_longest_run_streak_all()
            result = f"Longest run streak within all habits is for the habit '{task}': {streak}"
        tk.messagebox.showinfo("Streak Information", result)

    def list_habit(self):
        """
        Lists details for a habit in the 'List Habit' tab.
        """
        selected_habit = self.list_habit_combobox.get()
        if selected_habit:
            habit = next((habit for habit in self.tracker.get_all_habits() if habit["task"] == selected_habit), None)
            if habit:
                habit_text = f"Task: {habit['task']}\nPeriodicity: {habit['periodicity']}\nCreated At: {habit['created_at']}\nCompleted At: {habit['completed_at']}"
                self.list_habit_text.delete(1.0, tk.END)
                self.list_habit_text.insert(tk.END, habit_text)
            else:
                tk.messagebox.showinfo("Error", "Habit not found.")
        else:
            tk.messagebox.showinfo("Error", "Please select a habit.")

    def update_combobox_values(self):
        """
        Updates all Combobox values after creating or deleting habits.
        """
        habit_names = self.get_habit_names()
        self.delete_habit_combobox["values"] = habit_names
        self.complete_habit_combobox["values"] = habit_names
        self.list_habit_combobox["values"] = habit_names
        self.streak_habit_combobox["values"] = [""] + habit_names

    def update_list_text(self):
        """
        Updates the Text widget with the list of habits.
        """
        habits = self.tracker.get_all_habits()
        list_text = ""
        for habit in habits:
            list_text += f"Task: {habit['task']}, Periodicity: {habit['periodicity']}, Created At: {habit['created_at']}, Completed At: {habit['completed_at']}\n"
        self.list_habit_text.delete(1.0, tk.END)
        self.list_habit_text.insert(tk.END, list_text)

    def get_habit_names(self):
        """
        Get a list of habit names for Combobox values.

        Returns:
            List: A list of habit names.
        """
        return [habit["task"] for habit in self.tracker.get_all_habits()]

    def on_closing(self):
        """
        Callback function called when the application window is closing.
        Saves the habit data and destroys the root window.
        """
        self.tracker.save_data()
        self.root.destroy()

    def reset_app(self):
        """
        Resets the application by clearing all habit data.
        Updates Combobox values and the displayed list.
        """
        self.tracker.reset_data()
        self.update_combobox_values()
        self.update_list_text()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("")
    app = HabitTrackerApp(root)
    root.mainloop()
