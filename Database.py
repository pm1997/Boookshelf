import sqlite3
from typing import Iterable, Any


class DatabaseAdapter:
    def __init__(self):
        if not self.hasNeccessaryTables():
            self.initTables()

    def __del__(self):
        pass

    def executeSql(self, query: str, data_values: Iterable[Any]) -> None:
        pass

    def clearDatabase(self) -> None:
        pass

    def hasNeccessaryTables(self) -> bool:
        return True

    def initTables(self) -> None:
        pass

    def store(self) -> None:
        pass

    def getNextId(self, name: str) -> int:
        return 0

    def selectData(self, query: str, data_values: Any) -> list[Any]:
        return []

    def getAllIds(self, name: str) -> list[int]:
        if name in self.tableNames():
            result = self.selectData("SELECT id FROM " + name + " ;", [])
            return result
        return []

    def tableNames(self) -> list[str]:
        return ["Book", "Series", "BookToSeries"]


class Sqlite(DatabaseAdapter):
    def __init__(self, file: str):
        self.conn = sqlite3.connect(file)  # 'my_database.db' is the database file
        self.cursor = self.conn.cursor()
        super().__init__()

    def __del__(self):
        self.conn.close()

    def executeSql(self, query: str, data_values: Iterable[Any]) -> None:
        self.cursor.executemany(query, data_values)

    def initTables(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Book (
                id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                pages INTEGER
            );
        """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Series (
                id INTEGER PRIMARY KEY,
                name TEXT
            );
        """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS BookToSeries (
                id INTEGER PRIMARY KEY,
                bookId INTEGER ,
                seriesId INTEGER,
                position INTEGER,
                CONSTRAINT fk_book
                    FOREIGN KEY (bookId)
                    REFERENCES book(id),
                CONSTRAINT fk_series
                    FOREIGN KEY (seriesId)
                    REFERENCES series(id)
            );
        """
        )
        self.store()

    def getNextId(self, name: str) -> int:
        self.cursor.execute("SELECT COUNT(*) FROM " + name + ";")
        result = self.cursor.fetchone()
        return result[0]

    def clearDatabase(self) -> None:
        for table in self.tableNames():
            self.cursor.execute("DROP TABLE " + table + ";")

    def hasTable(self, name: str) -> bool:
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='" + name + "'"
        )
        result = self.cursor.fetchone()
        return result is not None

    def selectData(self, query: str, data_values: Any) -> list[Any]:
        self.cursor.execute(query, data_values)
        return self.cursor.fetchall()

    def hasNeccessaryTables(self) -> bool:
        return all(self.hasTable(table) for table in self.tableNames())

    # def initDml(self):
    #     self.cursor.execute(
    #         "INSERT INTO users (name, email) VALUES (?, ?)",
    #         ("Alice", "alice@example.com"),
    #     )
    #     self.cursor.execute(
    #         "INSERT INTO users (name, email) VALUES (?, ?)", ("Bob", "bob@example.com")
    #     )

    def store(self):
        self.conn.commit()
