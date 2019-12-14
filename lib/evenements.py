#!/usr/bin/python
#-*- coding: utf-8 -*-
#  donne les events

import csv
import os
import pickle

"""Module event """
class event :
    annonceur = "test"

    def legacy_all_event(self)  :
        event = dict()
        with open("evenements.csv","r") as eventf :
            lireevt = csv.reader(eventf,delimiter="|")
            for ligne in lireevt :
                event[ligne[0]]=ligne[1]
        return event ;

    def scan_all_event(self) :
       racine = self.annonceur+".dir"
       if not os.path.isdir(racine) : return None
       event = dict() 
       for f in os.listdir(racine) :
          if f.startswith("evt-") :
              with open(racine+"/"+f,'rb') as f2 :
                 event[f]=pickle.load(f2)
                 f2.close()

       return event
    
    def maj_event(self,ref,champ,valeur) :
       chemin = self.annonceur+".dir/"+ref
       tmp_evt=dict()
       if os.path.isfile(chemin) :
          with open(chemin,'rb') as f :
             tmp_evt = pickle.load(f)
             f.close()
       tmp_evt[champ]=valeur ;
       with open(chemin,'wb') as f :
           pickle.dump(tmp_evt,f) 
           f.close()

    def apropos(self) :
    	"""donne la version"""
    	return "2.&beta;"
