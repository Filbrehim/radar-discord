#!/usr/bin/python
#-*- coding: utf-8 -*-
#  donne les events

import os,pickle

"""Module annonce """
class annonce :
    annonceur = "rummeur"
    serveur = 0
    canal = 0 
    annoncer = False 
    chemin = ""
    prefs = 0

    def get_preference(self,fork) :
       """cherche les preferences"""
       chemin = self.annonceur + ".dir/" + str(self.serveur) + ".dir/preference.pkl" 
       existe = os.path.isfile(chemin) 
       if not existe :
           self.annoncer = False 
           if not fork :
               print(f"pas de fichier ${chemin}") 
       else :
           self.annoncer = True
           self.chemin = chemin
           pref_f = open(chemin,"rb") 
           self.prefs = pickle.load(pref_f)
           pref_f.close()

    def apropos(self) :
        """donne la version"""
        return "1."
