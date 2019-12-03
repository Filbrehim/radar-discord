#!/bin/bash
cat <<finfin >> evenements.csv
$(date --date="21:00" +%s)|Rendez-vous à la Croisée
finfin
wc -l evenements.csv

