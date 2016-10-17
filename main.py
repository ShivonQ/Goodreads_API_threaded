from goodreads_client import goodreads_client as ap
import threading
from queue import Queue
import time

"""This is taken from: - https://pythonprogramming.net/threading-tutorial-python/
  Reference given to me by - Anna Dudda !!!"""
""" This class does the book-search on the basis of four different keywords given using multi-threading"""

# putting a lock so that no other funtion can call it when other is using
print_lock = threading.Lock()


def search_books(search):
    book_data = ap.search(search)
    time.sleep(.5)  # pretend  do some work.
    with print_lock:
        print("I am the book_search \n", book_data)


# TODO: This is the wrong API cal I think.  author_by_name only yeilds author data not book data
def search_book_title(search):
    book_data = ap.author_by_name(search)
    with print_lock:
        print("I am the title_search \n", book_data)


def search_for_author(name):
    author_data = ap.author_by_name(name)
    time.sleep(1)
    with print_lock:
        print('search_for_author Thread')
        print('I found {}, hopefully that was what you were looking for.'.format(author_data['name']))
    #     must return the data so the next thread can use what was found.
    return author_data



def find_all_books_by_author(author_data):
    time.sleep(.5)
    a_id = author_data['ID']
    book_data = ap.all_books_by_author(a_id)
    with print_lock:
        print('find_all_books_by_author Thread')
        for entry in book_data:
            print(entry)
    q2.task_done()


def author_search_threader():
    # I created another threader to isolate the book queue from the author queue
    while True:
        # fetch a thread targeted at this threader
        author_search = q2.get()
        # catch the results of this first thread
        auth_data = search_for_author(author_search)
        # pass to the second thread
        find_all_books_by_author(auth_data)
        # alert queue that its done
        q2.task_done()


def book_search_threader():
    while True:
        # gets an worker from the queue
        searcher = q.get()
        # Run the example job with the avail worker in queue (thread)
        search_books(searcher)
        search_book_title(searcher)
        # completed with the job
        q.task_done()

q = Queue()
q2 = Queue()

# how many threads are we going to allow for
# TODO: put this whole threading portions into a function.
# So whena  user gives input it runs either these threads or the author ones
for x in range(5):
    book_search = threading.Thread(name='book-search', target=book_search_threader)
    author_search = threading.Thread(name='author_search', target=book_search_threader)
    # classifying as a daemon, so they will die when the main dies
    book_search.daemon = True
    author_search.daemon = True
    # begins, must come after daemon definition
    book_search.start()
    author_search.start()

for number in range(10):
    auth_by_name_thread = threading.Thread(name='author_search', target=author_search_threader)
    all_books_by_author_thread = threading.Thread(name='all_books_by_author', target=author_search_threader)
    # daemons be here
    auth_by_name_thread.daemon = True
    all_books_by_author_thread.daemon = True
    # start the thread waiting for their info
    auth_by_name_thread.start()
    all_books_by_author_thread.start()


start = time.time()
# list of random search string- can change it as per your choice
# TODO: REPLACE THIS WITH USER INPUTS. AND A CHOICE TO DO THREADING OPTION 1 or 2
search_string = ['Computer', 'Love', 'Music', 'Violence']
author_search_list = ['J.R.R. Tolkien','Ian C. Esslemont','Steven Erikson', 'Brandon Sanderson']

for search in search_string:
    q.put(search)
for param in author_search_list:
    q2.put(param)


# wait until the thread terminates.
q.join()
q2.join()

print('Entire job took:', time.time() - start)
