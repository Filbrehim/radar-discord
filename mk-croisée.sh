#!/bin/bash
cat <<finfin | sort> evenements.csv
$(date --date="sunday, 14:00" +%s)|Zul Farak|Rendez-vous donjon de la Ligue|Auberdine Donjon
$(date --date="thursday, 20:30" +%s)|Auberge du Parc|Rendez-vous rôleplay de la Ligue !|Auberdine
$(date --date="saturday, 21:00" +%s)|Taverne des rôdeurs|Guilde xx|Sirannon 
$(date --date="wednesday, 21:00" +%s)|Taverne des rôdeurs|Guilde xx|Sirannon 
$(date --date="tuesday, 21:00" +%s)|Gala du Lierre Touffu|à Hobbitebourg|Sirannon JDR
finfin
wc -l evenements.csv

