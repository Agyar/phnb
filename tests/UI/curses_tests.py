import sys
sys.path.insert(0, "../../src")
from UI.phnb_curses import *
from DB.phnb_db_handler import xml_handler
from phnb import phnb

phnb_db = xml_handler("/home/ben/.hnb")
#phnb_db.load_db()
#phnb_db.fill_in()

phnb_ui = phnb_curses()
phnb_ui.init_ui()

key_handler = phnb_curses_keys_handler(phnb_ui)

phnb = phnb(phnb_db, phnb_ui)

#while (True):
""" version 1 """
    #key = phnb_curses._screen.getch()
    #if key == ord('q'):
        #break
""" version 2 """
    #if key_handler.get_key() == phnb_event.KEY_EXIT:
        #break

""" key displayer """
#key = phnb_curses._screen.getch()
#phnb_curses.end_ui()
#print(key)

y, x = 2, 2

phnb.draw_phnb()
while (True):
    k = key_handler.get_key()

    if k == phnb_event.KEY_EXIT:
        break

    elif k == phnb_event.KEY_TAB:
        if phnb_ui._active_panel == '_main':
            phnb_ui.switch_focus('_c_one')
        elif phnb_ui._active_panel == '_c_one':
            phnb_ui.switch_focus('_c_two')
        elif phnb_ui._active_panel == '_c_two':
            phnb_ui.switch_focus('_main')

    elif k == phnb_event.KEY_STAB:
        if phnb_ui._active_panel == '_main':
            phnb_ui.switch_focus('_c_two')
        elif phnb_ui._active_panel == '_c_one':
            phnb_ui.switch_focus('_main')
        elif phnb_ui._active_panel == '_c_two':
            phnb_ui.switch_focus('_c_one')

    elif k == phnb_event.KEY_RESIZE:
        # TODO
        break

    elif k == phnb_event.KEY_UP:
        phnb._move_csr_up()
        phnb.draw_phnb()

    elif k == phnb_event.KEY_DOWN:
        phnb._move_csr_down()
        phnb.draw_phnb()

    elif k == phnb_event.KEY_RIGHT:
        phnb.expand()
        phnb.draw_phnb()

    elif k == phnb_event.KEY_LEFT:
        phnb.collapse()
        phnb.draw_phnb()

    elif k == phnb_event.KEY_CLEAR:
        phnb.draw_phnb()

    elif k:
        #phnb_ui._screen.addstr(y, x, k, curses.A_REVERSE)
        phnb_ui._screen.addch(y, x, k, curses.A_NORMAL)
        #phnb_ui._refresh()
        x += 1
