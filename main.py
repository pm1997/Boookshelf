import tkinter as tk

from Database import Sqlite
from Book import Book, Series, getAllBooks


class MyFrame:

    def __init__(self, app: tk.Tk):
        self.name_var = tk.StringVar()
        app.title("Counting Seconds")
        button = tk.Button(app, text="Stop", width=25, command=app.destroy)
        edit1 = tk.Entry(
            app, textvariable=self.name_var, font=("calibre", 10, "normal")
        )
        button2 = tk.Button(app, text="test", width=25, command=self.on_press)

        button.grid(row=0, column=0)
        edit1.grid(row=1, column=0)
        button2.grid(row=2, column=0)

    def on_press(self):
        value = self.name_var.get()

        if value == "":
            print("You didn't enter anything!")
        else:
            print(f'You typed: "{value}"')


if __name__ == "__main__":

    db = Sqlite("data.sqlite")

    book1 = Book(db, "test", "a1")
    book2 = Book(db, "test32", "a2")
    book3 = Book(db, "test3", "a3")
    book4 = Book(db, "testt4", "a4")
    book5 = Book(db, "test5", "a5")
    book6 = Book(db, "test6", "a6")

    serie = Series([book1, book2, book3, Book(db, 1)])
    serie -= book2
    serie += book5

    print(serie.books())

    serie2 = serie + book6
    print(serie2.books())

    app = tk.Tk()

    frame = MyFrame(app)

    serie2.store()

    db.store()

    allBooks = getAllBooks(db)
    print(allBooks)
    #    if Shelf.Book("test4") in serie:
    if book3 in serie:
        print("ok")

    # db.clearDatabase()

# app.mainloop()
