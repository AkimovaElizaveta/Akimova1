class Author:
    def __init__(self, author_id, name, country):
        self.author_id = author_id
        self.name = name
        self.country = country

    def get_info(self):
        return f"{self.name} ({self.country})"

    class Book:
    def __init__(self, book_id, title, author, price, genre, file_format):
        if price < 0:
            raise ValueError("Цена книги не может быть отрицательной")
        self.book_id = book_id
        self.title = title
        self.author = author
        self.price = price
        self.genre = genre
        self.file_format = file_format

    def get_info(self):
        return (f"[{self.book_id}] {self.title} - {self.author.name}, "
                f"{self.genre}, {self.file_format}, {self.price} руб.")

    from exceptions.store_errors import NotEnoughMoneyError


class Customer:
    def __init__(self, customer_id, name, email, balance=0.0):
        if balance < 0:
            raise ValueError("Баланс не может быть отрицательным")
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.balance = balance
        self.library = []

    def add_funds(self, amount):
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть больше нуля")
        self.balance += amount

    def pay(self, amount):
        if amount > self.balance:
            raise NotEnoughMoneyError(self.balance, amount)
        self.balance -= amount

    def add_book(self, book):
        self.library.append(book)

    def has_book(self, book):
        for item in self.library:
            if item.book_id == book.book_id:
                return True
        return False

    def get_info(self):
        return f"[{self.customer_id}] {self.name}, {self.email}, баланс: {self.balance} руб."

    class Order:
    def __init__(self, order_id, customer, book, price, date):
        self.order_id = order_id
        self.customer = customer
        self.book = book
        self.price = price
        self.date = date

    def get_info(self):
        return (f"Заказ №{self.order_id}: {self.customer.name} купил "
                f"«{self.book.title}» за {self.price} руб. ({self.date})")
