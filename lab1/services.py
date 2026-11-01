from datetime import date

from exceptions.store_errors import (
    BookNotFoundError,
    CustomerNotFoundError,
    BookAlreadyPurchasedError,
)
from models.order import Order


class StoreService:
    def __init__(self):
        self.authors = []
        self.books = []
        self.customers = []
        self.orders = []

    def add_author(self, author):
        self.authors.append(author)

    def add_book(self, book):
        self.books.append(book)

    def add_customer(self, customer):
        self.customers.append(customer)

    def add_order(self, order):
        self.orders.append(order)

    def find_book(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                return book
        raise BookNotFoundError(book_id)

    def find_customer(self, customer_id):
        for customer in self.customers:
            if customer.customer_id == customer_id:
                return customer
        raise CustomerNotFoundError(customer_id)

    def buy_book(self, customer_id, book_id):
        customer = self.find_customer(customer_id)
        book = self.find_book(book_id)
        if customer.has_book(book):
            raise BookAlreadyPurchasedError(book.title)
        customer.pay(book.price)
        customer.add_book(book)
        order = Order(len(self.orders) + 1, customer, book, book.price,
                      date.today().isoformat())
        self.orders.append(order)
        return order
