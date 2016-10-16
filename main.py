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


def search_book_title(search):
    book_data = ap.author_by_name(search)
    with print_lock:
        print("I am the title_search \n", book_data)

def search_for_author(name):
    author_data = ap.author_by_name(name)
    time.sleep(.5)
    with print_lock:
        print('I found {}, hopefully that was what you were looking for.'.format(author_data['name']))
    #     must return the data so the next thread can use what was found.
    return author_data


def all_books_by_author(author_data):
    book_data = ap.all_books_by_author(author_data['id'])
    with print_lock:
        for entry in book_data:
            print(book_data)

# I created another threader to isolate the book queue from the author queue
def author_search_threader():
    while True:
        author_search = q.get()



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

# how many threads are we going to allow for
for x in range(5):
    book_search = threading.Thread(name='book-search', target=book_search_threader)
    author_search = threading.Thread(name='author_search', target=book_search_threader)
    # classifying as a daemon, so they will die when the main dies
    book_search.daemon = True
    author_search.daemon = True
    # begins, must come after daemon definition
    book_search.start()
    author_search.start()

start = time.time()
# list of random search string- can change it as per your choice
# TODO: REPLACE THIS WITH USER INPUTS. AND A CHOICE TO DO THREADING OPTION 1 or 2
search_string = ['Computer', 'Love', 'Music', 'Violence']
for search in search_string:
    q.put(search)

# wait until the thread terminates.
q.join()

print('Entire job took:', time.time() - start)