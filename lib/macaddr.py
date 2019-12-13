#!/usr/bin/python
#-*- coding: utf-8 -*-
#  déchiffre les adresse MAC

import re

macf1txt = ":[0-9a-f]{1,2}" * 6
macf1re = re.compile(macf1txt[1:])
ciscotxt = "-[0-9a-f]{4}" * 3
ciscore  = re.compile(ciscotxt[1:])
compactre = re.compile("^[0-9a-f]{12}$")

fichieroui = 0 ## 0 => indefini, 1 => defini pas lu, 2=> lu
fichierouitxt = "" 
ouidict = dict() 

"""Module mac """
def chercher(chainei) :
	"""recherche si chaine est un adresse MAC"""
	global fichieroui
	quoi = dict() 
	quoi['score'] = 0 
	quoi['donne'] = chainei
	chaine = chainei.lower()
	if macf1re.match(chaine) :
		quoi['score']   = 1 
		quoi['type']    = "mac format IEEE 802"
		quoi['compact'] = "".join(chaine.split(':')) 

	if ciscore.match(chaine) :
		quoi['score']   = 1 
		quoi['type']    = "mac format Cisco"
		quoi['compact'] = "".join(chaine.split('-')) 
 
	if compactre.match(chaine) :
		quoi['score']   = 1
		quoi['type']    = "mac format compact"
		quoi['compact'] = chaine

	if 'compact' in quoi.keys() :
		if fichieroui == 1 : ouitodict("")
		if fichieroui > 0 :
			ieeevendor = quoi['compact'][0:6] 
			if ieeevendor  in ouidict.keys() :
				quoi['vendeur'] = ouidict[ieeevendor] 
				quoi['score']   = quoi['score'] + 1

	return quoi

def ouitodict(emplacement) :
	"""charge le fichier OUI dans un dictionnaire"""
	global fichieroui,fichierouitxt
	echo = 10 
	if fichieroui == 1 :
		with open(fichierouitxt) as ficoui :
			for tmp_l in ficoui.readlines()  :
				ouidict[tmp_l[0:6].lower()] = tmp_l 
		fichieroui = 2
	if fichieroui == 0 :
		fichierouitxt = emplacement
		fichieroui = 1 
		
def apropos() :
	"""donne la version"""
	return "1.2"
