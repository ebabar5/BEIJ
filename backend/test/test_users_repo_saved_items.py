import json 
import pytest
import unittest
from pathlib import Path 
from unittest.mock import patch 
from tempfile import TemporaryDirectory

from app.repositories import users_repo
from app.error_handling import NotFound

# test saved items for users (prepare the test fixture)
class TestUsersRepo(unittest.TestCase):
    def setUp(self) -> None: 
        self.tempdir = TemporaryDirectory() 
        self.addCleanup(self.tempdir.cleanup)
        self.users_path = Path(self.tempdir.name) / "users.json"
        
        # DATA_PATH in users_repo
        self.data_path_patcher = patch(
            "app.repositories.users_repo.DATA_PATH",
            new = self.users_path,
        )
        self.data_path_patcher.start()
        self.addCleanup(self.data_path_patcher.stop)

    # write to a list of users in the temp users.json
    def _write_users(self, users) -> None: 
        self.users_path.write_text(json.dumps(users), 
        encoding = "utf-8")

    # read the JSON list back that is stored in temp 
    def _read_users(self):
        return json.loads(self.users_path.read_text(
            encoding = "utf-8"
        ))

    def test_get_saved_item_ids(self):
        users = [
            {
                "user_id": "user1",
                "username": "testuser",
                "email": "test@random.com", 
            } # not including saved_item_ids 
        ]
        self._write_users(users)
        saved_item_ids = users_repo.get_saved_item_ids("user1")
        self.assertEqual(saved_item_ids, [])
    
    def test_add_saved_item_ids(self):
        users = [
            {
                "user_id": "user1",
                "username": "testuser",
                "email": "test@random.com",
                "saved_item_ids": [],
            }
        ]
        self._write_users(users)
        updated_user = users_repo.add_saved_item("user1", "p1")
        self.assertIn("p1", updated_user["saved_item_ids"])
        raw = self._read_users()
        self.assertEqual(raw[0]["saved_item_ids"], ["p1"])

    def test_add_saved_item_error(self):
        self._write_users([])
        with self.assertRaises(NotFound):
            users_repo.add_saved_item("There is no user", "p1")
    





