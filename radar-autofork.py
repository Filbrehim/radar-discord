#!/usr/bin/env python3

import os,sys,re
import discord
import macaddr,sanwwid,timestamp
from jeton import get_discord_token

macaddr.ouitodict("oui.txt")
sanwwid.ouitodict("oui.txt")

moi="radar"
fork=True
flog=sys.stdout

for a in sys.argv[0:] :
	if a == "tty" : 
		fork = False
		print ("pas de fork")
	if a[0:5] == "user=" : moi=a[5:]

if fork :
	pid=os.fork()
	if pid > 0 :
		print ('démon pour {moi} forké avec le pid {pid}'.format(pid=pid,moi=moi))
		pidtxt="radar.pid"
		fpid=open(pidtxt,"w")
		print('{pid}'.format(pid=pid),file=fpid)
		fpid.close()
		exit()

	sys.stdout.close()
	sys.stdin.close()
	sys.stderr.close()
	flog = open(moi+".log","a",buffering=1)

host=os.uname().nodename
jeu = discord.Game(f"{moi} sur {host}")
client = discord.Client()

async def afficher(res,demande,message,channel) :
   if res['score'] :
      print (" ** {s}: {texte}".format(s=res['score'],texte=res['type']),file=flog)
      await channel.send("__{0}__ a un score de **{1}**".format(demande,res['score']))
      if message.channel != channel : 
          await message.channel.send("__{0}__ a un score de **{1}**".format(demande,res['score']))
      for champ in ['type','compact','vendeur'] :
          if champ in res.keys() :
              await channel.send("{0} : **{1}**".format(champ,res[champ])) 
      if 'detail' in res.keys() :
          for d in res['detail'] :
              await channel.send("{0} : **{1}**".format(d,res['detail'][d]))

async def webhook(res,demande,message) :
   if res['score'] == 0 : return 
   channel_id_str = str(message.guild.id)+".dir"
   channel_dir = moi+".dir/"+channel_id_str
   if os.path.isdir(channel_dir) :
      print(" paramètres dans {0}".format(channel_dir),file=flog)
      if os.path.exists(channel_dir+"/webhook.txt") :
         a=1
      else :
         await afficher(res,demande,message,message.channel)
   else :
      os.mkdir(channel_dir)
      await afficher(res,demande,message,message.channel)

@client.event
async def on_ready():
    ## print('On se connecte comme {0.user} le {1}'.format(client,time.strftime("%s %A %e %B %Y %T")),file=flog)
    print('On se connecte comme {0.user}'.format(client),file=flog)
    await client.change_presence(activity=jeu)

@client.event
async def on_message(message):
    for_me = False
    if message.author == client.user:
        return

    if message.author.bot :
        print('je parle pas au bot ({0.author.name}), ça les instruits !'.format(message),file=flog) 
        return 

    if message.content.startswith('$hello'):
        await message.channel.send('Hello! {0.author.name}'.format(message))
        if type(message.channel) == discord.channel.DMChannel :
            await message.channel.send("hum, conversation privée {0.author.name} ?".format(message))
        else :
            print('on a répondu à {0.author.name} sur {0.channel.name}, de la guilde {0.guild.name}'.format(message),file=flog)
            if message.guild.name != "" :
                await message.channel.send("je suis content d'être sur {0.guild.name} (ID={0.guild.id})".format(message))
        return 

## message direct ?
    if type(message.channel) == discord.channel.DMChannel :
        for demande in message.content.split() :
            if len(demande) < 7 : continue
            for res in [ macaddr.chercher(demande), sanwwid.chercher(demande), timestamp.chercher(demande) ] :
                await afficher(res,demande,message,message.channel) 
        return 

## on est mentionné ?
    for mentionne in message.mentions :
       if not fork :
           print(f"{mentionne.name} est mentionné")
       if mentionne.name.lower() == moi.lower() :
           for_me = True 

    if for_me :
        public = False 
        for demande in message.content.split() :
             if demande == "/public" : public = True
        print('un message pour moi [{0.content}] de {0.author.name} sur {0.channel.name}'.format(message),file=flog)
        channel_answer = message.author.dm_channel 
        if channel_answer == None :
             channel_answer = await message.author.create_dm()
        await message.channel.send('{1.author.name} me demande **{0}**'.format(message.content,message))
        async with message.channel.typing() :
           for demande in message.content.split() :
             if len(demande) < 7 : continue
             if demande == "/public" : continue
             for res in [ macaddr.chercher(demande), sanwwid.chercher(demande), timestamp.chercher(demande) ] :
                 if public and os.path.isdir(moi+".dir") :
                    await webhook(res,demande,message)
                 else : 
                    await afficher(res,demande,message,channel_answer) 
                    await channel_answer.send('utiliser `/public` pour un affichage public du résultat')

client.run(get_discord_token()) 
