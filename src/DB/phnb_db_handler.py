try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

class xml_handler:

    """ Provides phnb with the hnb-compatible xml data. """
    _db_file = ""
    _db = None
    _data = []

    def __init__(self, db_file):
        self._db_file = db_file

    def __iter__(self):
        """ format: (int, dict, string) """
        for node_tuple in self._data:
            yield node_tuple

    def load_db(self):
        self._db = ET.ElementTree(file=self._db_file)
        self._db = self._db.getroot()

    def fill_in(self, node=None, meta=None, level=0):
        if node == None:
            for child in self._db:
                self.fill_in(child)

        elif node.tag == 'data':
            self._data += [ (level, meta, node.text) ]

        elif node.tag == 'node':
            for child in node:
                self.fill_in(child, node.attrib, level+1)

    def export(self, db_file=None):
        if db_file is None:
            db_file = self._db_file
        root = ET.ElementTree(self._db)
        root.write(db_file)
