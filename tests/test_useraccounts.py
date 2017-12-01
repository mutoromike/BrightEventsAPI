import unittest
# import module useraccounts
from app.useraccounts import UserClass


class AccountTestCases(unittest.TestCase):
    # Test for duplicate accounts(user already exists)
    # Test for short passwords
    # Test for correct output/account creation
    # Test login with no account
    # Test login with wrong password
    # Test login with existing email and password
    

    def setUp(self):
        # Setting up UserClass before anything
        
        self.user = UserClass()

    def tearDown(self):
        # Removing UserClass after everything
        
        del self.user

    def test_mismatchPasswords(self):
        # Checking if passwords are a match
        # Returns error message

        msg = self.user.registerUser(
            "mike", "mike@gmail.com", "asdQWER4", "asdQWER3")
        self.assertEqual(msg, "Password mismatch")

    def test_existingUser(self):
        # Checking for existing users
        # Returns error message

        self.user.registerUser(
            "mike", "mike@gmail.com", "asdQWER4", "asdQWER4")
        msg = self.user.registerUser(
            "mike", "mike@gmail.com", "asdQWER4", "asdQWER4")
        self.assertIn("User already exists", msg)

    def test_passwordLength(self):
        # Checking for pssword length
        # Returns error message

        msg = self.user.registerUser(
            "mike", "mike@gmail.com", "asdQ", "asdQ")
        self.assertEqual(
            msg, "Your password should be at least 6 characters long")

    def test_specialChar(self):
        # Checking for Special characters in username
        # Returns error message

        msg = self.user.registerUser(
            "mike$", "mike@gmail.com", "asdQWER4", "asdQWER4")
        self.assertIn("No special characters ", msg)

    def test_invalidEmail(self):
        # Checking for invalid email address
        # Returns error message

        msg = self.user.registerUser(
            "mike", "mikegmail.com", "asdQWER4", "asdQWER4")
        self.assertEqual(msg, "Please provide a valid email address")

    def test_correctInput(self):
        # Checking for correct input in all fields
        # Returns success message
        msg = self.user.registerUser(
            "mike", "mike@gmail.com", "asdQWER4", "asdQWER4")
        self.assertIn("Successfully registered", msg)

    def test_absenceOfUserAccount(self):
        # Checking for absence of user account
        # Returns error message
        self.user.user_list = [
            {'username': 'mike', 'password': 'asdQWER4', 'email': 'mike@gmail.com'}]
        msg = self.user.login("michael", "asdQWER4")
        self.assertEqual(msg, "You have no account,please sign up")

    def test_loginWrongPassword(self):
        # Checking for log in wrong password
        # Returns error message

        self.user.user_list = [
            {'username': 'mike', 'password': 'asdQWER4', 'email': 'mike@gmail.com'}]
        msg = self.user.login("mike", "asdQWER34")
        self.assertEqual(msg, "Password mismatch")

    def test_correctLogin(self):
        # Checking for correct log in credentials
        # Returns error message

        self.user.user_list = [
            {'username': 'mike', 'password': 'asdQWER4', 'email': 'mike@gmail.com'}]
        msg = self.user.login("mike", "asdQWER4")
        self.assertIn("create event!", msg)


if __name__ == '__main__':
    unittest.main()
