import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget

from Form import Ui_Form


class Book:
    def __init__(self, title, author, year, genre, image_link):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.image_link = image_link if image_link else 'default.png'


class MyWidget(QWidget, Ui_Form):
    def __init__(self, book: Book):
        super().__init__()
        self.setupUi(self)

        self.title.setText(book.title)
        self.genre.setText(book.genre)
        self.year.setText(str(book.year))
        self.author.setText(book.author)

        pixmap = QPixmap(book.image_link).scaled(160, 240)
        self.image.setPixmap(pixmap)
