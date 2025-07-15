from Database import DatabaseAdapter


class Book:

    def __init__(self, db: DatabaseAdapter, *args):  # type: ignore
        self.new = False
        self.db: DatabaseAdapter = db
        self.author: str = ""
        self.title: str = ""
        self.pages: int = 0
        self.id: int = 0
        if len(args) == 1:  # type: ignore
            self.id = args[0]
            self.author = ""
            self.title = ""
            self.pages = 0
        else:
            self.title = args[0]
            self.author = args[1]
            self.pages = 123
            self.id = self.db.getNextId("Book")
            self.new = True

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"Book(title='{self.title}', author='{self.author}', pages={self.pages})"

    def setId(self, new_id: int):
        self.id = new_id

    def store(self) -> None:
        if self.new:
            print("INSERT INTO users (name, email) VALUES (?, ?)")
        else:
            print("update")


class Series:
    def __init__(
        self,
        books: list[Book],
        db: DatabaseAdapter = None,  # type: ignore
    ):
        self.bookList: list[Book] = books
        self.db = db

    def __add__(self, book: Book):
        self.bookList.append(book)
        return self

    def __sub__(self, book: Book):
        self.bookList.remove(book)
        return self

    def __contains__(self, book: Book):
        return book in self.bookList

    def books(self):
        return self.bookList

    def store(self) -> None:
        for book in self.bookList:
            book.store()
        # todo:  store series itself
