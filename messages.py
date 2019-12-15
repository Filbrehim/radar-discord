#!/usr/bin/env python3

import csv
import signal
import os,sys,re
import discord
import time,locale,datetime
import traceback
from jeton import get_discord_token
sys.path.insert(1,'lib')
import evenements,preferences


locale.setlocale(locale.LC_TIME, 'fr_FR.utf8')
host=os.uname().nodename
moi="radar"
for a in sys.argv[0:] :
    if a[0:5] == "user=" : moi=a[5:]

jeu = discord.Game("{0}  sur {1}".format(moi,host))
client = discord.Client()
rpevent = []
annonce = preferences.preference()
annonce.annonceur = moi 
event = evenements.event()
event.annonceur = moi


async def afficher_event(channel,rpevent_local) :
    for evt in rpevent_local :
       print(rpevent_local[evt])
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

async def effacer_anciens_message(channel) :
    async for message in channel.history(limit=100) :
        if message.author == client.user :
            await message.delete() 

@client.event
async def on_ready():
    print('On se connecte comme {0.user}'.format(client))
    await client.change_presence(activity=jeu)
    for server in client.guilds :
      try :
        annonce.serveur = server.id
        print (f"{server.name} a pour ID {server.id}")
        annonce.get_preference(False)
        if annonce.annoncer :
            print ("preference trouvées : le canal d'annonce est {0}".format(annonce.prefs["canal_n"]))
            for channel in server.channels :
                if channel.name == annonce.prefs["canal_n"] :
                    rpevent = event.scan_all_event()
                    await effacer_anciens_message(channel)
                    if len(rpevent) > 0 :
                       await channel.send("Et maintenant, quelques informations ... ")
                       await afficher_event(channel,rpevent)
                    else :
                       await channel.send("Pas de nouvelle, bonne nouvelle!") 
                        
      except Exception as inst:
         print(inst)
         print(traceback.print_tb(inst.__traceback__))

    await client.close()

client.run(get_discord_token(moi))

print("déconnecté")
