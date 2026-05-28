#%%
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Ui.ConsoleMenu import ConsoleMenu

class TestConsoleMenu :

    def test_display_title(self):
        menu = ConsoleMenu()
        menu.display_title()
    
    def test_process_choice(self):
        menu = ConsoleMenu()
       # menu.process_choice(choice="1")

        for i in range(1,5):
            chaine = str(i)
            menu.process_choice(chaine)
        

if __name__ == "__main__":
    test_menu = TestConsoleMenu()
    test_menu.test_display_title()
    test_ConsoleMenu = TestConsoleMenu()
    test_menu.test_process_choice()
# %%
