'''This is where the database routes will go.  Since it will be using peewee it should be very few routes.'''
from peewee import *
from peewee_models import *
from tabulate import tabulate

# db = SqliteDatabase('PersonalLibrary.db')
# db.connect()
# db.create_tables([book_model, author_model], safe=True)


def insert_author_to_table(author_data):
    author_new = author_model.create(name=author_data['name'], id=author_data['ID'],  link=author_data['link'])
    author_new.save()


def insert_books_to_table(books):
    new_Books = book_model.create(id=books['id'], Title=books['title'], Author_ID=books['auth_id'], Author_Name=books['author_name'])
    new_Books.save()


def displaySavedBooks():
    big_books = []
    for book in book_model:
        small = compile_record(book)
        big_books.append(small)
    #      print(tabulate(Books, tablefmt="fancy_grid", headers=['Author', 'Author ID', 'Title', 'Book ID']))
    print(tabulate(big_books, tablefmt="fancy_grid", headers=["Author", "Author ID", "Title", "Book ID"]))


def compile_record(record):
    small_list = [record.Author_Name,record.Author_ID,record.Title,record.id]
    return small_list