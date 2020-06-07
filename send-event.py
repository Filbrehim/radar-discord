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

compterendu="/var/www/html/Discord" 

crf=tempfile.NamedTemporaryFile(dir=compterendu,suffix=".html",prefix="test-unitaire-",delete=False,mode="w")
rssf=open(compterendu+"/rss.xml",mode="w")

print ('<rss version="2.0">\n<channel>',file=rssf)
print ('\t<title>test event</title>\n\t<description>test des events frezza</description>',file=rssf)
print ('<html> <head> <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/> <link rel="stylesheet" type="text/css" href="/style.css" />',file=crf)
print ('<title> test du {0}</title></head><body><li>{0}</li>'.format(time.strftime("%A %e %T")),file=crf)

## 
moi="frezza"
evt = evenements.event()
evt.annonceur = moi
for chemin in [ evt.annonceur+".dir"  ] :
        if not os.path.isdir(chemin) : os.mkdir(chemin)

### VERSION API

sdao = "SDAO"
wow_classic = "WoW Classic"
wow = "WoW Retail"
royaume = { "sirannon" : sdao , "auberdine" : wow_classic , "kirin-tor" : wow }
roleplay = { "auberge" , "taverne" , "jdr" }
fight = { "raid", "donjon" , "jcj" , "pvp" }
debut_test("évènements","on liste des évènements")
ficevent="evenements.csv"
with open (ficevent) as csvfile :
        evtreader = csv.reader(csvfile,delimiter='|')
        for rangee in evtreader :
           print(f'\t\t<item><title>{rangee[1]}</title><description>{rangee[2]}</description></item>',file=rssf)
           titre = str(rangee[0]+rangee[1])
           r0 = "evt-"+hashlib.sha1(titre.encode('utf-8')).hexdigest() 
           evt.maj_event(r0,"titre",rangee[1])
           evt.maj_event(r0,"quoi",rangee[2])
           evt.maj_event(r0,"_quand_unix",rangee[0])
           evt.maj_event(r0,"quand",time.strftime("%A %e %H:%M",time.localtime(int(rangee[0]))))
           for chaine in rangee[1].split() :
              if chaine.lower() in roleplay :
                 evt.maj_event(r0,"type", chr(127866) + " " + chaine + " " + chr(127866))
           for chaine in rangee[2].split() :
              if chaine.lower() in roleplay :
                 evt.maj_event(r0,"type", chr(127866) + " " + chaine + " " + chr(127866))
           for chaine in rangee[3].split() :
              if chaine.lower() in royaume :
                 evt.maj_event(r0,"royaume",royaume[chaine.lower()] + " " + chaine) 
              if chaine.lower() in fight :
                 evt.maj_event(r0,"type", chr(9876) + " " + chaine + " " + chr(9876))
              if chaine.lower() in roleplay :
                 evt.maj_event(r0,"type", chr(127866) + " " + chaine + " " + chr(127866))

           ## sword : &#9876; : beer : &#127866;
           if "Hurlevent" in rangee[1] : evt.maj_event(r0,"faction","Alliance")
           if "Croisée" in rangee[1] : evt.maj_event(r0,"type","\u2694 PVP \u2694")
           if "Orgrimmar" in rangee[1] : 
                   evt.maj_event(r0,"type","\U0001f37a Rôleplay "+chr(127866)) 
                   evt.maj_event(r0,"faction","Horde")
        csvfile.close()

liste = evt.scan_all_event()
for k in liste :
   print(k)
   print("index {0} : {1}".format(k,liste[k]),file=crf)
   del liste[k]['titre']
   del liste[k]['quoi']
print("</body></html>",file=crf)

### traintement fichier

print ('</channel>\n</rss>',file=rssf)
rssf.close()
crf.close()
os.chmod(crf.name,stat.S_IRWXU|stat.S_IRGRP|stat.S_IROTH)
if os.path.isfile(compterendu + "/dernier-test.html") : os.unlink(compterendu + "/dernier-test.html")
os.link(crf.name , compterendu + "/dernier-test.html")


