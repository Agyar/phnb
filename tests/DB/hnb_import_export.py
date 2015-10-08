#!/usr/bin/env python

import sys
sys.path.insert(0, "../../src")
from DB.phnb_db_handler import xml_handler

xml_handler = xml_handler("/home/ben/.hnb")
#useless now, init call these from the start
# xml_handler.load_db()
# xml_handler.fill_in()

# xml_handler.export("test.xml")

""" display all informations we have """
#for level, meta, text in xml_handler:
    #print (level, meta, text)

""" sexy print text tabbed per level """
#for level, meta, text in xml_handler:
    #if meta == !None
        #print (" "*4*level, text)

""" sexy print text tabbed per level for finished task"""
#for level, meta, text in xml_handler:
    #if meta and meta['done'] == 'yes':
        #print ("    "*4*(level-1), text[0:79])

""" display text on level 1 """
for level, meta, text in xml_handler:
    if level == 1: 
        print (text)

""" display text and meta on level 1  """
for level, meta, text in xml_handler:
    if level == 1: 
        print (meta, text)
