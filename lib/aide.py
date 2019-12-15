#!/usr/bin/python
#-*- coding: utf-8 -*-
#  affiche de l'aide
#  d'abord dans commun, puis dans annonceur

import os,pickle

"""Module preferences """
class aide :
    annonceur = "rumeur"
    serveur = 0
    async def rechercher(self,text,channel) :
       """fixe les preferences"""
       trouve = 0 
       for chemin in [ "commun.dir/" + text + ".txt" , 
                       "commun.dir/" + self.annonceur + "-" + text + ".txt" ] :
          if os.path.isfile(chemin) :
             txt_compose=""
             with open(chemin,'r') as f :
                 for tmp_buf in f.readlines() :
                     txt_compose = txt_compose + tmp_buf
                 f.close()
             trouve = trouve + 1
             await channel.send(txt_compose)
       return trouve

    def apropos(self) :
        """donne la version"""
        return "1.&beta; "
