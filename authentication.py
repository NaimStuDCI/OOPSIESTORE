from abc import ABC, abstractmethod

class User(ABC):
    """Abstract base class for user management."""
    @abstractmethod    
    def check_password(self, password):
        """Check if the provided password matches the user's password."""
        pass
    
    @abstractmethod
    def is_admin(self):
        """Check if the user has admin privileges."""
        pass

    @abstractmethod
    def full_name(self):
        """Return the full name of the user."""
        pass

class Admin(User):
    """Class representing an admin user."""
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.role = "admin"
    
    def check_password(self, password):
        return self._password == password
    
    def is_admin(self):
        return True
    
class Employee(User):
    """Class representing a regular user."""
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.role = "employee"
    
    def check_password(self, password):
        return self.password == password
    
    def is_admin(self):
        return False
    
class Customer(User):
    """Class representing a customer user."""
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.role = "customer"
    
    def check_password(self, password):
        return self.password == password
    
    def is_admin(self):
        return False