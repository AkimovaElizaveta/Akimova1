import xml.etree.ElementTree as ET

from exceptions.store_errors import StoreError
from models.author import Author
from models.book import Book
from models.customer import Customer
from services.store_service import StoreService
from storage.json_storage import JsonStorage
from storage.xml_storage import XmlStorage

JSON_FILE = "store.json"
XML_FILE = "store.xml"


def create_demo_store():
    store = StoreService()
    tolstoy = Author(1, "Лев Толстой", "Россия")
    bulgakov = Author(2, "Михаил Булгаков", "Россия")
    store.add_author(tolstoy)
    store.add_author(bulgakov)
    store.add_book(Book(1, "Война и мир", tolstoy, 450.0, "Роман", "epub"))
    store.add_book(Book(2, "Анна Каренина", tolstoy, 350.0, "Роман", "fb2"))
    store.add_book(Book(3, "Мастер и Маргарита", bulgakov, 300.0, "Роман", "pdf"))
    store.add_customer(Customer(1, "Иван Петров", "ivan@mail.ru", 1000.0))
    store.add_customer(Customer(2, "Анна Сидорова", "anna@mail.ru", 200.0))
    return store


def input_int(text):
    while True:
        try:
            return int(input(text))
        except ValueError:
            print("Ошибка: нужно ввести целое число")


def input_float(text):
    while True:
        try:
            return float(input(text))
        except ValueError:
            print("Ошибка: нужно ввести число")


def show_menu():
    print()
    print("===== Магазин цифровых книг =====")
    print("1 - Показать книги")
    print("2 - Показать покупателей")
    print("3 - Купить книгу")
    print("4 - Пополнить баланс")
    print("5 - Показать заказы")
    print("6 - Сохранить в JSON")
    print("7 - Загрузить из JSON")
    print("8 - Сохранить в XML")
    print("9 - Загрузить из XML")
    print("0 - Выход")


def show_books(store):
    print("Список книг:")
    for book in store.books:
        print(book.get_info())


def show_customers(store):
    print("Список покупателей:")
    for customer in store.customers:
        print(customer.get_info())
        if len(customer.library) == 0:
            print("   Купленных книг нет")
        for book in customer.library:
            print("   -", book.title)


def show_orders(store):
    if len(store.orders) == 0:
        print("Заказов пока нет")
    for order in store.orders:
        print(order.get_info())


def main():
    store = create_demo_store()
    json_storage = JsonStorage()
    xml_storage = XmlStorage()

    while True:
        show_menu()
        choice = input("Выберите пункт: ")
        try:
            if choice == "1":
                show_books(store)
            elif choice == "2":
                show_customers(store)
            elif choice == "3":
                customer_id = input_int("Номер покупателя: ")
                book_id = input_int("Номер книги: ")
                order = store.buy_book(customer_id, book_id)
                print("Покупка выполнена!")
                print(order.get_info())
            elif choice == "4":
                customer_id = input_int("Номер покупателя: ")
                amount = input_float("Сумма пополнения: ")
                customer = store.find_customer(customer_id)
                customer.add_funds(amount)
                print("Баланс пополнен. Сейчас:", customer.balance, "руб.")
            elif choice == "5":
                show_orders(store)
            elif choice == "6":
                json_storage.save(store, JSON_FILE)
                print("Данные сохранены в", JSON_FILE)
            elif choice == "7":
                store = json_storage.load(JSON_FILE)
                print("Данные загружены из", JSON_FILE)
            elif choice == "8":
                xml_storage.save(store, XML_FILE)
                print("Данные сохранены в", XML_FILE)
            elif choice == "9":
                store = xml_storage.load(XML_FILE)
                print("Данные загружены из", XML_FILE)
            elif choice == "0":
                print("До свидания!")
                break
            else:
                print("Нет такого пункта меню")
        except StoreError as error:
            print("Ошибка магазина:", error)
        except FileNotFoundError:
            print("Ошибка: файл не найден. Сначала сохраните данные")
        except ET.ParseError:
            print("Ошибка: XML-файл повреждён")
        except KeyError as error:
            print("Ошибка: в файле нет поля", error)
        except ValueError as error:
            print("Ошибка значения:", error)
        except Exception as error:
            print("Непредвиденная ошибка:", error)


main()




