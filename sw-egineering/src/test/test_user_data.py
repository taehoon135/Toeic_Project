import os
import unittest
import json
import tempfile
import shutil
from user_data_manipulation.user_data import UserData


class TestUserData(unittest.TestCase):
    def setUp(self):
        # Create a temporary JSON file for testing
        self.test_data = {
            "User1": {"password": 1234, "APIKEY": 1234},
            "Manager": {"password": "admin"}
        }
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test_userdata.json")
        
        # Write test data to temporary file
        with open(self.test_file, 'w') as f:
            json.dump(self.test_data, f)
        
        self.user_data = UserData(self.test_file)

    def tearDown(self):
        # Clean up temporary files
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        shutil.rmtree(self.temp_dir)

    def test_id_check(self):
        self.assertTrue(self.user_data.id_check("User1"))
        self.assertFalse(self.user_data.id_check("NonExistentUser"))

    def test_password_check(self):
        self.assertTrue(self.user_data.password_check("User1", 1234))
        self.assertFalse(self.user_data.password_check("User1", "wrong_password"))

    def test_add_user(self):
        new_user_id = "User2"
        new_user_props = {"password": "abcd", "APIKEY": 5678}
        
        # Test adding new user
        self.assertTrue(self.user_data.add_user(new_user_id, new_user_props))
        
        # Test adding existing user
        self.assertFalse(self.user_data.add_user(new_user_id, new_user_props))

    def test_get_user_prop(self):
        self.assertEqual(self.user_data.get_user_prop("User1", "APIKEY"), 1234)
        self.assertIsNone(self.user_data.get_user_prop("User1", "NonExistentProp"))

    def test_add_prop(self):
        self.assertTrue(self.user_data.add_prop("Manager", "APIKEY", 9090))
        self.assertEqual(self.user_data.get_user_prop("Manager", "APIKEY"), 9090)

    def test_modify_prop(self):
        self.assertTrue(self.user_data.modify_prop("User1", "password", 4356))
        self.assertEqual(self.user_data.get_user_prop("User1", "password"), 4356)

    def test_delete_prop(self):
        self.assertTrue(self.user_data.delete_prop("User1", "APIKEY"))
        self.assertIsNone(self.user_data.get_user_prop("User1", "APIKEY"))

    def test_delete_user(self):
        self.assertTrue(self.user_data.delete_user("User1"))
        self.assertFalse(self.user_data.id_check("User1"))

    def test_save(self):
        output_file = os.path.join(self.temp_dir, "updated_user_data.json")
        self.user_data.save(output_file)
        self.assertTrue(os.path.exists(output_file))
        
        # Verify saved data
        with open(output_file, 'r') as f:
            saved_data = json.load(f)
        self.assertEqual(saved_data, self.user_data.get_all_data())

if __name__ == "__main__":
    unittest.main()