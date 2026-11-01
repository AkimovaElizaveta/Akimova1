import json

from models.author import Author
from models.book import Book
from models.customer import Customer
from models.order import Order
from services.store_service import StoreService


class JsonStorage:
    def save(self, store, filename):
        data = {
            "authors": [],
            "books": [],
            "customers": [],
            "orders": [],
        }
        for a in store.authors:
            data["authors"].append({
                "author_id": a.author_id,
                "name": a.name,
                "country": a.country,
            })
        for b in store.books:
            data["books"].append({
                "book_id": b.book_id,
                "title": b.title,
                "author_id": b.author.author_id,
                "price": b.price,
                "genre": b.genre,
                "file_format": b.file_format,
            })
        for c in store.customers:
            data["customers"].append({
                "customer_id": c.customer_id,
                "name": c.name,
                "email": c.email,
                "balance": c.balance,
                "library": [book.book_id for book in c.library],
            })
        for o in store.orders:
            data["orders"].append({
                "order_id": o.order_id,
                "customer_id": o.customer.customer_id,
                "book_id": o.book.book_id,
                "price": o.price,
                "date": o.date,
            })
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def load(self, filename):
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        store = StoreService()
        authors = {}
        for a in data["authors"]:
            author = Author(a["author_id"], a["name"], a["country"])
            authors[author.author_id] = author
            store.add_author(author)
        for b in data["books"]:
            author = authors[b["author_id"]]
            store.add_book(Book(b["book_id"], b["title"], author,
                                b["price"], b["genre"], b["file_format"]))
        for c in data["customers"]:
            customer = Customer(c["customer_id"], c["name"], c["email"], c["balance"])
            for book_id in c["library"]:
                customer.add_book(store.find_book(book_id))
            store.add_customer(customer)
        for o in data["orders"]:
            store.add_order(Order(o["order_id"],
                                  store.find_customer(o["customer_id"]),
                                  store.find_book(o["book_id"]),
                                  o["price"], o["date"]))
        return store


    import xml.etree.ElementTree as ET

from models.author import Author
from models.book import Book
from models.customer import Customer
from models.order import Order
from services.store_service import StoreService


def get_text(element, tag):
    child = element.find(tag)
    if child is None or child.text is None:
        raise ValueError(f"В XML нет элемента <{tag}>")
    return child.text


class XmlStorage:
    def save(self, store, filename):
        root = ET.Element("store")

        authors = ET.SubElement(root, "authors")
        for a in store.authors:
            item = ET.SubElement(authors, "author", id=str(a.author_id))
            ET.SubElement(item, "name").text = a.name
            ET.SubElement(item, "country").text = a.country

        books = ET.SubElement(root, "books")
        for b in store.books:
            item = ET.SubElement(books, "book", id=str(b.book_id))
            ET.SubElement(item, "title").text = b.title
            ET.SubElement(item, "author_id").text = str(b.author.author_id)
            ET.SubElement(item, "price").text = str(b.price)
            ET.SubElement(item, "genre").text = b.genre
            ET.SubElement(item, "file_format").text = b.file_format

        customers = ET.SubElement(root, "customers")
        for c in store.customers:
            item = ET.SubElement(customers, "customer", id=str(c.customer_id))
            ET.SubElement(item, "name").text = c.name
            ET.SubElement(item, "email").text = c.email
            ET.SubElement(item, "balance").text = str(c.balance)
            library = ET.SubElement(item, "library")
            for book in c.library:
                ET.SubElement(library, "book_id").text = str(book.book_id)

        orders = ET.SubElement(root, "orders")
        for o in store.orders:
            item = ET.SubElement(orders, "order", id=str(o.order_id))
            ET.SubElement(item, "customer_id").text = str(o.customer.customer_id)
            ET.SubElement(item, "book_id").text = str(o.book.book_id)
            ET.SubElement(item, "price").text = str(o.price)
            ET.SubElement(item, "date").text = o.date

        tree = ET.ElementTree(root)
        ET.indent(tree, space="    ")
        tree.write(filename, encoding="utf-8", xml_declaration=True)

    def load(self, filename):
        root = ET.parse(filename).getroot()

        store = StoreService()
        authors = {}
        for item in root.find("authors"):
            author = Author(int(item.get("id")), get_text(item, "name"),
                            get_text(item, "country"))
            authors[author.author_id] = author
            store.add_author(author)

        for item in root.find("books"):
            author = authors[int(get_text(item, "author_id"))]
            store.add_book(Book(int(item.get("id")), get_text(item, "title"),
                                author, float(get_text(item, "price")),
                                get_text(item, "genre"),
                                get_text(item, "file_format")))

        for item in root.find("customers"):
            customer = Customer(int(item.get("id")), get_text(item, "name"),
                                get_text(item, "email"),
                                float(get_text(item, "balance")))
            for book_id in item.find("library"):
                customer.add_book(store.find_book(int(book_id.text)))
            store.add_customer(customer)

        for item in root.find("orders"):
            store.add_order(Order(int(item.get("id")),
                                  store.find_customer(int(get_text(item, "customer_id"))),
                                  store.find_book(int(get_text(item, "book_id"))),
                                  float(get_text(item, "price")),
                                  get_text(item, "date")))
        return store
