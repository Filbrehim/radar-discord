#!/bin/bash
cat <<finfin | sort> evenements.csv
$(date --date="sunday, 21:00" +%s)|Rendez-vous à la Croisée| venez nombreux et armés
$(date --date="wednesday, 21:00" +%s)|Rendez-vous à Orgrimmar| venez écouter une histoire
finfin
wc -l evenements.csv

