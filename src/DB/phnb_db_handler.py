try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

class xml_handler:
    """ Provides phnb with the hnb-compatible xml data. """

    def __init__(self, db_file):
        self._data = []
        self._db_file = db_file
        self._load_db()
        self._fill_in()
        self._current_node = 0

    def __iter__(self):
        """ format: (int, dict, string) """
        for node_tuple in self._data:
            yield node_tuple

    def index(self, x):
        return self._data.index(x)

    def main_nodes(self):
        return ([(_m, _t)] for _l,_m,_t in self._data if _l == 1)

    def _load_db(self):
        self._db = ET.ElementTree(file=self._db_file)
        self._db = self._db.getroot()

    def _fill_in(self, node=None, meta=None, level=0):
        if node == None:
            for child in self._db:
                self._fill_in(child)

        elif node.tag == 'data':
            self._data += [ (level, meta, node.text) ]

        elif node.tag == 'node':
            for child in node:
                self._fill_in(child, node.attrib, level+1)

    def export(self, db_file=None):
        if db_file is None:
            db_file = self._db_file
        root = ET.ElementTree(self._db)
        root.write(db_file)
