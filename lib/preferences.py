#!/usr/bin/python
#-*- coding: utf-8 -*-
#  donne les events

import os,pickle

"""Module preferences """
class preference :
    annonceur = "rumeur"
    serveur = 0
    canal = 0 
    annoncer = False 
    chemin = ""
    prefs = 0
    upref = None

    def get_upref(self,id) :
       """preference pour un utilisateur"""
       chemin = self.annonceur +".dir/upref-" + str(id) + ".pkl"
       if not os.path.isfile(chemin) : return None
       else :
          with open(chemin,'rb') as pref_f :
             self.upref = pickle.load(pref_f)
             pref_f.close()
          return self.upref

    def set_upref(self,id,p) :
        """fixe le preference utilisateur"""
        chemin = self.annonceur +".dir/upref-" + str(id) + ".pkl"
        with open(chemin,'wb') as pref_f :
            pickle.dump(p,pref_f)
            pref_f.close()

    def get_preference(self,fork) :
       """cherche les preferences"""
       chemin = self.annonceur + ".dir/" + str(self.serveur) + ".dir/preference.pkl" 
       existe = os.path.isfile(chemin) 
       if not existe :
           self.annoncer = False 
           if not fork :
               print(f"pas de fichier {chemin}") 
       else :
           self.annoncer = True
           self.chemin = chemin
           pref_f = open(chemin,"rb") 
           self.prefs = pickle.load(pref_f)
           pref_f.close()

    def set_preference(self,fork,p) :
       """fixe les preferences"""
       chemin = self.annonceur + ".dir/" + str(self.serveur) + ".dir/preference.pkl" 
       pref_f = open(chemin,"wb") 
       pickle.dump(p,pref_f)
       pref_f.close()

    def apropos(self) :
        """donne la version"""
        return "2.&beta; <br/>pref canal et utilisateur"
