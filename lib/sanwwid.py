#!/usr/bin/python
#-*- coding: utf-8 -*-
#  déchiffre les adresse MAC

import re

macf1txt = ":[0-9a-f]{1,2}" * 6
macf1re = re.compile(macf1txt[1:])
ciscotxt = "-[0-9a-f]{4}" * 3
ciscore  = re.compile(ciscotxt[1:])
compactre = re.compile("[0-9a-f]{32}")

fichieroui = 0 ## 0 => indefini, 1 => defini pas lu, 2=> lu
fichierouitxt = "" 
ouidict = dict() 

"""Module wwid """
def chercher(chainei) :
	"""recherche si chaine est un wwid """
	global fichieroui
	quoi = dict() 
	quoi['score'] = 0 
	quoi['donne'] = chainei
	chaine = chainei.lower()

	if compactre.match(chaine) and len(chaine) == 32 :
		quoi['score'] = 1 
		quoi['type']  = "un wwid long (32)"
		quoi['compact'] = chaine
         
	hita = esthitachi(chaine) 
	if 'score' in hita.keys() :
		quoi['score']   = quoi['score'] + hita['score'] 
		quoi['type']    = "un wwid d'Hitachi Vantara"
		quoi['detail']  = hita

	if 'compact' in quoi.keys() :
		if fichieroui == 1 : ouitodict("")
		if fichieroui > 0 :
			ieeevendor = quoi['compact'][1:7] 
			if ieeevendor  in ouidict.keys() :
				quoi['vendeur'] = ouidict[ieeevendor] 
				quoi['score']   = quoi['score'] + 1

	return quoi

def esthitachi(chaine) :
	"""recherche les wwid Hitachi"""
	hita = dict() 
	tmp_h = chaine.find("0060e8") 
	if tmp_h == -1 : return hita 
	hita['score'] = 1
	tmp_normalise = chaine[tmp_h+6:]
	tmp_m = chaine[tmp_h+17:tmp_h+18]
	tmp_type = chaine[tmp_h+6:tmp_h+6+3]
	tmp_serie = chaine[tmp_h+19:tmp_h+19+4] 
	if tmp_m == 1 :
		hita['modèle'] = "VSP Midrange"
		hita['score']  = hita['score'] + 1
	elif tmp_m == 2 :
		hita['modèle'] = "HUS VM" 
		hita['score']  = hita['score'] + 1
	elif tmp_m == 3 :
		hita['modèle'] = "G1000" 
		hita['score']  = hita['score'] + 1

	if tmp_type == "003" :
		hita['modèle'] = "G1000"
		hita['score']  = hita['score'] + 1
	elif tmp_type == "004" :
		hita['modèle'] = "USP"
		hita['score']  = hita['score'] + 1
	elif tmp_type == "005" :
		hita['modèle'] = "USP-V"
		hita['score']  = hita['score'] + 1
	elif tmp_type == "006" :
		hita['modèle'] = "VSP"
		hita['score']  = hita['score'] + 1
	elif tmp_type == "016" :
		hita['modèle'] = "VSP"
		hita['série'] = "1" + chaine[tmp_h+9:tmp_h+9+4]
		hita['score']  = hita['score'] + 2
	elif tmp_type == "022" or tmp_type == "012" :
		tmp2_ser_s = chaine[tmp_h+9:tmp_h+9+4]
		tmp2_ser_i = int(tmp2_ser_s,16) 
		hita['série'] = "0x(1){} ou 4{}" .format(tmp2_ser_s,tmp2_ser_i) 
		if tmp_type == "022" :
			hita['modèle'] = "GSP G600/G400/G200" 
		else :
			hita['modèle'] = "VSP G600/G400 et VSP F400/F600" 
		tmp_p1 = chaine[tmp_h+13]
		tmp_pn = chaine[tmp_h+14]
		hita['port']   = "CL {0} {1}".format(1+int(tmp_p1),chr(65+int(tmp_pn)) )
		hita['score']  = hita['score'] + 3
	elif tmp_type == "010" :
		tmp2_ser_s = chaine[tmp_h+15:tmp_h+15+8]
		tmp2_ser_i = int(tmp2_ser_s,16) 
		hita['série'] = "0x(1){} ou 4{}" .format(tmp2_ser_s,tmp2_ser_i) 
		if tmp2_ser_i < 90000000 :
			hita['modèle'] = "AMS 1200" 
		else :
			hita['modèle'] = "HUS 100" 
		tmp_p1 = int(chaine[tmp_h+14],16)
		tmp_pn = tmp_p1 // 8
		tmp_p1 = tmp_p1 - 8 * tmp_pn
		hita['port']   = "CL {0} {1}".format(1+int(tmp_p1),chr(65+int(tmp_pn)) )
		hita['score']  = hita['score'] + 3

	return hita 

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
	return "1."
