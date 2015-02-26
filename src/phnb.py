#!/usr/bin/env python

from UI.phnb_curses import phnb_curses, phnb_event, phnb_curses_keys_handler
from DB.phnb_db_handler import xml_handler

# TODO not nice
import curses

class phnb:

    def __init__(self, db, ui):
        self.db   = db
        self.ui   = ui
        self._csr = 0
        self._dl  = None
        self._modified = True

    def draw_phnb(self):
        if self._modified:
            dl = []
            gen = ( n for n in self.db._data )
            self._build_display_list(dl, gen)
            self._dl = self._decorate_display_list(dl)
            self._modified = False

        self.ui.redraw()

        o_y, m_y, x = 2, 2, 2
        for level, meta, _p, _s, text in self._dl:
            if level == 1 and meta.get('expanded'):
                token = True
            elif level == 1:
                token = False
            if level == 1:
                self.ui.draw_line(80, m_y, x, _p+text, _s, '_main')
                m_y += 1
            elif token:
                #self.ui.draw_line(80, o_y, x, _p+text, _s, '_c_one')
                if self.ui._active_panel == '_main':
                    self.ui.draw_line(80, o_y, x, _p+text, _s, '_c_one')
                else:
                    self.ui.draw_line(80, o_y, x, _p+text, _s, self.ui._active_panel)
                o_y += 1
        self.ui._refresh_all()
    
    def expand(self):
        l, m, _, _, t = self._dl[self._csr]
        i = self.db.index((l,m,t))
        meta = m.copy()
        meta['expanded'] = 'yes'
        self.db._data[i] = (l, meta, t)
        self._modified = True

    def collapse(self):
        l, m, _, _, t = self._dl[self._csr]
        i = self.db.index((l,m,t))
        meta = m.copy()
        if meta.get('expanded'):
            meta.pop('expanded')
        self.db._data[i] = (l, meta, t)
        self._modified = True

    def make_todo(self):
        l, m, _, _, t = self._dl[self._csr]
        i = self.db.index((l,m,t))
        meta = m.copy()
        meta['type'] = 'todo'
        meta['done'] = 'no'
        self.db._data[i] = (l, meta, t)

    def make_node(self):
        l, m, _, _, t = self._dl[self._csr]
        i = self.db.index((l,m,t))
        meta = m.copy()
        if meta.get('type'):
            meta.pop('type')
            meta.pop('done')
        self.db._data[i] = (l, meta, t)

    def tick_done(self):
        l, m, _, _, t = self._dl[self._csr]
        i = self.db.index((l,m,t))
        meta = m.copy()
        meta['done'] = 'yes'
        self.db._data[i] = (l, meta, t)

    def untick_done(self):
        l, m, _, _, t = self._dl[self._csr]
        i = self.db.index((l,m,t))
        meta = m.copy()
        meta['done'] = 'no'
        self.db._data[i] = (l, meta, t)

    def _move_csr_up(self):
        if self._csr > 0:
            l, m, p, _, t = self._dl[self._csr]
            self._dl[self._csr] = ( l, m, p, curses.A_NORMAL, t ) 
            # TODO it is += 1 but rather a 'find next node of same 
            #      level, += 1 for each node in _dl between the two
            self._csr -= 1
            l, m, p, _, t = self._dl[self._csr]
            self._dl[self._csr] = ( l, m, p, curses.A_REVERSE, t)

    def _move_csr_down(self):
        if self._csr < len(self._dl):
            l, m, p, _, t = self._dl[self._csr]
            self._dl[self._csr] = ( l, m, p, curses.A_NORMAL, t ) 
            # TODO it is += 1 but rather a 'find next node of same 
            #      level, += 1 for each node in _dl between the two
            self._csr += 1
            l, m, p, _, t = self._dl[self._csr]
            self._dl[self._csr] = ( l, m, p, curses.A_REVERSE, t)

    def _decorate_display_list(self, dl):
        _dl = []
        for level, meta, text in dl:
            style = curses.A_NORMAL
            if meta.get('type') == 'todo':
                # TODO adapt this
                #style = curses.A_BOLD
                if meta.get('done') == 'yes':
                    prefix = '[X] '
                else:
                    # TODO add computation of % completed mode
                    prefix = '[ ] '
            elif meta.get('expanded'):
                prefix = '- '
            else:
                prefix = '+ '
            prefix = (level-2)*'    '+prefix
            _dl.append((level, meta, prefix, style, text))
        return _dl

    def _build_display_list(self, display_list, generator, level=1, expanded=False ):
        for _l, _m, _t in generator:
            if _l <= level:
                display_list.append((_l, _m, _t))
                if _m.get('expanded'):
                    self._build_display_list(display_list, generator, level+1, True)
