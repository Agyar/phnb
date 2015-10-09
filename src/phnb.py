#!/usr/bin/env python

from UI.phnb_curses import phnb_curses, phnb_event, phnb_curses_keys_handler
from DB.phnb_db_handler import xml_handler

# TODO not nice
import itertools
import curses

class phnb:

    def __init__(self, db, ui):
        self.db   = db
        self.ui   = ui
        self._csr = 0
        self._dl  = None
        self._register = None
        self._modified = True
        self.hide_done = False

    def update_db(self):
        if self._modified:
            dl = []
            gen = ( n for n in self.db._data )
            self._build_display_list(dl, gen)
            self.build_parents()
            self._dl = self._decorate_display_list(dl)
            self._modified = False

    def draw_phnb(self):
        self.update_db()

        self.ui.redraw()

        o_y, m_y, x = 2, 2, 2
        for level, meta, _p, _s, text in self._dl:
            if level == 1 and meta.get('expanded'):
                token = True
            elif level == 1:
                token = False
            if level == 1:
                self.ui.draw_line(80-x, m_y, x, _p+text, _s, '_main')
                m_y += 1
            elif token:
                self.ui.draw_line(80-x, o_y, x, _p+text, _s, '_c_one')
                if self.ui._active_panel == '_main':
                    self.ui.draw_line(80-x, o_y, x, _p+text, _s, '_c_one')
                else:
                    self.ui.draw_line(80-x, o_y, x, _p+text, _s, self.ui._active_panel)
                o_y += 1
                if o_y > 64:
                    return 
        self.ui._refresh_all()

    def expand(self):
        l, m, p, _, t = self._dl[self._csr]
        i = self.db.index((l,m,t))
        meta = m.copy()
        meta['expanded'] = 'yes'
        self.db._data[i] = (l, meta, t)
        self._dl[self._csr] = ( l, meta, p, curses.A_REVERSE, t)
        self._modified = True

    def collapse(self):
        l, m, _, _, t = self._dl[self._csr]
        i = self.db.index((l,m,t))
        meta = m.copy()
        if meta.get('expanded'):
            meta.pop('expanded')
        self.db._data[i] = (l, meta, t)
        self._modified = True

    def copy_node(self):
        l, m, _, _, t = self._dl[self._csr]
        i = self.db.index((l,m,t))
        self._register = self.db._data[i]
        return i

    def delete_node(self):
        i = self.copy_node()
        self.db._data.pop(i)
        self._modified = True

    def cut_node(self):
        i = self.copy_node()
        self.db._data.pop(i)
        self._modified = True

    def paste_node(self):
        l, m, _, _, t = self._dl[self._csr]
        i = self.db.index((l, m, t))
        if self._register:
            _, _m, _t = self._register
            self.db._data.insert(i+1, (l, _m, _t))
            self._csr+=1
        self._modified = True

    def make_todo(self):
        l, m, _, _, t = self._dl[self._csr]
        i = self.db.index((l,m,t))
        meta = m.copy()
        meta['type'] = 'todo'
        meta['done'] = 'no'
        self.db._data[i] = (l, meta, t)
        self._modified = True

    def make_node(self):
        l, m, _, _, t = self._dl[self._csr]
        i = self.db.index((l,m,t))
        meta = m.copy()
        if meta.get('type'):
            meta.pop('type')
            meta.pop('done')
        self.db._data[i] = (l, meta, t)
        self._modified = True

    def tick_done(self):
        l, m, _, _, t = self._dl[self._csr]
        i = self.db.index((l,m,t))
        meta = m.copy()
        meta['done'] = 'yes'
        self.db._data[i] = (l, meta, t)
        self._modified = True

    def untick_done(self):
        l, m, _, _, t = self._dl[self._csr]
        i = self.db.index((l,m,t))
        meta = m.copy()
        meta['done'] = 'no'
        self.db._data[i] = (l, meta, t)
        self._modified = True

    def switch_done(self):
        _, m, _, _, _ = self._dl[self._csr]
        if m.get('done') == 'yes':
            self.untick_done()
        elif m.get('done') == 'no':
            self.tick_done()
        else:
            self.make_todo()
            self.update_db()
            self.tick_done()

    def switch_type(self):
        _, m, _, _, _ = self._dl[self._csr]
        if m.get('type'):
            self.make_node()
        else:
            self.make_todo()

    def upgrade_nodes(self):
        l, m, _, _, t = self._dl[self._csr]
        i = self.db.index((l,m,t))
        # TODO not working, this will erase the part of the list that do not 
        #      answer the condition l > _l
        list_update = ((_l+1, _m, _t) for _l, _m, _t in self.db._data[i:])
        self.db._data[i:] = list(itertools.takewhile(lambda x: x[0] < l, list_update))
        self._modified = True

    def downgrade_nodes(self):
        pass

    def _move_csr_up(self):
        """ deprecated """
        if self._csr > 0:
            l, m, p, _, t = self._dl[self._csr]
            self._dl[self._csr] = ( l, m, p, curses.A_NORMAL, t ) 
            # TODO it is += 1 but rather a 'find next node of same 
            #      level, += 1 for each node in _dl between the two
            self._csr -= 1
            l, m, p, _, t = self._dl[self._csr]
            self._dl[self._csr] = ( l, m, p, curses.A_REVERSE, t)

    def _move_csr_up_by_lvl(self):
        if self._csr > 0:
            l, m, p, _, t = self._dl[self._csr]
            self._dl[self._csr] = ( l, m, p, curses.A_NORMAL, t ) 
                                                                   
            # assume prev item should be the prev in the list
            self._csr -= 1

            # _csr will be at least 0, no need to check

            # if assumption was wrong, go get this soab
            _l, _m, _p, _, _t = self._dl[self._csr]
            if _l != l:
                self.find_prev_brotha(l)
                _l, _m, _p, _, _t = self._dl[self._csr]

            # hilight elected item
            self._dl[self._csr] = ( _l, _m, _p, curses.A_REVERSE, _t)

    def find_prev_brotha(self, level):
        backup = self._csr
        self._dl.reverse()
        for l, _, _, _, _ in self._dl[0:backup]:
            self._csr -= 1
            if l == level:
                self._dl.reverse()
                return
            if l < level:
                self._dl.reverse()
                self._csr = backup+1
                return
        self._dl.reverse()
        self._csr = backup+1
        return

    def _move_csr_down_by_lvl(self):
        if self._csr < len(self._dl):
            l, m, p, _, t = self._dl[self._csr]
            self._dl[self._csr] = ( l, m, p, curses.A_NORMAL, t ) 

            # assume next item should be the next following
            self._csr += 1

            # in any case we should not go farther than the end
            if self._csr == len(self._dl):
                self._csr -= 1
                self._dl[self._csr] = ( l, m, p, curses.A_REVERSE, t ) 
                return

            # if next _csr is not of same level, then go find it
            _l, _m, _p, _, _t = self._dl[self._csr]
            if _l != l:
                self.find_next_brotha(l)
                _l, _m, _p, _, _t = self._dl[self._csr]

            # hilight our elected next item
            self._dl[self._csr] = ( _l, _m, _p, curses.A_REVERSE, _t)

    def find_next_brotha(self, level):
        backup = self._csr
        for l, _, _, _, _ in self._dl[self._csr:]:
            self._csr += 1
            if l == level:
                return 
            if l > level:
                self._csr = backup-1
                return 
        self._csr = backup-1
        return 

    def _move_csr_down(self):
        """ deprecated """
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
        l, m, t = dl[self._csr]
        for level, meta, text in dl:
            if (l,m,t) == (level, meta, text):
                # FIX THIS
                # TODO CAUTION this can also work for duplicated nodes
                style = curses.A_REVERSE
            else:
                style = curses.A_NORMAL
            if meta.get('type') == 'todo':
                if meta.get('done') == 'yes':
                    prefix = '[X] '
                else:
                    # TODO add computation of % completed mode
                    prefix = '[ ] '
            elif meta.get('expanded') and (level, meta, text) in self._parents_list:
                prefix = '- '
                style = curses.A_BOLD
            elif (level, meta, text) in self._parents_list:
                prefix = '+ '
                style = curses.A_BOLD
            else:
                prefix = '- '
            prefix = (level-2)*'    '+prefix
            _dl.append((level, meta, prefix, style, text))
        return _dl

    def _build_display_list(self, display_list, generator, level=1, expanded=False ):
        for _l, _m, _t in generator:
            if _l <= level:
                if (_m.get('done') == 'yes' and not self.hide_done) or _m.get('done') == 'no' or not _m.get('done'):
                    display_list.append((_l, _m, _t))
                if _m.get('expanded'):
                    self._build_display_list(display_list, generator, level+1, True)

    def switch_hide(self):
        if self.hide_done:
            self.hide_done = False
        else:
            self.hide_done = True
        self._modified = True

    def build_parents(self):
        hc = []
        _l, _m, _t = 0, None, None
        for l, m, t in self.db._data:
            if l > _l:
                hc.append((_l, _m, _t))
            _l, _m, _t = l, m, t
        self._parents_list = hc
