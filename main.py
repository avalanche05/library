import sys

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

import book
from MainWindow import Ui_MainWindow
import sqlite3

DB_NAME = 'library.db'


def get_genre() -> dict:
    con = sqlite3.connect(DB_NAME)

    cur = con.cursor()

    result = cur.execute("""SELECT * FROM genre""").fetchall()

    con.close()
    return {elem[0]: elem[1] for elem in result}


class Book:
    def __init__(self, title, author, year, genre, image_link):
        genres = get_genre()
        self.title = title
        self.author = author
        self.year = year
        self.genre = genres[genre]
        self.image_link = image_link if image_link else 'default.png'


def get_books() -> list:
    con = sqlite3.connect(DB_NAME)

    cur = con.cursor()

    result = cur.execute("""SELECT * FROM book""").fetchall()

    ans = []
    for elem in result:
        ans.append(Book(*elem[1:]))

    con.close()
    return ans


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.listView.clicked.connect(self.open_book)

        self.books = get_books()

        self.comboBox.addItems(['автор', 'название'])

        self.pushButton.clicked.connect(self.search)

    def get_book(self, title: str):
        for elem in self.books:
            if elem.title == title:
                return elem

    def search(self):
        self.listView.clear()
        find_books = []
        text = self.lineEdit.text()

        if self.comboBox.currentText() == 'автор':
            for i in range(len(self.books)):
                if text.replace(' ', '').lower() in self.books[i].author.replace(' ', '').lower():
                    find_books.append((i, self.books[i]))

        for b in find_books:
            button = QPushButton()
            button.setText(b[1].title)

            self.listView.addItem(b[1].title)

    def open_book(self, event: QtCore.QModelIndex):
        book_fnd = self.get_book(event.data())

        self.book_dialog = book.MyWidget(book_fnd)
        self.book_dialog.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
