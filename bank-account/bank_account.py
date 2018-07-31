import threading

def raise_exception_if_account_closed(method):
    def exception_decorator(bank_account, *args):
        if not bank_account.opened:
            raise ValueError("Can't perform {} on a closed account.".format(method.__name__))
        else:
            return method(bank_account, *args)
    return exception_decorator

class BankAccount(object):
    def __init__(self):
        self.opened = False
        self.balance = 0
        self.lock = threading.Lock()

    @raise_exception_if_account_closed
    def get_balance(self):
        return self.balance

    def open(self):
        self.opened = True

    @raise_exception_if_account_closed
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("If you want to withdraw {}, you'll have to explicitely use the 'withdraw' service".format(-amount))
        else:
            self.__add_to_balance(amount)

    @raise_exception_if_account_closed
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("If you want to deposit {}, you'll have to explicitely use the 'deposit' service".format(-amount))
        else:
            self.__add_to_balance(-amount)

    @raise_exception_if_account_closed
    def close(self):
        self.opened = False

    def __add_to_balance(self, value):
        self.lock.acquire()
        new_balance = self.balance+value
        if new_balance >= 0:
            self.balance = new_balance
            self.lock.release()
        else:
            self.lock.release()
            raise ValueError("Sorry, apparently we're not a real bank and you can't have a negative balance. Performing the action you asked for would result in a total balance of", new_balance)
