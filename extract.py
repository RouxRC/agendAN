#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO:
# - finish fields
# - save as csv
# - save as ical
# - add dow/hours/legislature fields
# - calendar viz

import os, json

def datize(d):
    return d

def parse_session(s):
    return s

def parse_num_seance(n):
    return n

def parse_presences(r, typ):
    return "|".join([p["acteurRef"] for p in ((r.get("participants") or {}).get("participantsInternes") or {}).get("participantInterne", []) if p["presence"] == typ])

def parse_auditionnes(r):
    return "|".join(["%s %s %s (%s)" % (p["ident"]["civ"], p["ident"]["prenom"], p["ident"]["nom"], p["dateNais"]) for p in ((r.get("participants") or {}).get("personnesAuditionnees") or {}).get("personneAuditionnee", [])]),

# - ODJ             7644  => uniq([convocationODJ.item] + [objet for p in pointsODJ.pointODJ] + ["\n".join(resumeODJ.item)])
def parse_ODJ(o):
    pass

with open(os.path.join('data', 'AMO10_deputes_actifs_mandats_actifs_organes_XIV.json')) as f:
    orgas = {o["uid"]: o for o in json.load(f)['export']['organes']['organe']}

with open(os.path.join('data', 'Agenda_XV.json')) as f:
    reunions = []
    for r in json.load(f)['reunions']['reunion']:
        # Assemble complementary fields
        if "organe" in r:
            o = r.pop("organe")
            r["organeReuniRef"] = o["organeRef"]
        if "demandeurs" not in r or not r["demandeurs"]:
            r["demandeurs"] = {"acteur": [{"nom": d["acteurNom"], "acteurRef": d.get("acteurRef")} for d in [r.get("demandeur")] if d]}
        # Homogeneize fields containing both arrays or single object
        elif type(r["demandeurs"].get("acteur")) == dict:
            r["demandeurs"]["acteur"] = [r["demandeurs"]["acteur"]]
        if type(((r.get("participants") or {}).get("personnesAuditionnees") or {}).get("personneAuditionnee")) == dict:
            r["participants"]["personnesAuditionnees"]["personneAuditionnee"] = [r["participants"]["personnesAuditionnees"]["personneAuditionnee"]]

        # Skip unconfirmed
        if r.get('cycleDeVie', {}).get('etat', r.get('statut')).lower() != u'confirmé':
            continue

        # Skip Hémicycle Sénat
        if r.get("organeReuniRef") == "PO78718":
            continue

        reunions.append({
            "debut":            datize(r["timeStampDebut"]),
            "fin":              datize(r.get("timeStampFin")),
            "lieu":             r["lieu"].get("libelleCourt", r["lieu"]["libelleLong"]),
            "type":             r.get("typeReunion") or orgas.get(r["organeReuniRef"], {}).get("codeType"),
            "organe":           orgas.get(r.get("organeReuniRef"), {}).get("libelle"),
            "organe_demandeur": orgas.get(r["demandeurs"].get("organe", {}).get("organeRef"), {}).get("libelle"),
            "demandeurs":       "|".join([a["nom"] for a in r["demandeurs"].get("acteur", [])]),
            "ouverture_presse": r.get("ouverturePresse"),
            "session":          parse_session(r.get("sessionRef")),
            "titre":            parse_num_seance((r.get("identifiants") or {}).get("quantieme")),
            "presents":         parse_presences(r, u"présent"),
            "absents":          parse_presences(r, u"absent"),
            "excuses":          parse_presences(r, u"excusé"),
            "auditionnes":      parse_auditionnes(r),
            "ordre_du_jour":    parse_ODJ(r.get("ODJ"))
        })

# TOTAL                                         39360
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
