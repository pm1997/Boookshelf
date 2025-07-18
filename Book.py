from Database import DatabaseAdapter


def bookId(db: DatabaseAdapter, title: str, author: str) -> int | None:
    results = db.selectData(
        "SELECT id FROM Book WHERE title=? AND author=?;",
        [title, author],
    )
    if len(results) == 0:
        return None
    return results[0][0]


def bookAlreadyExists(db: DatabaseAdapter, title: str, author: str) -> bool:
    return bookId(db, title, author) is not None


class Book:

    def __init__(self, db: DatabaseAdapter, *args):  # type: ignore
        self.new = False
        self.db: DatabaseAdapter = db
        self.author: str = ""
        self.title: str = ""
        self.pages: int = 0
        self.id: int = 0
        if len(args) == 1 and type(args[0]) == int:  # type: ignore
            self.id = args[0]
            self.refresh()
        elif len(args) > 1:  # type: ignore
            self.title = str(args[0])  # type: ignore
            self.author = str(args[1])  # type: ignore
            if bookAlreadyExists(self.db, self.title, self.author):
                self.id = bookId(db, self.title, self.author)  # type: ignore
                self.refresh()
            else:
                self.pages = 0
                self.id = self.db.getNextId("Book")
                self.new = True
                self.store()
        else:
            raise ValueError("Invalid arguments")

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"Book(title='{self.title}', author='{self.author}', pages={self.pages})"

    def setId(self, new_id: int):
        self.id = new_id

    def refresh(self) -> None:
        results = self.db.selectData(
            "SELECT title, author, pages FROM Book WHERE id=?;",
            [self.id],
        )
        assert len(results) == 1
        self.title = results[0][0]
        self.author = results[0][1]
        self.pages = results[0][2]

    def store(self) -> None:
        if self.new:
            self.new = False
            self.db.executeSql(  # type: ignore
                "INSERT INTO Book (id, title, author, pages) VALUES (?, ?, ?, ?)",
                [(self.id, self.title, self.author, self.pages)],
            )
        else:
            print("update")
            self.db.executeSql(  # type: ignore
                "UPDATE Book SET title=?, author=?, pages =? WHERE id=?",
                [(self.title, self.author, self.pages, self.id)],
            )


def getAllBooks(db: DatabaseAdapter) -> list[Book]:
    ids = db.getAllIds("Book")
    results: list[Book] = []
    for entry in ids:
        results.append(Book(db, entry[0]))
    return results


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
