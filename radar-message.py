#!/usr/bin/env python3

import csv
import signal
import os,sys,re
import discord
import time,locale
from jeton import get_discord_token
sys.path.insert(1,'lib')
import evenements


locale.setlocale(locale.LC_TIME, 'fr_FR.utf8')
host=os.uname().nodename
moi=sys.argv[0].split(".")[1][1:]
jeu = discord.Game("{0}  sur {1}".format(moi,host))
client = discord.Client()
ficevent="evenements.csv"
rpevent = []

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
        print (f"{server.name} a pour ID {server.id}")
        if server.name == "Memory Echo" :
            for channel in server.channels :
                if channel.name == "affiches" :
                    await effacer_anciens_message(channel)
                    await channel.send("Et maintenant, quelques informations ... ")
                    await afficher_event(channel)

    await client.close()

client.run(get_discord_token("radar"))

print("déconnecté")
