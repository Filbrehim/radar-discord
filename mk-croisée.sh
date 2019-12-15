#!/bin/bash
cat <<finfin | sort> evenements.csv
$(date --date="sunday, 21:00" +%s)|Rendez-vous à la Croisée|venez nombreux et armés !
$(date --date="wednesday, 21:00" +%s)|Rendez-vous à Orgrimmar|venez écouter une histoire !
$(date --date="tuesday, 21:00" +%s)|Marché de Hurlevent|n'oubliez pas vos p.o. !
finfin
wc -l evenements.csv

