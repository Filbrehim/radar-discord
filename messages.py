#!/usr/bin/env python3

import csv
import signal
import os,sys,re
import discord
import time,locale
import traceback
from jeton import get_discord_token,get_discord_user
sys.path.insert(1,'lib')
import evenements,preferences

locale.setlocale(locale.LC_TIME, 'fr_FR.utf8')
host=os.uname().nodename
moi=get_discord_user()
alerte={}


for a in sys.argv[0:] :
    if a[0:5] == "user=" : moi=a[5:]

jeu = discord.Game("{0}  sur {1}".format(moi,host))
client = discord.Client()
rpevent = []
annonce = preferences.preference()
annonce.annonceur = moi 
event = evenements.event()
event.annonceur = moi
for a in sys.argv[0:] :
    if a[0:7] == "alerte=" :
        alerte[a[7:]]=event.alerte(a[7:])

async def effacer_anciens_message(channel,alerte) :
    uuid = {}
    for a in alerte :
        a2=alerte[a]
        uuid[a2["titre"]] = a2["quoi"]
    async for message in channel.history(limit=100) :
        if message.author == client.user :
            if len(uuid) == 0 :
                await message.delete()
            else :
                ## trier sur embed.get_field(uuid) ?
                if len(message.embeds) == 0 :
                    await message.delete()
                else :
                    if message.embeds[0].title in uuid :
                        await message.delete()                    

@client.event
async def on_ready():
    print(f'On se connecte comme {client.user} ')
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
                    await effacer_anciens_message(channel,alerte)

                    if len(alerte) > 0 :
                        rpevent = event.scan_some_alerte(alerte)
                    else :
                        rpevent = event.scan_all_event()

                    if len(rpevent) > 0 :
                       await channel.send("Et maintenant, quelques informations ... ")
                       await event.afficher_event(channel,rpevent,sys.stdout)
                    else :
                       await channel.send("Pas de nouvelle, bonne nouvelle!") 
                        
      except Exception as inst:
         print(inst)
         print(traceback.print_tb(inst.__traceback__))

    await client.close()

client.run(get_discord_token(moi))

print("déconnecté")
