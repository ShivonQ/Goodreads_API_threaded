from database import *

'''This is where the peewee model for a book will be stored'''

"""Make sure that this object stores the goodreads _id.  We will need it later.
    https://www.goodreads.com/search/index.xml?q=Ender&key=4ylN8OWi1dhG5Yhq3PQstA
    that will show you what types of data the server responds with."""

db = SqliteDatabase('PersonalLibrary.db')


class Base_Model(Model):
    class Meta:
        database = db


class book_model(Base_Model):
    id = CharField(max_length=60, unique=True)
    Title = CharField(max_length=120)
    Author_ID = CharField(max_length=100)
    Author_Name = CharField(max_length=100)


class author_model(Base_Model):
    name = CharField(max_length=70)
    id = IntegerField(unique=True)
    link = CharField()

