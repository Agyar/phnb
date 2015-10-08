import curses

class phnb_curses:

    """ Note: in curses, width is y, height is x """
    def __init__(self, w=1920, h=1080):
        self.PAD_HEIGHT = h
        self.PAD_WIDTH = w
        self._mode      = 'extended'
        self._panels = {}
        self.MIN_SIZE_CVIEW = 212
        self._C_WIDTH = 80
        self._C_HEIGHT = 54
        self._M_WIDTH = 50
        self.init_ui()

    def init_ui(self):
        self._screen = curses.initscr()
        curses.noecho()
        curses.raw()
        curses.curs_set(0)
        self._screen.keypad(1)

        self._create_pad()
        self._define_colors()

        self.SCR_HEIGHT, self.SCR_WIDTH = self._screen.getmaxyx()
        if self.SCR_WIDTH < self.MIN_SIZE_CVIEW :
            self._mode = 'vanilla'
        else:
            self._active_panel    =  '_main'
            self._panels = {
                    # win name : {( start x, start y, end x, end y) : win obj}
                    '_main'  : {( 1,   0, self.SCR_HEIGHT, 46  )    :None},
                    '_c_one' : {( 1,  47, self.SCR_HEIGHT, 129 )    :None},
                    '_c_two' : {( 1, 130, self.SCR_HEIGHT, 212 )    :None}
            }
            self._make_textboxes()
        self._screen.refresh()

    def _define_colors(self):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_CYAN, curses.COLOR_BLACK)

        curses.init_pair(8, curses.COLOR_WHITE,  curses.COLOR_BLACK)
        curses.init_pair(9, curses.COLOR_WHITE,  curses.COLOR_RED)
        curses.init_pair(10,curses.COLOR_BLACK,  curses.COLOR_GREEN)
        curses.init_pair(11,curses.COLOR_BLACK,  curses.COLOR_YELLOW)
        curses.init_pair(12,curses.COLOR_BLACK,  curses.COLOR_BLUE)
        curses.init_pair(13,curses.COLOR_WHITE,  curses.COLOR_MAGENTA)
        curses.init_pair(14,curses.COLOR_WHITE,  curses.COLOR_CYAN)

        self._active_color = curses.color_pair(1)
        self._inactive_color = curses.color_pair(8)
    
    def end_ui(self):
        curses.noraw()
        self._screen.keypad(0)
        curses.echo()
        curses.endwin()

    def _create_pad(self):
        self._pad = curses.newpad(self.PAD_HEIGHT, self.PAD_WIDTH)
        self._pad.box()

    def _make_textboxes(self):
        for window_name, attrs in self._panels.items():
            for pos, win in attrs.items():
                self._panels[window_name][pos] = self._pad.derwin(
                        pos[2], pos[3]-pos[1], pos[0], pos[1])

        for key, value in self._panels.items():
            for pos, win in value.items():
                win.box()
                win.bkgd(self._inactive_color)
                # win.addstr(24, 24, 'I AM {0}'.format(key))
        self._get_win().bkgd(self._active_color)
        self._refresh_all()

    def redraw(self):
        self._pad.erase()
        self._make_textboxes()

    def _get_win(self, win_name=None):
        if win_name is None:
            win_name = self._active_panel
        curr = [ w for p,w in self._panels[win_name].items()]
        return curr[0]

    def _refresh_all(self):
        self._pad.refresh(1, 0, 0, 0, 
                self.SCR_HEIGHT-1, self.SCR_WIDTH-1)
    
    def _refresh(self, win):
        cy, cx = win.getbegyx()
        maxy, maxx = self._screen.getmaxyx()
        # TODO pimp by _pad sizes .  . <- here
        self._pad.refresh(cy, cx, 0, 0, 
                self.SCR_HEIGHT-1, self.SCR_WIDTH-1)

    def _csr_next_line(self):
        """ returns a tuple on next position to write to """
        pass

    def draw_line(self, limit, y, x, text, style, win=None):
        """ write one textline to active panel """
        self._get_win(win).addnstr(y, x, text, limit, style)

    def switch_focus(self, panel_name):
        """ hilight active window """
        self._get_win().bkgd(self._inactive_color)
        self._get_win(panel_name).bkgd(self._active_color)
        self._active_panel = panel_name
        self._refresh_all()

class phnb_event:

    """ Constant table for phnb events. """
    KEY_UP            = 42 << 1
    KEY_DOWN          = 42 << 2
    KEY_RIGHT         = 42 << 3
    KEY_LEFT          = 42 << 4
    KEY_DEL           = 42 << 5
    KEY_CLEAR         = 42 << 6
    KEY_ENTER         = 42 << 7
    KEY_COPY          = 42 << 8
    KEY_PASTE         = 42 << 9
    KEY_CUT           = 42 << 10
    KEY_EXIT          = 42 << 11
    KEY_TAB           = 42 << 12
    KEY_STAB          = 42 << 13
    KEY_REDO          = 42 << 14
    KEY_SAVE          = 42 << 15
    KEY_RESIZE        = 42 << 16
    KEY_SWITCH_TYPE   = 42 << 17
    KEY_SWITCH_DONE   = 42 << 18
    KEY_UPGRADE       = 42 << 19
    KEY_DOWNGRADE     = 42 << 20
    KEY_SWITCH        = 42 << 21
    KEY_HIDE          = 42 << 22

class phnb_curses_keys_handler:

    """ Curses keyboard events handler for phnb. """
    _event_db = {
        curses.KEY_UP       : phnb_event.KEY_UP,
        curses.KEY_DOWN     : phnb_event.KEY_DOWN,
        curses.KEY_RIGHT    : phnb_event.KEY_RIGHT,
        curses.KEY_LEFT     : phnb_event.KEY_LEFT,
        330                 : phnb_event.KEY_DEL,
        curses.KEY_CLEAR    : phnb_event.KEY_CLEAR,
        curses.KEY_ENTER    : phnb_event.KEY_ENTER,
        17                  : phnb_event.KEY_EXIT,
        9                   : phnb_event.KEY_TAB,
        353                 : phnb_event.KEY_STAB,
        24                  : phnb_event.KEY_CUT,
        22                  : phnb_event.KEY_PASTE,
        3                  : phnb_event.KEY_COPY,
        18                  : phnb_event.KEY_REDO,
        19                  : phnb_event.KEY_SAVE,
        curses.KEY_RESIZE   : phnb_event.KEY_RESIZE,
        20                  : phnb_event.KEY_SWITCH_TYPE,
        4                   : phnb_event.KEY_SWITCH_DONE,
        62                  : phnb_event.KEY_UPGRADE,
        60                  : phnb_event.KEY_DOWNGRADE,
        15                  : phnb_event.KEY_SWITCH,
        127                 : phnb_event.KEY_HIDE,
    }

    def __init__(self, phnb_curses):
        self._screen = phnb_curses._screen

    def get_key(self):
        _key = self._screen.getch()
        _isdb = self._event_db.get(_key)
        if _isdb:
            return _isdb
        return _key
