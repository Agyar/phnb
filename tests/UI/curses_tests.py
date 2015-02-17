import sys
sys.path.insert(0, "../../src")
from UI.phnb_curses import *

phnb_curses = phnb_curses()
phnb_curses.init_ui()

phnb_curses._create_pad()
phnb_curses._make_textboxes()

key_handler = phnb_curses_keys_handler(phnb_curses)

#while (True):
""" version 1 """
    #key = phnb_curses._screen.getch()
    #if key == ord('q'):
        #break
""" version 2 """
    #if key_handler.get_key() == phnb_event.KEY_EXIT:
        #break

""" key displayer """
key = phnb_curses._screen.getch()
phnb_curses.end_ui()
print(key)


