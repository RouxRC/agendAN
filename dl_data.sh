#/bin/bash

mkdir data

LEG="XV"
LEGN=15
if ! [ -z "$1" ]; then
  LEG="XIV"
  LEGN=14
fi

wget http://data.assemblee-nationale.fr/static/openData/repository/$LEGN/amo/deputes_actifs_mandats_actifs_organes/AMO10_deputes_actifs_mandats_actifs_organes_${LEG}.json.zip ||
wget http://data.assemblee-nationale.fr/static/openData/repository/$LEGN/amo/deputes_senateurs_ministres_legislatures_${LEG}/AMO20_dep_sen_min_tous_mandats_et_organes_${LEG}.json.zip -O AMO10_deputes_actifs_mandats_actifs_organes_${LEG}.json.zip
unzip AMO10_deputes_actifs_mandats_actifs_organes_${LEG}.json.zip
mv AMO*${LEG}.json data/AMO10_deputes_actifs_mandats_actifs_organes_${LEG}.json
rm -f AMO10_deputes_actifs_mandats_actifs_organes_${LEG}.json.zip

wget http://data.assemblee-nationale.fr/static/openData/repository/$LEGN/vp/reunions/Agenda_${LEG}.json.zip
unzip Agenda_${LEG}.json.zip
mv Agenda_${LEG}.json data/
rm -f Agenda_${LEG}.json.zip

./extract.py $LEG
