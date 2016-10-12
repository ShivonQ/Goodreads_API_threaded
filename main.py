"""This class does the multi-threading with a single search keyword
Three different API calls from one key-word search with multi-threading"""
from Validator import *
from goodreads_client import goodreads_client as ap
import threading


def search_for_author(keyword):
    author_data = ap.author_by_name(keyword)
    print("ID: {}\nName: {}\nLink: {}\n".format(author_data['ID'], author_data['name'], author_data['link']))


def search_book(keyword):
    book_data = ap.all_books_by_author(keyword)
    print("book-search", book_data)


def search_book_title(keyword):
    book_data = ap.search(keyword)
    print("title-search ", book_data)


def main():
    keyword = get_string1_input("Enter the search keyword !!!")
    search_thread = threading.Thread(name='search', target=search_book, args=(keyword,))
    author_thread = threading.Thread(name='author_search', target=search_for_author, args=(keyword,))
    title_thread = threading.Thread(name='title', target=search_book_title, args=(keyword,))

    search_thread.run()
    author_thread.run()
    title_thread.run()

if __name__ == '__main__':
    main()
