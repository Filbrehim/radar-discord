#!/usr/bin/env python3

import os,sys,re
import discord
import time
from pprint import pprint
from jeton import get_discord_token,get_discord_user
sys.path.insert(1,'lib')
import macaddr,sanwwid,timestamp,preferences,aide
import evenements

macaddr.ouitodict("lib/oui.txt")
sanwwid.ouitodict("lib/oui.txt")

moi=get_discord_user()

fork=True
flog=sys.stdout
anti_flood = dict() 

for a in sys.argv[0:] :
	if a == "tty" : 
		fork = False
		print ("pas de fork")
	if a[0:5] == "user=" : moi=a[5:]

preference = preferences.preference()
preference.annonceur = moi
aide = aide.aide()
aide.annonceur = moi

if not os.path.isdir(moi+".dir") : os.mkdir(moi+".dir")
if os.path.isfile(moi+".pid") : os.unlink(moi+".pid")

if fork :
	pid=os.fork()
	if pid > 0 :
		print (f'démon pour {moi} forké avec le pid {pid}')
		pidtxt=moi+".pid"
		fpid=open(pidtxt,"w")
		print('{pid}'.format(pid=pid),file=fpid)
		fpid.close()
		exit()

	sys.stdout.close()
	sys.stdin.close()
	sys.stderr.close()
	flog = open(moi+".log","a",buffering=1)

rpevent = []
g_event = evenements.event()
g_event.annonceur = moi
host=os.uname().nodename
jeu = discord.Game(f"!aide en MP @{moi}")
client = discord.Client()

async def preferences(message,public) :
   if type(preference.prefs) is dict :
      tmp_quand = time.time()
      tmp_quand_s = time.strftime("à %Hh%m",time.localtime(tmp_quand))
      if tmp_quand - preference.prefs["quand"] > 86400 :
          tmp_quand_s = time.strftime("%A %e %B",time.localtime(tmp_quand))
      await message.channel.send("{0} a choisi de poster sur **{1}** {2}". \
         format(preference.prefs["qui"],preference.prefs["canal_n"],tmp_quand_s))

async def annoncer_ici(message,public) :
   if preference.prefs == 0 :
      preference.prefs = dict()
   preference.prefs["canal_n"] = message.channel.name
   preference.prefs["canal_i"] = message.channel.id
   preference.prefs["quand"]   = time.time()
   preference.prefs["qui"]     = message.author.name
   preference.set_preference(fork,preference.prefs) 

async def recherche_radar(message,public) :
   channel_answer = message.author.dm_channel 
   if channel_answer == None :
        channel_answer = await message.author.create_dm()
   for demande in message.content.split() :
     if len(demande) < 7 : continue
     if demande == "/public" : continue
     for res in [ macaddr.chercher(demande), sanwwid.chercher(demande), timestamp.chercher(demande) ] :
         if public and os.path.isdir(moi+".dir") :
            await webhook(res,demande,message)
         else : 
            await afficher(res,demande,message,channel_answer) 
            flood = time.time()
            if message.author in anti_flood :
                 if anti_flood[message.author] + 60 < flood :
                      anti_flood[message.author] = flood
                      await channel_answer.send('utiliser `/public` pour un affichage public du résultat')
            else :
                 anti_flood[message.author] = flood
                 await channel_answer.send('utiliser `/public` pour un affichage public du résultat')

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
    print('On se connecte comme {0.user.name}'.format(client),file=flog)
    for server in client.guilds :
        if not fork :
            print(f" je suis présent sur {server.name}")
            preference_dir=moi+".dir/"+str(server.id)+".dir"
            if not os.path.isdir(preference_dir) :
                 print(" * création répertoire") 
                 os.mkdir(preference_dir)
            if not os.path.isfile(preference_dir+"/preference.pkl")  :
                 print(f"   ** sans préférence {preference_dir}")
            for channel in server.text_channels :
                 print(f"   ** {channel.name} ") 
    await client.change_presence(activity=jeu)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.author.bot :
        if not fork :
            print(f'je parle pas au bot ({message.author.name}), ça les instruits !',file=flog) 
        return 

    for_me = False
    private_msg = False
    cest_qui = message.author.name
    if type(message.channel) == discord.channel.DMChannel : private_msg = True
    if not private_msg and message.author.nick != None :
        cest_qui = message.author.nick

    if message.content.startswith('!hello'):
        if private_msg :
            await message.channel.send(f'Hello! {cest_qui}')
            await message.channel.send(f"hum, conversation privée {message.author.name} ?")
            await message.channel.send("moi c'est {0} sur **{1}**".format(moi,os.uname().nodename))
            print(f'on a répondu à {message.author.name}, mais en privé',file=flog)
        else :
            await message.channel.send(f'Hello! {cest_qui}')
            print('on a répondu à {0.author.name} sur {0.channel.name}, de la guilde {0.guild.name}'.format(message),file=flog)
            content = "content"
            if moi == "frezza" : content = "contente"
            await message.channel.send(f"je suis {content} d'être sur {message.guild.name}")
            await message.channel.send(f"utiliser @{client.user.name} pour m'interpeller") 
        return 

## message direct ?
    if private_msg :
        ## preparation event en cours ?
        upref = preference.get_upref(message.author.id) 
        ### annonce event en cours ?
        if upref != None and 'annonce_event' in upref :
            pgm_quand = int(upref['annonce_event'])
            if time.time() - pgm_quand > 3600 :
                 await message.channel.send("temps imparti pour composer un event dépassé")
                 if 'event' in upref : del (upref['event'])
                 del (upref['annonce_event'])
                 preference.set_upref(message.author.id,upref)
            else :
                 await message.channel.send("composition d'event en cours (il reste {} secondes)".format(3600+pgm_quand-int(time.time())))
                 await g_event.creer_event(message,preference)

        for demande in message.content.split() :
            if demande == "!pref" :
                if upref == None :
                    upref = { 'rgpd' : time.time() , 'aoublie' : time.time()+180*86400 , 'pigeon préféré' : 'Afrique' , 'nom' : cest_qui }
                    await message.channel.send("t'étais pas connu de nos services ...")
                else : demande = "!rgpd"
                upref['nom'] = cest_qui
                preference.set_upref(message.author.id,upref)
				
            if demande == "!rgpd" :
                await message.channel.send("pas la peine d'être grossier !")
                if upref == None :
                   await message.channel.send("t'es pas connu de nos services.")
                else :
                   async with message.channel.typing() :
                      await message.channel.send("tient donc, voyons ça ...")
                      for k in upref :
                         if k == "rgpd" : 
                            await message.channel.send("RGPD mise à jour **{0}**".format(time.strftime("%a %e %B",time.localtime(int(upref[k])))))
                            continue
                         if k == "aoublie" : 
                            await message.channel.send("Rayé de nos listes dés le **{0}**".format(time.strftime("%a %e %B %Y",time.localtime(int(upref[k])))))
                            continue
                         if k == "annonce_event" : 
                            await message.channel.send(f"{k} : {upref[k]}")
                            tmp_ts = timestamp.chercher(str(int(upref[k]))) 
                            await message.channel.send("annonce d'une event : **{1}** ({0})".\
                               format(tmp_ts['detail']['quand'],tmp_ts['detail']['relatif']) ) 
                            continue
                         await message.channel.send(f"{k} : {upref[k]}")
                   continue

            if demande == "!event" :
                rpevent = g_event.scan_all_event()
                print(f'{message.author.name} demande des event',file=flog)
                print('on en a trouvé {}'.format(len(rpevent)),file=flog)
                if len(rpevent) > 0 :
                    await message.channel.send("prochainement sur vos écrans : ")
                    await g_event.afficher_event(message.channel,rpevent,flog)
                    await message.channel.send("on peut filter avec un mot clef: **?auberge**")
                    continue

            if demande[0] == "?" :
                rpevent = g_event.scan_all_event_pour_quoi(demande[1:])
                print(f'{message.author.name} demande des event : {demande}',file=flog)
                print('on en a trouvé {}'.format(len(rpevent)),file=flog)
                if len(rpevent) > 0 :
                    await message.channel.send(f"prochainement sur vos écrans : (**{demande}**)")
                    await g_event.afficher_event(message.channel,rpevent,flog)
                    continue
            if demande == "!help" : demande = "!aide" 
            if demande[0] == "!" : 
                if 0 < await aide.rechercher(demande[1:],message.channel) : continue

            if len(demande) < 7 : continue
            if moi == "radar" :
                async with message.channel.typing() :
                    for res in [ macaddr.chercher(demande), sanwwid.chercher(demande), timestamp.chercher(demande) ] :
                        await afficher(res,demande,message,message.channel) 
        return 
    else :
        preference.canal   = message.channel
        preference.serveur = preference.canal.guild.id
        preference.get_preference(fork)
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
        print('un message pour moi [{0.content}] de {1} sur {0.channel.name}'.format(message,cest_qui),file=flog)
        await message.channel.send(f'{cest_qui} me demande **{message.content}**')
        if moi == "radar" :
            async with message.channel.typing() :
                await recherche_radar(message,public) 

        for demande in message.content.split() :

            if demande == "!annoncer_ici" :
                 await annoncer_ici(message,fork)
                 await message.channel.send(f"{cest_qui} a choisi {message.channel.name} comme canal d'annonce")
            if demande == "!rgpd" :
                await message.channel.send('rgpd !? on est procédureux ?')
                await preferences(message,fork)

            if demande == "!annonce" and not private_msg :
                upref = preference.get_upref(message.author.id)
                if upref == None  :
                    upref = { 'rgpd' : time.time() , 'aoublie' : time.time()+180*86400 , 'pigeon préféré' : 'Asie'  }
                if 'event' in upref :
                    await  message.channel.send(f"{cest_qui} il y a déjà un event en cours")
                    continue
                await  message.channel.send(f"{cest_qui}, je suppose que vous avez le droit d'annoncer un event")
                await  message.channel.send(f"{cest_qui}, mais poursuivons en privé")
                upref['annonce_event'] = int(time.time())
                upref['event'] = { 'canal original' : message.guild.name , 'par' : cest_qui }
                upref['aoublie'] = upref['annonce_event'] +180*86400
                preference.set_upref(message.author.id,upref)

client.run(get_discord_token(moi)) 
