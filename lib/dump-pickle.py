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

def dumper(fichier)  :
	if not os.path.isfile(fichier) :
		print (f"{fichier} n'a pas été trouvé")
		return
	with open(fichier,'rb') as f :
		print (f"dump de {fichier}")
		p = pickle.load(f)
		if type(p) is dict :
			for k in p :
				print(f"{k:17s} : {p[k]}")
		else :
			pprint(p) 
		f.close()
		print("\n") 

for a in sys.argv[1:] :
	dumper(a)

