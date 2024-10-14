import time
from threading import Thread, Lock
from time import sleep
import random


class Bank:
    def __init__(self, balance):
        self.balance = balance
        self.lock = Lock()

    def deposit(self):
        for i in range(100):
            amount = random.randint(50, 500)
            with self.lock:
                self.balance += amount
                print(f'Пополнение: {amount}. Баланс: {self.balance}')
                if self.balance >= 500 and not self.lock.locked():
                    self.lock.release()
                time.sleep(0.001)

    def take(self):
        for i in range(100):
            amount = random.randint(50, 500)
            print(f'Запрос на {amount}')
            time.sleep(0.001)
            with self.lock:
                if amount <= self.balance:
                    self.balance -= amount
                    print(f'Снятие: {amount}. Баланс: {self.balance}')
                    time.sleep(0.001)
                else:
                    print('Запрос отклонён, недостаточно средств')
                    self.lock.acquire()
                    time.sleep(0.001)

bank = Bank(0)

deposit_thread = Thread(target=bank.deposit())
take_thread = Thread(target=bank.take())

deposit_thread.start()
take_thread.start()

deposit_thread.join()
take_thread.join()

print(f"Итоговый баланс: {bank.balance}")
