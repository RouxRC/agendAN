#/bin/bash

rm -rf data
mkdir data

wget http://data.assemblee-nationale.fr/static/openData/repository/AMO/deputes_actifs_mandats_actifs_organes/AMO10_deputes_actifs_mandats_actifs_organes_XIV.json.zip
unzip AMO10_deputes_actifs_mandats_actifs_organes_XIV.json.zip
mv AMO10_deputes_actifs_mandats_actifs_organes_XIV.json data/
rm -f AMO10_deputes_actifs_mandats_actifs_organes_XIV.json.zip

wget http://data.assemblee-nationale.fr/static/openData/repository/15/vp/reunions/Agenda_XV.json.zip
unzip Agenda_XV.json.zip
mv Agenda_XV.json data/
rm -f Agenda_XV.json.zip
