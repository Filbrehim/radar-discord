#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import pickle
from pprint import pprint
import tempfile
import time
import sys
import csv
import stat
import locale
import hashlib
sys.path.insert(1, 'lib')
import evenements
import preferences
import timestamp
locale.setlocale(locale.LC_TIME, 'fr_FR.utf8')

def imprimer(p,indent=0) :
	if type(p) is dict :
		for k in p :
			if type(p[k]) is dict : 
				print(f"{k:17s} =>")
				imprimer(p[k],indent+1)
			else : 
				print(" "*indent*4+f"{k:17s} : {p[k]}")
	else :
		pprint(p) 
	
def dumper(fichier)  :
	if not os.path.isfile(fichier) :
		print (f"{fichier} n'a pas été trouvé")
		return
	with open(fichier,'rb') as f :
		print (f"dump de {fichier}")
		p = pickle.load(f)
		imprimer(p) 
		print("\n") 
		f.close()

for a in sys.argv[1:] :
	dumper(a)

