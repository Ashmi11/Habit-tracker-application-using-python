import json
import os
from datetime import datetime, date


class HabitTracker:
    def __init__(self, data_file="habit_data.json"):
        """
        Initializes a HabitTracker instance.

        Parameters:
            - data_file (str): The filename for storing habit data in JSON format.
        """
        self.data_file = data_file
        self.habits = []
        self.load_data()

    def load_data(self):
        """
        Loads habit data from the specified JSON file.
        """
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                self.habits = json.load(file)

    def save_data(self):
        """
        Saves habit data to the specified JSON file.
        """
        with open(self.data_file, "w") as file:
            json.dump(self.habits, file, default=str)

    def reset_data(self):
        """
        Resets all habit data.
        """
        self.habits = []
        self.save_data()

    def create_habit(self, task, periodicity):
        """
        Creates a new habit.

        Parameters:
            - task (str): The name of the habit.
            - periodicity (str): The frequency of the habit ("daily" or "weekly").
        """
        # Check if a habit with the same name already exists
        if any(habit["task"].lower() == task.lower() for habit in self.habits):
            print(f"Error: Habit with the name '{task}' already exists.")
        else:
            habit = {
                "task": task,
                "periodicity": periodicity,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "completed_at": [],
                "streak": 0,  # Initialize streak to 0 when creating a new habit
                "all_streaks": []  # Initialize all_streaks to an empty list
            }
            self.habits.append(habit)
            self.save_data()

    def delete_habit(self, task):
        """
        Deletes a habit.

        Parameters:
            - task (str): The name of the habit to be deleted.
        """
        self.habits = [habit for habit in self.habits if habit["task"] != task]
        self.save_data()

    def complete_task(self, task, custom_completed_at=None):
        """
        Marks a habit as completed and updates streak.

        Parameters:
            - task (str): The name of the habit to be marked as completed.
            - custom_completed_at (str): Custom completion time (optional).
        """
        habit = next((habit for habit in self.habits if habit["task"] == task), None)
        if habit:
            habit["completed_at"] = custom_completed_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            habit["streak"] += 1
            self.save_data()

    def get_all_habits(self):
        """
        Retrieves a list of all habits.
        """
        return self.habits

    def get_habits_by_periodicity(self, periodicity):
        """
        Retrieves habits based on their periodicity.

        Parameters:
            - periodicity (str): The frequency of habits to retrieve ("daily" or "weekly").

        Returns:
            List of habits with the specified periodicity.
        """
        return [habit for habit in self.habits if habit["periodicity"] == periodicity]

    def get_longest_run_streak_for_habit(self, task):
        """
        Retrieves the longest run streak for a specific habit.

        Parameters:
            - task (str): The name of the habit.

        Returns:
            int: The longest run streak for the specified habit.
        """
        habit = next((habit for habit in self.habits if habit["task"].lower() == task.lower()), None)
        return habit.get("streak", 0)

    def get_longest_run_streak_all(self):
        """
        Retrieves the longest run streak across all habits.

        Returns:
            str: The habit and streak with the longest run.
        """
        all_streaks = [(habit["task"], habit.get("streak", 0)) for habit in self.habits]
        longest_streak_habit, longest_streak = max(all_streaks, key=lambda x: x[1], default=(None, 0))
        return f"{longest_streak_habit}: {longest_streak}"

    def get_broken_habits(self):
        """
        Retrieves habits that are considered broken (not completed within the expected timeframe).

        Returns:
            List of broken habits.
        """
        current_datetime = datetime.now()
        broken_habits = []

        for habit in self.habits:
            if habit["completed_at"]:
                completed_at = datetime.strptime(habit["completed_at"], "%Y-%m-%d %H:%M:%S")
                days_since_completion = (current_datetime - completed_at).days

                if (days_since_completion > 1 and habit["periodicity"] == "daily") or (
                        days_since_completion > 7 and habit["periodicity"] == "weekly"
                ):
                    broken_habits.append(habit)
                    habit["streak"] = 0

        return broken_habits


class Analytics:
    def __init__(self, habit_tracker):
        """
        Initializes an Analytics instance.

        Parameters:
            - habit_tracker (HabitTracker): The HabitTracker instance to perform analytics on.
        """
        self.habit_tracker = habit_tracker

    def get_all_tracked_habits(self):
        """
        Retrieves a list of all tracked habits.

        Returns:
            List of all habits tracked by the associated HabitTracker.
        """
        return self.habit_tracker.get_all_habits()

    def get_habits_by_periodicity(self, periodicity):
        """
        Retrieves habits based on their periodicity.

        Parameters:
            - periodicity (str): The frequency of habits to retrieve ("daily" or "weekly").

        Returns:
            List of habits with the specified periodicity.
        """
        return self.habit_tracker.get_habits_by_periodicity(periodicity)

    def get_longest_run_streak_all(self):
        """
        Retrieves the longest run streak across all habits.

        Returns:
            str: The habit and streak with the longest run.
        """
        return self.habit_tracker.get_longest_run_streak_all()

    def get_broken_habits(self):
        """
        Retrieves habits that are considered broken (not completed within the expected timeframe).

        Returns:
            List of broken habits.
        """
        return self.habit_tracker.get_broken_habits()


# Example Usage
if __name__ == "__main__":
    tracker = HabitTracker()

    # Create habits
    tracker.create_habit("Exercise", "daily")
    tracker.create_habit("Reading", "daily")
    tracker.create_habit("Meditation", "daily")
    tracker.create_habit("Running", "weekly")
    tracker.create_habit("Coding", "weekly")

    # Simulate completing tasks
    tracker.complete_task("Exercise")
    tracker.complete_task("Reading")
    tracker.complete_task("Meditation")
    tracker.complete_task("Running")
    tracker.complete_task("Coding")

    # Simulate completing tasks for 4 weeks
    for _ in range(4):
        tracker.complete_task("Exercise")
        tracker.complete_task("Reading")
        tracker.complete_task("Meditation")
        tracker.complete_task("Running")
        tracker.complete_task("Coding")

    # Print habits
    print("All Habits:")
    for habit in tracker.get_all_habits():
        print(habit)

    print("\nHabits with periodicity 'daily':")
    for habit in tracker.get_habits_by_periodicity("daily"):
        print(habit)

    print("\nLongest run streak for 'Exercise':", tracker.get_longest_run_streak_for_habit("Exercise"))
    print("Longest run streak for all habits:", tracker.get_longest_run_streak_all())
