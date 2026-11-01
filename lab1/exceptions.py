class StoreError(Exception):
    """Базовое исключение магазина цифровых книг"""

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class BookNotFoundError(StoreError):
    def __init__(self, book_id):
        super().__init__(f"Книга с номером {book_id} не найдена")
        self.book_id = book_id


class CustomerNotFoundError(StoreError):
    def __init__(self, customer_id):
        super().__init__(f"Покупатель с номером {customer_id} не найден")
        self.customer_id = customer_id


class NotEnoughMoneyError(StoreError):
    def __init__(self, balance, price):
        super().__init__(f"Недостаточно средств: на счёте {balance}, нужно {price}")
        self.balance = balance
        self.price = price


class BookAlreadyPurchasedError(StoreError):
    def __init__(self, title):
        super().__init__(f"Книга «{title}» уже куплена")
        self.title = title
