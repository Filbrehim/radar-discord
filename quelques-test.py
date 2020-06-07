#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
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


def debut_test(titre,texte) :
	global crf
	print ('<H3>{0}</H3>{1}<pre>\n'.format(titre,texte),file=crf)

def fin_test(texte) :
	global crf
	print ('</pre>',file=crf) 

compterendu=os.environ['HOME']+"/public_html/Discord" 

crf=tempfile.NamedTemporaryFile(dir=compterendu,suffix=".html",prefix="test-unitaire-",delete=False,mode="w")

print ("http://192.168.1.62/Discord/{0}\n".format(os.path.basename(crf.name)))
print ('<html> <head> <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/> <link rel="stylesheet" type="text/css" href="/style.css" />',file=crf)
print ('<title> test du {0}</title></head><body><li>{0}</li>'.format(time.strftime("%A %e %T")),file=crf)

## 
moi="test"
evt = evenements.event()
evt.annonceur = moi
for chemin in [ evt.annonceur+".dir"  ] :
	if not os.path.isdir(chemin) : os.mkdir(chemin)

### VERSION API

print ("<li>version de l'API <tt>evenement</tt> : <b>{0}</b></li>".format(evt.apropos()),file=crf  )
debut_test("évènements","on liste des évènements")
#tous = evt.legacy_all_event()
#for e in tous :
#	print("le {0} : {1}".format(time.strftime("%A %e %H:%M",time.localtime(int(e))),tous[e]),file=crf)
ficevent="evenements.csv"
with open (ficevent) as csvfile :
	evtreader = csv.reader(csvfile,delimiter='|')
	for rangee in evtreader :
	   titre = str(rangee[0]+rangee[1])
	   r0 = "evt-"+hashlib.sha1(titre.encode('utf-8')).hexdigest() 
	   evt.maj_event(r0,"titre",rangee[1])
	   evt.maj_event(r0,"quoi",rangee[2])
	   evt.maj_event(r0,"_quand_unix",rangee[0])
	   evt.maj_event(r0,"quand",time.strftime("%A %e %H:%M",time.localtime(int(rangee[0]))))
	   ## sword : &#9876; : beer : &#127866;
	   if "Hurlevent" in rangee[1] : evt.maj_event(r0,"faction","Alliance")
	   if "Croisée" in rangee[1] : evt.maj_event(r0,"type","\u2694 PVP \u2694")
	   if "Orgrimmar" in rangee[1] : 
		   evt.maj_event(r0,"type","\U0001f37a Rôleplay "+chr(127866)) 
		   evt.maj_event(r0,"faction","Horde")
	csvfile.close()

liste = evt.scan_all_event_pour_quoi("auberge")
for k in liste :
   print(k)
   print("index {0} : {1}".format(k,liste[k]),file=crf)
   del liste[k]['titre']
   del liste[k]['quoi']
   ## for k2 in liste[k] : print (f"{k2} : {liste[k][k2]}")
print("<H5>Validation des jours</H5>",file=crf)
print("<li><b>{}</b> : <tt>{}</tt></li>".format('jeu',evt.valider_date('jeu')),file=crf)
print("<li><b>{}</b> : <tt>{}</tt></li>".format('darnivar',evt.valider_date('darnivar')),file=crf)
print("<li><b>{}</b> : <tt>{}</tt></li>".format('m',evt.valider_date('m')),file=crf)
fin_test("xx")

### PREFERENCES
pref = preferences.preference()
print ("<li>version de l'API <tt>preference</tt> : <b>{0}</b></li>".format(pref.apropos()),file=crf	 )
debut_test("préférence","on test les préférences utilisateur")
pref.annonceur = moi
tmp_p = pref.get_upref(128)
print(f"pref pour 128 : {tmp_p}",file=crf)
quoi='pigeon préféré' 
if tmp_p == None : tmp_p = dict() 
if quoi in tmp_p :
   if tmp_p[quoi] == "Asie" : tmp_p[quoi] = "Afrique"
   else : tmp_p[quoi] = "Asie"
   print(f"nouveau {quoi} : {tmp_p[quoi]}",file=crf)
else :
   tmp_p[quoi] = "Asie"
   print(f" pas de {quoi} : Arghhhh ",file=crf)

pref.set_upref(128,tmp_p)

pref.annonceur = "radar" 
pref.serveur = "570317142294003713"
pref.get_preference(False) 
tmp_p = pref.prefs
print(tmp_p) 

fin_test("xx")
### TIMESTAMP

print ("<li>version de l'API <tt>timestamp</tt> : <b>{0}</b></li>".format(timestamp.apropos()),file=crf	 )
debut_test("timestamp","on déchiffre des timestamp d'unix")
print (timestamp.chercher("1234567890"),file=crf)
print (timestamp.chercher(1534567890),file=crf)
print (timestamp.chercher(1734567890.1234),file=crf)
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
if os.path.isfile(compterendu + "/dernier-test.html") : os.unlink(compterendu + "/dernier-test.html")
os.link(crf.name , compterendu + "/dernier-test.html")

print("rm {0}/*".format(compterendu))

