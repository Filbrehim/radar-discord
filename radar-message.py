#!/usr/bin/env python3

import csv
import signal
import os,sys,re
import discord
import time,locale
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
ficevent="evenements.csv"
rpevent = []
annonce = preferences.preference()
annonce.annonceur = moi 

with open (ficevent) as csvfile :
    evtreader = csv.reader(csvfile,delimiter='|') 
    for rangee in evtreader :
        r0 = int(rangee[0])
        rangee[0] =  time.strftime("%A %e à %H:%M",time.localtime(r0))
        rpevent.append(rangee)
    csvfile.close()

for evt in rpevent :
	print (f"à {evt[0]} : {evt[1]}")

async def afficher_event(channel) :
    for evt in rpevent :
       Emb = discord.Embed(title=evt[1],type="rich",description=evt[2])
       Emb.add_field(name="quand",value=evt[0])
       await channel.send(embed=Emb)

async def effacer_anciens_message(channel) :
    async for message in channel.history(limit=20) :
        if message.author == client.user :
            await message.delete() 

@client.event
async def on_ready():
    print('On se connecte comme {0.user}'.format(client))
    await client.change_presence(activity=jeu)
    for server in client.guilds :
        annonce.serveur = server.id
        print (f"{server.name} a pour ID {server.id}")
        annonce.get_preference(False)
        if annonce.annoncer :
            print ("preference trouvées : le canal d'annonce est {0}".format(annonce.prefs["canal_n"]))
            for channel in server.channels :
                if channel.name == annonce.prefs["canal_n"] :
                    await effacer_anciens_message(channel)
                    await channel.send("Et maintenant, quelques informations ... ")
                    await afficher_event(channel)

    await client.close()

client.run(get_discord_token(moi))

print("déconnecté")
