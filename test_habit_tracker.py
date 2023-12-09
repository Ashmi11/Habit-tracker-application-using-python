import unittest
import json
import os
from datetime import datetime, timedelta
from habit_tracker import HabitTracker

class TestHabitTracker(unittest.TestCase):
    """
    Unit tests for the HabitTracker class.

    These tests cover various functionalities of the HabitTracker class.
    """

    def setUp(self):
        """
        Set up the test environment.

        Creates a temporary data file and initializes a HabitTracker instance for testing.
        """
        self.data_file = "test_habit_data.json"
        self.tracker = HabitTracker(data_file=self.data_file)

    def tearDown(self):
        """
        Clean up the test environment.

        Removes the temporary data file created during testing.
        """
        if os.path.exists(self.data_file):
            os.remove(self.data_file)

    def test_create_habit(self):
        """
        Test the creation of a new habit.

        Verifies that a habit is correctly created and added to the list of habits.
        """
        self.tracker.create_habit("TestHabit", "daily")
        habits = self.tracker.get_all_habits()
        self.assertEqual(len(habits), 1)
        self.assertEqual(habits[0]["task"], "TestHabit")

    def test_delete_habit(self):
        """
        Test the deletion of a habit.

        Verifies that a habit is correctly deleted from the list of habits.
        """
        self.tracker.create_habit("TestHabit", "daily")
        self.tracker.delete_habit("TestHabit")
        habits = self.tracker.get_all_habits()
        self.assertEqual(len(habits), 0)

    def test_complete_task(self):
        """
        Test completing a habit task.

        Verifies that completing a task increases the streak count for the habit.
        """
        self.tracker.create_habit("TestHabit", "daily")
        self.tracker.complete_task("TestHabit")
        habits = self.tracker.get_all_habits()
        self.assertEqual(habits[0]["streak"], 1)

    def test_get_longest_run_streak_for_habit(self):
        """
        Test retrieving the longest run streak for a specific habit.

        Verifies that the correct longest run streak is returned for a specific habit.
        """
        self.tracker.create_habit("TestHabit", "daily")
        self.tracker.complete_task("TestHabit")
        self.tracker.complete_task("TestHabit")
        streak = self.tracker.get_longest_run_streak_for_habit("TestHabit")
        self.assertEqual(streak, 2)

    def test_get_longest_run_streak_all(self):
        """
        Test retrieving the longest run streak for all habits.

        Verifies that the correct habit with the longest run streak is returned.
        """
        self.tracker.create_habit("TestHabit1", "daily")
        self.tracker.create_habit("TestHabit2", "daily")

        for _ in range(3):
            self.tracker.complete_task("TestHabit1")

        streak = self.tracker.get_longest_run_streak_all()
        self.assertEqual(streak, "TestHabit1: 3")

    def test_get_broken_habits(self):
        """
        Test retrieving broken habits.

        Verifies that habits with broken streaks are correctly identified and returned.
        """
        self.tracker.create_habit("TestHabit1", "daily")
        self.tracker.create_habit("TestHabit2", "weekly")

        # Simulate completing tasks
        self.tracker.complete_task("TestHabit1", custom_completed_at="2023-01-01 12:00:00")
        self.tracker.complete_task("TestHabit2", custom_completed_at="2023-12-09 12:00:00")

        # Simulate breaking habit streaks
        broken_habits = self.tracker.get_broken_habits()
        self.assertEqual(len(broken_habits), 1)
        self.assertEqual(broken_habits[0]["task"], "TestHabit1")

    def test_get_habits_by_periodicity(self):
        """
        Test retrieving habits by periodicity.

        Verifies that habits with a specific periodicity are correctly identified and returned.
        """
        self.tracker.create_habit("TestHabit1", "daily")
        self.tracker.create_habit("TestHabit2", "weekly")
        self.tracker.create_habit("TestHabit3", "daily")

        daily_habits = self.tracker.get_habits_by_periodicity("daily")
        self.assertEqual(len(daily_habits), 2)
        self.assertEqual(daily_habits[0]["task"], "TestHabit1")
        self.assertEqual(daily_habits[1]["task"], "TestHabit3")

if __name__ == "__main__":
    unittest.main()