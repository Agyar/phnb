import curses

class phnb_curses:

    PAD_HEIGHT = 0
    PAD_WIDTH = 0

    _screen = None
    _pad = None
    _active_panel =  '_main'
    _panels = {
        # TODO determine them by computation
        '_main'  : {( 1,   0, 52, 46  )    :None},
        '_c_one' : {( 1,  48, 52, 128 )    :None},
        '_c_two' : {( 1, 130, 52, 210 )    :None}
    }

    def __init__(self, h=1080, w=1920):
        self.PAD_HEIGHT = h
        self.PAD_WIDTH = w
        self.init_ui()

    def init_ui(self):
        self._screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self._screen.keypad(1)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self._screen.bkgd(curses.color_pair(2))
        self._screen.refresh()
    
    def end_ui(self):
        curses.nocbreak()
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

        # not working "_v" does not exist ...
        #windows = [ w for p,w in _v.items() for _k,_v in self._panels.items() ]
        #for w in range(len(windows)):
            #windows[w].box()
            #windows[w].addstr(24, 24, 'I AM {0}'.format(list(self._panels.keys())[w]))
            #cy, cx = windows[w].getbegyx()
            #maxy, maxx = self._screen.getmaxyx()
            #self._pad.refresh(cy, cx, 1, maxx//2 - 110, maxy-1, maxx-1)

        for key, value in self._panels.items():
            for pos, win in value.items():
                win.box()
                win.addstr(24, 24, 'I AM {0}'.format(key))
                cy, cx = win.getbegyx()
                maxy, maxx = self._screen.getmaxyx()
                self._pad.refresh(cy, cx, 1, maxx//2 - 110, maxy-1, maxx-1)

        """ old ver """
        #windows = []
        #for k, dic in self._panels.items():
            #windows.append(self._pad.derwin(v[2], v[3]-v[1], v[0], v[1]))
        #for k in range(len(windows)):
            #windows[k].box()


            # TODO ONLY FOR TESTING PURPOSE HERE
            #windows[k].addstr(24, 24, 'I AM {0}'.format(list(self._panels.keys())[k]))
            #cy, cx = windows[k].getbegyx()
            #maxy, maxx = self._screen.getmaxyx()
            #self._pad.refresh(cy, cx, 1, maxx//2 - 110, maxy-1, maxx-1)


        #return windows

    def _csr_next_line(self, panel_name):
        """ returns a tuple on next position to write to """
        pass

    def switch_focus(self):
        """ hilight active window """
        #self._panels['active'].


        pass
        

class phnb_event:

    """ Constant table for phnb events. """
    KEY_UP       = 42 << 1
    KEY_DOWN     = 42 << 2
    KEY_RIGHT    = 42 << 3
    KEY_LEFT     = 42 << 4
    KEY_DEL      = 42 << 5
    KEY_CLEAR    = 42 << 6
    KEY_ENTER    = 42 << 7
    KEY_COPY     = 42 << 8
    KEY_PASTE    = 42 << 9
    KEY_CUT      = 42 << 10
    KEY_EXIT     = 42 << 11
    KEY_TAB      = 42 << 12
    KEY_STAB     = 42 << 13
    KEY_REDO     = 42 << 14

class phnb_curses_keys_handler:

    """ Curses keyboard events handler for phnb. """
    _event_db = {
        curses.KEY_UP       : phnb_event.KEY_UP,
        curses.KEY_DOWN     : phnb_event.KEY_DOWN,
        curses.KEY_RIGHT    : phnb_event.KEY_RIGHT,
        curses.KEY_LEFT     : phnb_event.KEY_LEFT,
        curses.KEY_DL       : phnb_event.KEY_DEL,
        curses.KEY_CLEAR    : phnb_event.KEY_CLEAR,
        curses.KEY_ENTER    : phnb_event.KEY_ENTER,
        #TODO replace this with ^q 
        ord('q')            : phnb_event.KEY_EXIT,
        9                   : phnb_event.KEY_TAB,
        353                 : phnb_event.KEY_STAB,
        24                  : phnb_event.KEY_CUT,
        22                  : phnb_event.KEY_PASTE,
        23                  : phnb_event.KEY_COPY,
        18                  : phnb_event.KEY_REDO,
    }

    _screen = None

    def __init__(self, phnb_curses):
        self._screen = phnb_curses._screen

    def get_key(self):
        _key = self._screen.getch()
        _isdb = self._event_db.get(_key)
        if _isdb:
            return _isdb

