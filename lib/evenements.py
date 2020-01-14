#!/usr/bin/python
#-*- coding: utf-8 -*-
#  donne les events

import csv
import os
import pickle
import discord
import datetime
import time 

"""Module event """
class event :
    annonceur = "test"

    async def afficher_event(self,channel,rpevent_local) :
        for evt in rpevent_local :
           print(rpevent_local[evt])
           if int(time.time()) + 43200 > int(rpevent_local[evt]['_quand_unix']) : continue
           Emb = discord.Embed(title=rpevent_local[evt]['titre'],
                               type="rich",
                               timestamp = datetime.datetime.fromtimestamp(int(rpevent_local[evt]['_quand_unix'])),
                               description=rpevent_local[evt]['quoi'].strip())
           del rpevent_local[evt]['titre']
           del rpevent_local[evt]['quoi']
           del rpevent_local[evt]['_quand_unix']
           del rpevent_local[evt]['quand']
           if 'faction' in rpevent_local[evt] :
               if rpevent_local[evt]['faction'] == "Horde" : Emb.colour = 0xe74c3c
               if rpevent_local[evt]['faction'] == "Alliance" : Emb.colour = 0x3498db
    
           if 'author' in rpevent_local[evt] :
               Emb.set_author(name=rpevent_local[evt]['author'])
           else :
               Emb.set_footer(text="C'est juste une rumeur")
           for k in rpevent_local[evt] : 
              Emb.add_field(name=k,value=rpevent_local[evt][k]) 
           await channel.send(embed=Emb)

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
