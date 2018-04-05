
with open('AMO10_deputes_actifs_mandats_actifs_organes_XIV.json') as f:
    orgas = {o["uid"]: o for o in json.load(f)['export']['organes']['organe']}

with open('Agenda_XV.json') as f:
    a = json.load(f)['reunions']['reunion']
len(a)
# TOTAL                                         39360

keys = []
for b in a:
    keys += b.keys()
keys = sorted(list(set(keys)))
keytypes = {v: type([b for b in a if b.get(v)][0].get(v)) for v in keys}

c = [b for b in a if b.get('cycleDeVie', {}).get('etat', b.get('statut')).lower() == 'confirm\xe9']
len(c)
# Confirmés                                     32341 = 7644 + 24697
#
# - organeReuniRef = {                          9385
#   + not typeReunion                           7644
#   "PO644420": "Hémicycle",                    1371        X
#   "PO78718":  "Sénat Hémicycle (WTF)"         655
#   "437 other values"                                      X
# }
# - typeReunion = {                             24697
#   "GP":   "Groupes politiques",               915         X
#   "GE":   "Groupes d'études",                 436         X
#   "GEVI": "Groupes d'études internationaux",  20          X
#   "GA":   "Groupes d'amitié",                 356         X
#   "DEP":  "Réunions individuelles"            22970
# }
#
# FIELDS
# - identifiants    2026  => quantieme = numéro séance for hémicycle
# - lieu            32341 => libelleLong/?code/?libelleCourt
# - ODJ             7644  => uniq([convocationODJ.item] + [p.objet for p in pointsODJ.pointODJ] + ["\n".join(resumeODJ.item)])
# - demandeur       7856  => acteurNom/?acteurRef
# - demandeurs      24485 => acteur.(nom/acteurRef or array of nom/acteurRef) or organe.(nom/organeRef)
# - participants    7644  => presences = [presence/acteurRef for p in participantsInternes.participantInterne] + auditionnes = [personnesAuditionnees.personneAuditionnee = dict or array of dict ident.civ/ident.prenom/ident.nom/dateNais]
# - organe          18    => if not organeReuniRef try get('organe').get('organeRef')
# - organeReuniRef  32129
# - ouverturePresse 7644
# - sessionRef      7644
# - timeStampDebut  32341
# - timeStampFin    31744
# - typeReunion	    24697
