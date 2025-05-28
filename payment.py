from abc import ABC, abstractmethod

class PaymentMethod(ABC):

    @abstractmethod
    def pay(self, amount: float):
        pass

class CreditCardPayment(PaymentMethod):
    def __init__(self, card_number: str):
        self.card_number = card_number

    def pay(self, amount: float):
        print(f"Processing credit card payment of ${amount:.2f} using card {self.card_number}.")
    
class PayPalPayment(PaymentMethod):
    def __init__(self, email: str):
        self.email = email

    def pay(self, amount: float):
        print(f"Processing PayPal payment of ${amount:.2f} using account {self.email}.")

class CryptoPayment(PaymentMethod):
    def __init__(self, wallet_address: str):
        self.wallet_address = wallet_address

    def pay(self, amount: float):
        print(f"Processing cryptocurrency payment of ${amount:.2f} to wallet {self.wallet_address}.")

