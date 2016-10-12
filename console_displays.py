'''This is where all console display & menu strings will be stored'''


class menu_display:
    @staticmethod
    def main_menu():
        menu = ('\t1) Search a book\n'
                '\t2) Find an author by name\n'
                '\t3) Display all saved books\n'
                '\t4) Quit \n'
                '\nWhat do you want ??? : \n')
        return menu

    @staticmethod
    def sub_menu():
        sub_menu = (
            '\nSearch a Book\n'
            '\t1) By Author\n'
            '\t2) By ISBN\n'
            '\t3) By Title\n'
            '\t4) Back'
            '\nEnter Selection'
        )
        return sub_menu

    @staticmethod
    def initial_console_display():
        print('\033[1m' + '\033[94m' + "The Program starts here !!! " + '\033[0m')
        print("***************************")
        print("Menu : ")