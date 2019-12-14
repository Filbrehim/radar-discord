#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import tempfile
import time
import sys
import csv
import stat
import locale
sys.path.insert(1, 'lib')
import evenements
import timestamp
locale.setlocale(locale.LC_TIME, 'fr_FR.utf8')


def debut_test(titre,texte) :
	global crf
	print ('<H3>{0}</H3>{1}<pre>\n'.format(titre,texte),file=crf)

def fin_test(texte) :
	global crf
	print ('</pre>',file=crf) 
compterendu="/var/www/html/Discord" 
crf=tempfile.NamedTemporaryFile(dir=compterendu,suffix=".html",prefix="test-unitaire-",delete=False,mode="w")

print ("http://192.168.1.62/Discord/{0}\n".format(os.path.basename(crf.name)))
print ('<html> <head> <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/> <link rel="stylesheet" type="text/css" href="/style.css" />',file=crf)
print ('<title> test du {0}</title></head><body><li>{0}</li>'.format(time.strftime("%A %e %T")),file=crf)

## 
moi="test"
evt = evenements.event()
evt.annonceur = moi
for chemin in [ evt.annonceur+".dir" , evt.annonceur+".dir/"+evt.serveur+".dir" ] :
    if not os.path.isdir(chemin) : os.mkdir(chemin)

### VERSION API

print ("<li>version de l'API <tt>evenement</tt> : <b>{0}</b></li>".format(evt.apropos()),file=crf  )
debut_test("évènements","on liste des évènements")
#tous = evt.legacy_all_event()
#for e in tous :
#   print("le {0} : {1}".format(time.strftime("%A %e %H:%M",time.localtime(int(e))),tous[e]),file=crf)
ficevent="evenements.csv"
with open (ficevent) as csvfile :
    evtreader = csv.reader(csvfile,delimiter='|')
    for rangee in evtreader :
       r0 = int(rangee[0]) 
       evt.maj_event(r0,"titre",rangee[1])
       evt.maj_event(r0,"quoi",rangee[2])
       ## sword : &#9876; : beer : &#127866;
       if "Croisée" in rangee[1] : evt.maj_event(r0,"type","PVP")
       if "Orgrimmar" in rangee[1] : evt.maj_event(r0,"type","Roleplay") 
    csvfile.close()

liste = evt.scan_all_event()
for k in liste :
   print(k)
   print("le {0} : {1}".format(time.strftime("%A %e %H:%M",time.localtime(int(k))),liste[k]),file=crf)
   del liste[k]['titre']
   del liste[k]['quoi']
   for k2 in liste[k] : print (f"{k2} : {liste[k][k2]}")
fin_test("xx")

### TIMESTAMP

debut_test("timestamp","on déchiffre des timestamp d'unix")
print (timestamp.chercher("1234567890"),file=crf)
tmp_ts=timestamp.chercher(str(int(time.time())+3*86400))
print (tmp_ts,file=crf)
print ("""
	la chaine JSON
	sur plusieurs lignes
	...
""",file=crf) 
fin_test("xx")
for key,values in tmp_ts.items() :
	if key ==  'detail' :
		print("<li><b>{0}</b> <ul>".format(key),file=crf)
		for key,values in tmp_ts['detail'].items() :
			print("<li><b>{0}</b> : <tt>{1}</tt></li>".format(key,values),file=crf)
		print("</ul></li>",file=crf)
	else :
		print("<li><b>{0}</b> : <tt>{1}</tt></li>".format(key,values),file=crf)

print("</body></html>",file=crf)

### traintement fichier

crf.close()
os.chmod(crf.name,stat.S_IRWXU|stat.S_IRGRP|stat.S_IROTH)
os.unlink(compterendu + "/dernier-test.html")
os.link(crf.name , compterendu + "/dernier-test.html")

print("rm {0}/*".format(compterendu))

