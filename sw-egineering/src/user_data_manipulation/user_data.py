import json


import json

class UserData:
    """
    A class to manage user data stored in a JSON file.

    Attributes:
        __user_data (dict): Stores user data as a dictionary.
    """

    def __init__(self, path):
        """
        Initializes the UserData object by loading user data from a JSON file.

        Args:
            path (str): The file path to load the user data from.

        Raises:
            FileNotFoundError: If the file at the given path does not exist.
            JSONDecodeError: If the file is not a valid JSON file.
        """
        with open(path, 'r', encoding='utf-8') as file:
            self.__user_data: dict = json.load(file)
    
    def id_check(self, id):
        """
        Checks if a given user ID exists in the data.

        Args:
            id (str): The user ID to check.

        Returns:
            bool: True if the user ID exists, False otherwise.
        """
        return id in self.__user_data
    
    def password_check(self, id, password):
        """
        Checks if a given password matches the password for a specific user ID.

        Args:
            id (str): The user ID to check.
            password (str): The password to validate.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return self.__user_data.get(id, {}).get("password") == password
    
    def save(self, path):
        """
        Saves the current user data to a specified JSON file.

        Args:
            path (str): The file path where the data will be saved.

        Returns:
            None
        """
        with open(path, "w", encoding="utf-8") as file:
            json.dump(self.__user_data, file, indent=4, ensure_ascii=False)

    def add_user(self, id, props):
        """
        Adds a new user to the user data.

        Args:
            id (str): The user ID to add.
            props (dict): A dictionary containing the properties for the new user.

        Returns:
            bool: True if the user was added successfully, False if the user ID already exists.

        Raises:
            ValueError: If props is not a dictionary.
        """
        if not isinstance(props, dict):
            raise ValueError("props must be a dictionary")
        
        if id not in self.__user_data:
            self.__user_data[id] = props
            return True
        else:
            return False
        
    def delete_user(self, id):
        """
        Deletes a user from the user data.

        Args:
            id (str): The user ID to delete.

        Returns:
            bool: True if the user was deleted successfully, False if the user ID does not exist.
        """
        if id in self.__user_data:
            del self.__user_data[id]
            return True
        return False
    
    def modify_prop(self, id, prop, val):
        """
        Modifies a property value for an existing user.

        Args:
            id (str): The user ID whose property is to be modified.
            prop (str): The property name to modify.
            val: The new value for the property.

        Returns:
            bool: True if the property was modified successfully, False otherwise.
        """
        if id in self.__user_data and prop in self.__user_data[id]:
            self.__user_data[id][prop] = val
            return True
        return False
    
    def add_prop(self, id, prop, val):
        """
        Adds a new property to a specific user.

        Args:
            id (str): The user ID to which the property will be added.
            prop (str): The name of the property to add.
            val: The value of the new property.

        Returns:
            bool: True if the property was added successfully, False if the user ID does not exist or the property already exists.
        """
        if id in self.__user_data:
            if prop not in self.__user_data[id]:
                self.__user_data[id][prop] = val
                return True
        return False

    def delete_prop(self, id, prop):
        """
        Deletes an existing property from a specific user.

        Args:
            id (str): The user ID whose property will be deleted.
            prop (str): The name of the property to delete.

        Returns:
            bool: True if the property was deleted successfully, False if the user ID or property does not exist.
        """
        if id in self.__user_data:
            if prop in self.__user_data[id]:
                del self.__user_data[id][prop]
                return True
        return False

        
    def get_user_prop(self, id, prop):
        """
        Retrieves the value of a specific property for a given user ID.

        Args:
            id (str): The user ID whose property value is to be retrieved.
            prop (str): The property name to retrieve.

        Returns:
            Any: The value of the property if it exists, None otherwise.
        """
        if id in self.__user_data:
            return self.__user_data[id].get(prop)
        else:
            return None
    
    def get_all_data(self):
        """
        Retrieves all data from the user data.

        Returns:
            dict: A dictionary containing all user data.
        """
        return self.__user_data