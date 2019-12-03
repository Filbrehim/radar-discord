
#!/usr/bin/python
#-*- coding: utf-8 -*-
#  donne les events

import csv

"""Module event """
def get_all_event()  :
    event = dict()
    with open("evenements.csv","r") as eventf :
        lireevt = csv.reader(eventf,delimiter="|")
        for ligne in lireevt :
            event[ligne[0]]=ligne[1]
    return event ;

def apropos() :
	"""donne la version"""
	return "1."
