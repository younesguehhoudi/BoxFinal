from Data.Models import initialize_database
from Ui.ConsoleMenu import ConsoleMenu

def main():
    initialize_database()
    menu = ConsoleMenu()
    menu.run()

if __name__ == "__main__":
    main()