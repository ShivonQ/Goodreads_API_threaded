"""This file will run the programs main loops, show the displays and generally
   bring together the other files into a cohesive unit"""
from tabulate import tabulate
from Validator import *
from goodreads_client import goodreads_client as ap
from database import *
from console_displays import menu_display
from peewee_models import *
import threading


def show_menu():
    """ displays the menu for the user
    checks if user has chosen the right choice from the list
    and calls methods to complete the action"""
    search_thread = threading.Thread(name='search', targer=search_book,)
    author_thread = threading.Thread(name='author_search', target=search_for_author)
    while True:
        menu = menu_display.main_menu()
        menu_choice = int(input(menu))
        while not is_whole_number(menu_choice, range(1, 4)):
            menu_choice = int(input("Invalid entry, please select from the list !!!"))
        if menu_choice == 1:
            search_book()
        if menu_choice == 2:
            search_for_author()
        if menu_choice ==3:
            displaySavedBooks()
        elif menu_choice == 4:
           exit(4)


def search_for_author():
    author_name = get_string1_input("find auther by name")
    author_data = ap.author_by_name(author_name)
    print("ID: {}\nName: {}\nLink: {}\n".format(author_data['ID'], author_data['name'], author_data['link']))
    insert_author_to_table(author_data)


def search_book():
    """Sub-menu for searching a book option."""
    menu_string = menu_display.sub_menu()
    while True:
        menu_choice = get_user_int(menu_string)
        if menu_choice == 1:
            try:
                keyword = get_string1_input('Enter author\'s name')
                search_from_api(keyword)
                break
            except Exception as e:
                print(" HERE - Error !!!", e)
        elif menu_choice == 2:
            keyword = get_string1_input("Enter ISBN for the book")
            search_from_api(keyword)
            break
        elif menu_choice == 3:
            keyword = get_string1_input("Enter the book-title")
            search_from_api(keyword)
            break
        elif menu_choice == 4:
            break
        else:
            print("Invalid input !!!")


def search_from_api(keyword):
    try:
        Books = ap.search(keyword)
        print("The books are:")
        print(tabulate(Books, tablefmt="fancy_grid"))
        for book in Books:
                insert_books_to_table(book)
    except Exception as e:
        print("API Error !!! ", e)


def main():
    db.connect()
    db.create_tables([book_model, author_model], safe=True)
    menu_display.initial_console_display()
    show_menu()


if __name__ == '__main__':
    main()
