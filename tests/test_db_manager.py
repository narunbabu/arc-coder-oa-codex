import os
import unittest
from todo_app.db_manager import DBManager


class TestDBManager(unittest.TestCase):
    def setUp(self):
        self.db_file = "test_tasks_notes.db"
        if os.path.exists(self.db_file):
            os.remove(self.db_file)
        self.db = DBManager(self.db_file)

    def tearDown(self):
        self.db.close()
        if os.path.exists(self.db_file):
            os.remove(self.db_file)

    def test_add_and_list_task(self):
        tid = self.db.add_task("Task 1", "2024-01-01", 1)
        tasks = self.db.list_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0][0], tid)
        self.assertEqual(tasks[0][1], "Task 1")

    def test_add_and_delete_note(self):
        nid = self.db.add_note("Note", "content")
        notes = self.db.list_notes()
        self.assertEqual(len(notes), 1)
        self.db.delete_note(nid)
        notes = self.db.list_notes()
        self.assertEqual(notes, [])


if __name__ == "__main__":
    unittest.main()
