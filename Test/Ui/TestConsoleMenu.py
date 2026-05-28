#%%
from pathlib import Path
import builtins
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Ui.ConsoleMenu import ConsoleMenu


class TestConsoleMenu:

    def test_display_title(self):
        menu = ConsoleMenu()
        menu.display_title()

    def test_display_options(self):
        menu = ConsoleMenu()
        menu.display_options()

    def test_ask_choice(self):
        menu = ConsoleMenu()
        original_input = builtins.input
        builtins.input = lambda prompt: "3"
        try:
            choice = menu.ask_choice()
        finally:
            builtins.input = original_input

        print(choice)

    def test_login_ui(self):
        menu = ConsoleMenu()
        menu.login_ui()

    def test_add_place_ui(self):
        menu = ConsoleMenu()
        menu.add_place_ui()

    def test_display_places_ui(self):
        menu = ConsoleMenu()
        menu.display_places_ui()

    def test_display_tour_ui(self):
        menu = ConsoleMenu()
        menu.display_tour_ui()

    def test_process_choice(self):
        menu = ConsoleMenu()
        menu.process_choice("1")
        menu.process_choice("2")
        menu.process_choice("3")
        menu.process_choice("4")

    def test_process_choice_invalid(self):
        menu = ConsoleMenu()
        menu.process_choice("0")


if __name__ == "__main__":
    test_menu = TestConsoleMenu()
    test_menu.test_display_title()
    test_menu.test_display_options()
    test_menu.test_ask_choice()
    test_menu.test_login_ui()
    test_menu.test_add_place_ui()
    test_menu.test_display_places_ui()
    test_menu.test_display_tour_ui()
    test_menu.test_process_choice()
    test_menu.test_process_choice_invalid()

# %%
