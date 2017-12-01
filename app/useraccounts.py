# File to handle user accounts
import re


class UserClass(object):
    # Class to handle registration and login of users
    

    def __init__(self):
        # list to contain users
        self.user_list = []

    def registerUser(self, username, email, password, cpassword):
        # Creating registered users that have signed up by adding to dictionary
        # Empty dict to hold each user
        user_dict = {}
        # Check for existing user
        for user in self.user_list:
            if username == user['username']:
                return "User already exists. Please login"
        # Check for right password length
        if len(password) < 6:
            return "Your password should be at least 6 characters long"
        # Check for special characters in username
        elif not re.match("^[a-zA-Z0-9_]*$", username):
            return "No special characters (. , ! space [] )"
        # Check for correct email
        elif not re.match(r"(^[a-zA-Z0-9_.]+@[a-zA-Z0-9-]+\.[a-z]+$)", email):
            return "Please provide a valid email address"
        # Password Mismatch
        elif password == cpassword:
            user_dict['username'] = username
            user_dict['email'] = email
            user_dict['password'] = password
            self.user_list.append(user_dict)
        else:
            return "Password mismatch"
        return "Successfully registered. You can now login!"

    def login(self, username, password):
        # Log in users
        for user in self.user_list:
            if username == user['username']:
                if password == user['password']:
                    return "Successfully logged in, create event!"
                return "Password mismatch"
        return "You have no account,please sign up"

    def changePassword(self, npassword, cpassword):
        #Change password
        for user in self.user_list:
            if npassword == cpassword:
                user['password'] = npassword
                return "Password changed successful"
            return "The new passwords should match"
        return "User does not exist, sign up!"

    def get_user_by_email(self, user):
        for item in self.user_list:
            if item['username'] == user:
                email = item['email']
                return email
        else:
            return False


