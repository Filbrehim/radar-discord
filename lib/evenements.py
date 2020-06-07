#!/usr/bin/python
#-*- coding: utf-8 -*-
#  donne les events

import csv
import os
import pickle
import discord
import datetime
import time 
import sys
sys.path.insert(1,'lib')
import preferences

"""Module event """
class event :
    annonceur = "test"
    message = None
    prefer2 = None
    politburo = None

    async def trouver(self,champ,event_tmp,texte,info) :
        if not champ in event_tmp :
           if texte[0:len(champ)+1] == champ+":" :
               return texte[len(champ)+2:]
           else :
               await self.message.channel.send(info)
               return None
        else :
               await self.message.channel.send(f"**{champ}** :" + event_tmp[champ])
               return None

    async def creer_event(self,message,pref) :
        self.prefer2 = pref
        upref = self.prefer2.get_upref(message.author.id)
        event_tmp = upref['event'] 
        self.message = message
        tmp_titre = await self.trouver('titre',event_tmp,message.content,'donner le titre avec **titre:**')
        if tmp_titre != None : event_tmp['titre'] = tmp_titre
        tmp_date = await self.trouver('date',event_tmp,message.content,'donner la date avec **date: jour de la semaine**')
        if tmp_date != None : 
            tmp_date_liste = self.valider_date(tmp_date)
            if 'jour' in tmp_date_liste  :
                event_tmp['date'] = tmp_date_liste['jour']
                event_tmp['timestamp'] = tmp_date_liste['timestamp']
            elif len(tmp_date_liste) > 0 :
                tmp_s = "" 
                for k in tmp_date_liste : tmp_s = tmp_s + tmp_date_liste[k] + ","
                await message.channel.send(f"**{message.content}** ambigüe : __{tmp_s}__")
            else :
                await message.channel.send(f"**{message.content}** ne correspond pas à un jour de la semaine")
        tmp_fac = await self.trouver('faction',event_tmp,message.content,'donner la faction avec **faction:**')
        if tmp_fac != None : event_tmp['faction'] = tmp_fac
        tmp_roy = await self.trouver('royaume', event_tmp,message.content,'donner le royaume/serveur avec **royaume:**')
        if tmp_roy != None : event_tmp['royaume'] = tmp_roy
        upref['event'] = event_tmp
        self.prefer2.set_upref(message.author.id,upref)
        complet = 4
        for k in { 'titre','date','faction','royaume' } :
            if k in event_tmp : 
                complet = complet - 1
        if complet == 0 :
            self.politburo = True
            await message.channel.send(f" toutes les informations sont présentes, on soumet au  Политбюро")

    def valider_date(self,tmp_date) :
        j2 = dict()
        t0 = int(time.time())
        t0 = 86400 * ( int(t0/86400) ) + 20 * 3600 + 1800
        tmp_date2 = tmp_date.lower()
        tmp_lg = len(tmp_date2) 
        tmp_compte = 0 
        for j in range(0,7) :
            js = time.strftime("%A",time.localtime(86400*j+t0)) 
            j2[j] = js
            if js[0:tmp_lg] !=  tmp_date2 : del(j2[j])
            else : 
               j2['jour'] = js
               j2['timestamp'] = 86400*j+t0
               tmp_compte = tmp_compte + 1 
        if tmp_compte > 1 : 
            del (j2['jour'])
            del (j2['timestamp'])
        return j2

    async def afficher_event(self,channel,rpevent_local,flog) :
        for evt in rpevent_local :
           if int(time.time()) - 7200 > int(rpevent_local[evt]['_quand_unix']) : continue
           print(rpevent_local[evt],file=flog)
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

              if "_quand_unix" in event[f] :
                  if int(event[f]["_quand_unix"]) < int(time.time() - 86400)  :
                      os.unlink(racine+"/"+f)
              else : ## pas de timestamp, event pas finalisé
                  del event[f]

       return event
    
    def scan_all_event_pour_quoi(self,quoi) :
       racine = self.annonceur+".dir"
       if not os.path.isdir(racine) : return None
       event = dict() 
       for f in os.listdir(racine) :
          if f.startswith("evt-") :
              with open(racine+"/"+f,'rb') as f2 :
                 event[f]=pickle.load(f2)
                 e_tmp=event[f]
                 f2.close()

              if "_quand_unix" in event[f] :
                  if int(event[f]["_quand_unix"]) < int(time.time() - 86400)  :
                      os.unlink(racine+"/"+f)
              else : ## pas de timestamp, event pas finalisé
                  del event[f]
              contenu = e_tmp['titre'] + ' ' + e_tmp['quoi']
              if contenu.lower().count(quoi.lower()) == 0 :
                  del event[f]
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
    	return "2.0"
