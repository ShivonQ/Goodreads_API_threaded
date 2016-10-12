'''This file will be where the goodreads magic happens, more to come later'''
import requests
import xml.etree.ElementTree as ET
from secret_key import secret_key


class goodreads_client():
    def __init__(self):
        self.secret_key = secret_key

    @staticmethod
    def search(parameter):
        try:
            # We construct a URL to send to The Goodreads API.  In this case it will take our key, and a
            # search parameter, either a Author, ISBN, or title. in my example file 'test_client.py'
            # you will see that I send the parameter 'Ender' and get a bucnh of weird HTML tags back.
            base_url = 'https://www.goodreads.com/search/index.xml?q='+parameter+'&key='+secret_key
            # An API call MUST be use .post not .get, because that tells the server we expect something back.
            response = requests.post(base_url)
            # here we make an Element Form of our XML so we can iterate through it to get information
            dict_form = ET.fromstring(response.text)
            # This should let me iterate through and get what I want.
            results = parse_best_books(dict_form)
            return results
        except Exception as e:
            print("Invalid search keyword !!! ", e)

    @staticmethod
    def all_books_by_author(auth_id):
        try:
            base_url = 'https://www.goodreads.com/series/list/'+auth_id+'.xml?key='+secret_key
            response = requests.post(base_url)
            dict_form = ET.fromstring(response.text)
            results = parse_best_books(dict_form)
            return results
        except:
            return " No author found with that ID"


    @staticmethod
    def author_by_name(author_name):
        try:
            base_url = 'https://www.goodreads.com/api/author_url/' + author_name + '?key=' + secret_key
            respond = requests.get(base_url)
            dict_form = ET.fromstring(respond.text)
            print("Dictionary", dict_form[1].attrib['id'])
            result = parse_author(dict_form)
            return result
        except Exception as e:
            print("Invalid author-name !!!", e)


    @staticmethod
    def author_result_to_list(author_data):
        list_form = []
        for key, value in author_data.items():
            list_form.append(value)
        print(list_form)

    @staticmethod
    def get_author_info_by_id(author_id):
        base_url = 'https://www.goodreads.com/author/show.xml ' + author_id + '?key=' + secret_key
        respond = requests.get(base_url)
        dict_form = ET.fromstring(respond.text)
        print("Dictionary", dict_form[1].attrib['id'])
        result = parse_author(dict_form)
        return result


def parse_author(dict_form):
    author = {'ID': dict_form[1].attrib['id'], 'name':dict_form[1][0].text, 'link': dict_form[1][1].text}
    return author


def parse_best_books(dict_form):
    all_books = []
    for best_book in dict_form.iter('best_book'):
        # Load up blank dictionary to store book data
        book = {'id': 0, 'title': '', 'auth_id': 0, 'author_name': ''}

        '''Due to the structure of the XML parsed by the Element-tree we have to iterate this way to get our data.
           All other methods I tried failed, and this one yields positive results.'''

        for id in best_book.findall('id'):
            book['id'] = id.text
        for title in best_book.findall('title'):
            book['title'] = title.text
        for author_info in best_book.findall('author'):
            book['auth_id'] = author_info.find('id').text
            book['author_name'] = author_info.find('name').text
        #     This part could be reinserted at a later time if image support was a thing
        # for image_url in best_book.findall('image_url'):
        #     book['image'] = image_url.text
        all_books.append(book)
    return all_books
