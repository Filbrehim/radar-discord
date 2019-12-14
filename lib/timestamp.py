#!/usr/bin/python
#-*- coding: utf-8 -*-
#  déchiffre les adresse MAC

import re
import time
import locale
import timestamp

locale.setlocale(locale.LC_TIME, 'fr_FR.utf8')
tsre=re.compile("[0-9]{9,10}") 

"""Module timestamp """
def chercher(chainei) :
	"""recherche si chaine est un timestamp"""
	quoi = dict()
	quoi['score'] = 0
	quoi['donne'] = chainei 
	if tsre.match(chainei) :
		quoi['score'] = 1
		quoi['type']  = "un timestamp de chez unix"
		tmp_detail = dict() 
		maintenant = int(time.time()) 
		chaine_int = 0
		if "." in chainei : chaine_int = float(chainei) 
		else : chaine_int = int(chainei) 
		if chaine_int < maintenant : 
			tmp_detail['direction'] = "passé" 
			tmp_detail['quand'] = "il y a"
		else : 
			tmp_detail['direction'] = "futur" 
			tmp_detail['quand'] = "dans"
		tmp_format="%A %e %B %Y, %T"
		tmp_detail['absolu'] = time.strftime(tmp_format,time.localtime(chaine_int))
		delta = abs(maintenant-chaine_int)
		delta0 = delta
		unite = "secondes" 
		if   delta <       43200 : 
			tmp_format = "%Hh%M" 
			if delta < 7201 : 
				delta0 = int(delta/60) 
				unite = "minutes"
			else : 
				delta0 = int(delta/3600)
				unite = "heures"
		elif delta <   7 * 86400 : 
			tmp_format = "%A %Hh%M"
			delta0 = int(delta/86400)
			unite = "jours"
		elif delta <  30 * 86400 : 
			tmp_format = "%A %e %Hh"
			delta0 = int(delta/86400) 
			unite = "jour"
		elif delta < 180 * 86400 : 
			tmp_format = "%A %e %B"
			delta0 = int(delta/(30*86400))
			unite = "mois"
		elif delta < 365 * 86400 : 
			tmp_format = "%A %e %B %Y"
			delta0 = int(delta/(30*86400))
			unite = "mois"
		else : 
			tmp_format = "%B %Y"
			delta0 = int(delta/(365*86400))
			unite = "années"
			

		tmp_detail['quand'] = "{0} {1} {2}".format(tmp_detail['quand'],delta0,unite)	
		tmp_detail['relatif'] = time.strftime(tmp_format,time.localtime(chaine_int))

		quoi['detail'] = tmp_detail 
	return quoi

		
def apropos() :
	"""donne la version"""
	return "1.2"
