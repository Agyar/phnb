import sys
sys.path.insert(0, "../../src")
from UI.phnb_curses import *

from phnb import phnb

phnb_ui = phnb_curses()
phnb_ui.init_ui()

key_handler = phnb_curses_keys_handler(phnb_ui)

y, x = 2, 2

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

    elif k == phnb_event.KEY_DOWN:
        phnb._move_csr_down()

    elif k == phnb_event.KEY_RIGHT:
        phnb.expand()

    elif k == phnb_event.KEY_LEFT:
        phnb.collapse()

    elif k == phnb_event.KEY_SWITCH_DONE:
        phnb.switch_done()

    elif k == phnb_event.KEY_SWITCH_TYPE:
        phnb.switch_type()

    elif k == phnb_event.KEY_UPGRADE:
        phnb.upgrade_nodes()

    elif k == phnb_event.KEY_DOWNGRADE:
        phnb.upgrade_nodes()

    elif k == phnb_event.KEY_HIDE:
        phnb.switch_hide()

    elif k == phnb_event.KEY_DEL:
        phnb.delete_node()

    elif k == phnb_event.KEY_COPY:
        phnb.copy_node()

    elif k == phnb_event.KEY_CUT:
        phnb.cut_node()

    elif k == phnb_event.KEY_PASTE:
        phnb.paste_node()

    # elif k == phnb_event.KEY_CLEAR:

    elif k:
        phnb_ui._screen.addch(y, x, k, curses.A_NORMAL)
        x += 1
