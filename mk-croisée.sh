#!/bin/bash
cat <<finfin | sort> evenements.csv
$(date --date="sunday, 21:00" +%s)|Rendez-vous à la Croisée|venez nombreux et armés !
$(date --date="wednesday, 21:00" +%s)|Rendez-vous à Orgrimmar|venez écouter une histoire !
$(date --date="tuesday, 21:00" +%s)|Marché de Hurlevent|n'oubliez pas vos p.o. !
$(date --date="tuesday, 21:00" +%s)|Gala du Lierre Touffu, à Hobbitebourg|n'oubliez pas les paroles !
finfin
wc -l evenements.csv

