# ==========================================
# FACTEURS D'EMISSION — PROJET CARBONE
# ==========================================


# ==========================================
# SCOPE 1 — INDIVIDU — VOITURE
# ==========================================

# Essence
# kg CO2e / litre
FACTEUR_ESSENCE = 2.797

# Diesel
# kg CO2e / litre
FACTEUR_DIESEL = 3.17

# GPL
# kg CO2e / litre
FACTEUR_GPL = 1.88


# ==========================================
# SCOPE 1 — INDIVIDU — GAZ NATUREL
# ==========================================

# kg CO2e / kWh PCI
FACTEUR_GAZ_NATUREL_KWH = 0.239

# kWh PCI par m3
KWH_PCI_PAR_M3_GAZ = 11.628

# kg CO2e / m3
FACTEUR_GAZ_NATUREL_M3 = (
    FACTEUR_GAZ_NATUREL_KWH
    * KWH_PCI_PAR_M3_GAZ
)


# ==========================================
# SCOPE 1 — INDIVIDU — GPL DOMESTIQUE
# ==========================================

# Poids retenu pour une bouteille
# kg par bouteille
POIDS_BOUTEILLE_GPL_KG = 13

# Facteur énergétique GPL
# kg CO2e / kg GPL
FACTEUR_GPL_KG = 3.00


# ==========================================
# FONCTIONS DE CALCUL — INDIVIDU — SCOPE 1
# ==========================================

def calcul_co2_essence(litres):
    return litres * FACTEUR_ESSENCE


def calcul_co2_diesel(litres):
    return litres * FACTEUR_DIESEL


def calcul_co2_gpl(litres):
    return litres * FACTEUR_GPL


def calcul_co2_gaz_m3(consommation_m3):
    return (
        consommation_m3
        * FACTEUR_GAZ_NATUREL_M3
    )


def calcul_co2_gpl_bouteilles(nombre_bouteilles):
    return (
        nombre_bouteilles
        * POIDS_BOUTEILLE_GPL_KG
        * FACTEUR_GPL_KG
    )


# ==========================================
# SCOPE 2 — INDIVIDU — ÉLECTRICITÉ
# ==========================================

# Facteur d'émission de l'électricité
# Tunisie / STEG
#
# Unité :
# kg CO2e / kWh

FACTEUR_ELECTRICITE = 0.4627


def calcul_co2_electricite(kwh):
    """
    Calcule les émissions liées
    à la consommation d'électricité.

    Entrée :
        kWh consommés

    Sortie :
        kg CO2e
    """
    return (
        kwh
        * FACTEUR_ELECTRICITE
    )


# ==========================================
# SCOPE 3 — INDIVIDU — ALIMENTATION
# ==========================================

# Hypothèse du projet :
# 1 portion = 100 g = 0,1 kg

FACTEUR_VIANDE_ROUGE = 28.00
FACTEUR_POULET = 3.00
FACTEUR_POISSON = 13.63
FACTEUR_PRODUITS_LAITIERS = 0.87


def calcul_co2_viande_rouge(repas_semaine):
    return (
        repas_semaine
        * 52
        * 0.1
        * FACTEUR_VIANDE_ROUGE
    )


def calcul_co2_poulet(repas_semaine):
    return (
        repas_semaine
        * 52
        * 0.1
        * FACTEUR_POULET
    )


def calcul_co2_poisson(repas_semaine):
    return (
        repas_semaine
        * 52
        * 0.1
        * FACTEUR_POISSON
    )


def calcul_co2_produits_laitiers(portions_semaine):
    return (
        portions_semaine
        * 52
        * 0.1
        * FACTEUR_PRODUITS_LAITIERS
    )


# ==========================================
# SCOPE 3 — INDIVIDU — TRANSPORT
# ==========================================

FACTEUR_BUS = 0.1234
FACTEUR_TRAIN = 0.01226
FACTEUR_TAXI = 0.2751

# Facteur d'émission retenu pour l'avion
# kg CO2e / passager-km
FACTEUR_AVION = 0.125

# Distances moyennes retenues par type de trajet
# km par voyage
DISTANCE_AVION_COURT = 500
DISTANCE_AVION_MOYEN = 2000
DISTANCE_AVION_LONG = 7000


def calcul_co2_bus(
    jours_semaine,
    distance_km
):
    return (
        jours_semaine
        * distance_km
        * 52
        * FACTEUR_BUS
    )


def calcul_co2_train(
    trajets_semaine,
    distance_km
):
    return (
        trajets_semaine
        * distance_km
        * 52
        * FACTEUR_TRAIN
    )


def calcul_co2_taxi(
    trajets_semaine,
    distance_km
):
    return (
        trajets_semaine
        * distance_km
        * 52
        * FACTEUR_TAXI
    )


def calcul_co2_avion(
    voyages_an,
    type_vol
):
    voyages_an = float(voyages_an)

    if type_vol == "court":
        distance_km = DISTANCE_AVION_COURT

    elif type_vol == "moyen":
        distance_km = DISTANCE_AVION_MOYEN

    elif type_vol == "long":
        distance_km = DISTANCE_AVION_LONG

    else:
        distance_km = 0

    return (
        voyages_an
        * distance_km
        * FACTEUR_AVION
    )


# ==========================================
# SCOPE 3 — INDIVIDU — ACHATS
# ==========================================

FACTEUR_VETEMENTS = 13.00
FACTEUR_CHAUSSURES = 16.00

FACTEUR_SMARTPHONE = 8.00
FACTEUR_ORDINATEUR_DESKTOP = 32.00
FACTEUR_ORDINATEUR_PORTABLE = 42.00
FACTEUR_TELEVISION = 40.00


def calcul_co2_vetements(nombre):
    return nombre * FACTEUR_VETEMENTS


def calcul_co2_chaussures(nombre):
    return nombre * FACTEUR_CHAUSSURES


def calcul_co2_smartphones(nombre):
    return nombre * FACTEUR_SMARTPHONE


def calcul_co2_ordinateurs(
    nombre,
    type_ordinateur="portable"
):
    if type_ordinateur == "desktop":
        facteur = FACTEUR_ORDINATEUR_DESKTOP
    else:
        facteur = FACTEUR_ORDINATEUR_PORTABLE

    return nombre * facteur


def calcul_co2_televisions(nombre):
    return nombre * FACTEUR_TELEVISION


# ==========================================
# SCOPE 3 — INDIVIDU — EAU
# ==========================================

FACTEUR_EAU = 0.3622


def calcul_co2_eau(consommation_m3):
    return (
        consommation_m3
        * FACTEUR_EAU
    )


# ==========================================
# SCOPE 3 — INDIVIDU — DÉCHETS
# ==========================================

FACTEUR_DECHETS = 497.29


def calcul_co2_dechets(
    quantite_tonnes
):
    return (
        quantite_tonnes
        * FACTEUR_DECHETS
    )


# ==========================================
# BÂTIMENT — SCOPE 1
# ==========================================

# Gaz naturel
# kg CO2e / m3
FACTEUR_BATIMENT_GAZ_NATUREL_M3 = 0.239

# GPL
# kg CO2e / kg GPL
FACTEUR_BATIMENT_GPL_KG = 3.00

# Fioul résiduel
# kg CO2e / litre
# Valeur de travail retenue pour le projet
FACTEUR_BATIMENT_FIOUL_L = 3.08433

# Diesel
# kg CO2e / litre
FACTEUR_BATIMENT_DIESEL_L = 3.17


# ==========================================
# BÂTIMENT — SCOPE 1 — RÉFRIGÉRANTS
# ==========================================

# kg CO2e / kg de fluide rechargé
PRG_R22 = 1810
PRG_R134A = 1430
PRG_R404A = 3922
PRG_R407C = 1774
PRG_R410A = 2088
PRG_R32 = 675


def calcul_co2_batiment_gaz_naturel(consommation_m3):
    return (
        float(consommation_m3)
        * FACTEUR_BATIMENT_GAZ_NATUREL_M3
    )


def calcul_co2_batiment_gpl(consommation_kg):
    return (
        float(consommation_kg)
        * FACTEUR_BATIMENT_GPL_KG
    )


def calcul_co2_batiment_fioul(consommation_litres):
    return (
        float(consommation_litres)
        * FACTEUR_BATIMENT_FIOUL_L
    )


def calcul_co2_batiment_diesel(consommation_litres):
    return (
        float(consommation_litres)
        * FACTEUR_BATIMENT_DIESEL_L
    )


def calcul_co2_batiment_refrigerant(
    type_refrigerant,
    quantite_kg
):
    facteurs = {
        "R22": PRG_R22,
        "R134A": PRG_R134A,
        "R404A": PRG_R404A,
        "R407C": PRG_R407C,
        "R410A": PRG_R410A,
        "R32": PRG_R32,
    }

    facteur = facteurs.get(
        type_refrigerant,
        0
    )

    return (
        float(quantite_kg)
        * facteur
    )


# ==========================================
# BÂTIMENT — SCOPE 2
# ==========================================

# Électricité achetée au réseau
# kg CO2e / kWh
FACTEUR_BATIMENT_ELECTRICITE = (
    FACTEUR_ELECTRICITE
)


def calcul_co2_batiment_electricite(
    kwh_achetes
):
    return (
        float(kwh_achetes)
        * FACTEUR_BATIMENT_ELECTRICITE
    )


# ==========================================
# BÂTIMENT — SCOPE 3
# MATÉRIAUX / RÉNOVATION
# ==========================================

# ------------------------------------------
# Facteurs spécifiques / régionaux retenus
# ------------------------------------------

# Ciment gris CEM I
# kg CO2e / kg
FACTEUR_CIMENT_GRIS_TN = 0.82

# Ciment blanc CEM I
# kg CO2e / kg
FACTEUR_CIMENT_BLANC_TN = 1.27

# Verre plat
# kg CO2 / kg
FACTEUR_VERRE_PLAT_TN = 0.21

# Verre creux
# kg CO2 / kg
FACTEUR_VERRE_CREUX_TN = 0.162


# ------------------------------------------
# Facteurs LCA de référence
# ------------------------------------------

# kg CO2e / kg
FACTEUR_BETON = 0.177
FACTEUR_ACIER = 1.344
FACTEUR_BRIQUE = 0.2569


# Aluminium :
# pas de facteur définitif intégré à ce stade.
FACTEUR_ALUMINIUM = None


# Isolation :
# valeurs de travail à valider méthodologiquement
# avant utilisation finale dans le calcul.
FACTEUR_LAINE_VERRE = 1.05
FACTEUR_LAINE_ROCHE = 2.00
FACTEUR_EPS = 3.00
FACTEUR_XPS = 4.00
FACTEUR_PUR_PIR = 5.00


def calcul_co2_ciment(
    quantite_kg,
    type_ciment
):
    if type_ciment == "gris":
        facteur = FACTEUR_CIMENT_GRIS_TN

    elif type_ciment == "blanc":
        facteur = FACTEUR_CIMENT_BLANC_TN

    else:
        facteur = 0

    return (
        float(quantite_kg)
        * facteur
    )


def calcul_co2_verre(
    quantite_kg,
    type_verre
):
    if type_verre == "plat":
        facteur = FACTEUR_VERRE_PLAT_TN

    elif type_verre == "creux":
        facteur = FACTEUR_VERRE_CREUX_TN

    else:
        facteur = 0

    return (
        float(quantite_kg)
        * facteur
    )


def calcul_co2_beton(quantite_kg):
    return (
        float(quantite_kg)
        * FACTEUR_BETON
    )


def calcul_co2_acier(quantite_kg):
    return (
        float(quantite_kg)
        * FACTEUR_ACIER
    )


def calcul_co2_brique(quantite_kg):
    return (
        float(quantite_kg)
        * FACTEUR_BRIQUE
    )


def calcul_co2_isolation(
    quantite_kg,
    type_isolation
):
    facteurs = {
        "laine_verre": FACTEUR_LAINE_VERRE,
        "laine_roche": FACTEUR_LAINE_ROCHE,
        "eps": FACTEUR_EPS,
        "xps": FACTEUR_XPS,
        "pur_pir": FACTEUR_PUR_PIR,
    }

    facteur = facteurs.get(
        type_isolation,
        0
    )

    return (
        float(quantite_kg)
        * facteur
    )


# ==========================================
# NOTES MÉTHODOLOGIQUES
# ==========================================
#
# 1. Les facteurs "Individu" sont conservés
#    tels qu'ils étaient utilisés dans le projet.
#
# 2. Les facteurs "Bâtiment" sont séparés
#    pour éviter de modifier le fonctionnement
#    déjà validé du module Individu.
#
# 3. Pour les matériaux, la priorité est donnée
#    aux données spécifiques à la Tunisie lorsque
#    nous en avons retenu une.
#
# 4. Aluminium et certains facteurs d'isolation
#    restent à finaliser avant un calcul définitif.

# ==========================================
# BÂTIMENT — SCOPE 3 — DÉCHETS
# ==========================================

FACTEURS_DECHETS_BATIMENT = {
    "papier_carton": {
        "recyclage": 4.65358,
        "incineration": 4.65358,
        "enfouissement": 1164.51317,
    },
    "plastique": {
        "recyclage": 4.65358,
        "incineration": 4.65358,
        "enfouissement": 9.00687,
    },
    "verre": {
        "recyclage": 4.65358,
        "incineration": 4.65358,
        "enfouissement": 9.00687,
    },
    "metaux": {
        "recyclage": 1.01398,
        "incineration": 4.65358,
        "enfouissement": 1.26435,
    },
    "organiques": {
        "compostage": 0.0,
        "incineration": 4.65358,
        "enfouissement": 656.10991,
    },
    "residuels": {
        "recyclage": 4.65358,
        "incineration": 4.65358,
        "enfouissement": 497.28993,
    },
}

def calcul_co2_dechet_batiment(
    type_dechet,
    quantite_tonnes,
    traitement="enfouissement"
):
    facteurs = FACTEURS_DECHETS_BATIMENT.get(type_dechet, {})
    facteur = facteurs.get(traitement, 0)
    return float(quantite_tonnes) * facteur


# ==========================================
# BÂTIMENT — SCOPE 3 — TRANSPORT
# ==========================================

FACTEUR_BATIMENT_VOITURE_ESSENCE_KM = 0.16272
FACTEUR_BATIMENT_VOITURE_DIESEL_KM = 0.17304
FACTEUR_BATIMENT_BUS_PASSAGER_KM = 0.10385
FACTEUR_BATIMENT_TRAIN_PASSAGER_KM = 0.03546
FACTEUR_BATIMENT_AVION_PASSAGER_KM = 0.10916

def calcul_co2_batiment_voiture(distance_km, carburant="essence"):
    facteur = (
        FACTEUR_BATIMENT_VOITURE_DIESEL_KM
        if carburant == "diesel"
        else FACTEUR_BATIMENT_VOITURE_ESSENCE_KM
    )
    return float(distance_km) * facteur

def calcul_co2_batiment_bus(distance_km):
    return float(distance_km) * FACTEUR_BATIMENT_BUS_PASSAGER_KM

def calcul_co2_batiment_train(distance_km):
    return float(distance_km) * FACTEUR_BATIMENT_TRAIN_PASSAGER_KM

def calcul_co2_batiment_avion(distance_km):
    return float(distance_km) * FACTEUR_BATIMENT_AVION_PASSAGER_KM


# ==========================================
# BÂTIMENT — SCOPE 3 — ALUMINIUM
# ==========================================

FACTEUR_ALUMINIUM = 2.176

def calcul_co2_aluminium(quantite_kg):
    return float(quantite_kg) * FACTEUR_ALUMINIUM


# ==========================================
# BÂTIMENT — SCOPE 3 — ÉQUIPEMENTS
# ==========================================

FACTEUR_BATIMENT_MOBILIER_KG = 6.00
FACTEUR_BATIMENT_ORDINATEUR_UNITE = 42.00
FACTEUR_BATIMENT_ECRAN_UNITE = 51.69
FACTEUR_BATIMENT_IMPRIMANTE_UNITE = 123.45
FACTEUR_BATIMENT_TELEVISION_UNITE = 40.00
FACTEUR_BATIMENT_AUTRE_EQUIPEMENT_UNITE = 42.00

def calcul_co2_batiment_equipements(type_equipement, quantite):
    facteurs = {
        "mobilier": FACTEUR_BATIMENT_MOBILIER_KG,
        "ordinateur": FACTEUR_BATIMENT_ORDINATEUR_UNITE,
        "ecran": FACTEUR_BATIMENT_ECRAN_UNITE,
        "imprimante": FACTEUR_BATIMENT_IMPRIMANTE_UNITE,
        "television": FACTEUR_BATIMENT_TELEVISION_UNITE,
        "photocopieur": FACTEUR_BATIMENT_IMPRIMANTE_UNITE,
        "videoprojecteur": FACTEUR_BATIMENT_AUTRE_EQUIPEMENT_UNITE,
        "reseau": FACTEUR_BATIMENT_AUTRE_EQUIPEMENT_UNITE,
        "climatiseur": FACTEUR_BATIMENT_AUTRE_EQUIPEMENT_UNITE,
        "refrigerateur": FACTEUR_BATIMENT_AUTRE_EQUIPEMENT_UNITE,
        "eclairage": FACTEUR_BATIMENT_AUTRE_EQUIPEMENT_UNITE,
        "equipement_electrique": FACTEUR_BATIMENT_AUTRE_EQUIPEMENT_UNITE,
        "batterie_onduleur": FACTEUR_BATIMENT_AUTRE_EQUIPEMENT_UNITE,
    }
    facteur = facteurs.get(type_equipement, 0)
    return float(quantite) * facteur


# ==========================================
# ENTREPRISE — SCOPE 3 — VÊTEMENTS / EPI
# ==========================================
# Facteurs par unité issus d'ECP/empreintes de produits uvex.
FACTEUR_ENTREPRISE_POLO_TRAVAIL = 3.57
FACTEUR_ENTREPRISE_PANTALON_TRAVAIL = 9.06
FACTEUR_ENTREPRISE_VESTE_TRAVAIL = 6.19
FACTEUR_ENTREPRISE_COMBINAISON_TRAVAIL = 5.97
FACTEUR_ENTREPRISE_CHAUSSURES_SECURITE = 7.94
FACTEUR_ENTREPRISE_BOTTES_SECURITE = 8.09
FACTEUR_ENTREPRISE_GANTS = 6.07
FACTEUR_ENTREPRISE_CASQUE = 2.07


def calcul_co2_entreprise_vetement(type_vetement, quantite):
    facteurs = {
        "polo": FACTEUR_ENTREPRISE_POLO_TRAVAIL,
        "pantalon": FACTEUR_ENTREPRISE_PANTALON_TRAVAIL,
        "veste": FACTEUR_ENTREPRISE_VESTE_TRAVAIL,
        "combinaison": FACTEUR_ENTREPRISE_COMBINAISON_TRAVAIL,
        "chaussures_securite": FACTEUR_ENTREPRISE_CHAUSSURES_SECURITE,
        "bottes_securite": FACTEUR_ENTREPRISE_BOTTES_SECURITE,
        "gants": FACTEUR_ENTREPRISE_GANTS,
        "casque": FACTEUR_ENTREPRISE_CASQUE,
    }
    return float(quantite or 0) * facteurs.get(type_vetement, 0)


# ==========================================
# ENTREPRISE — SCOPE 3 — ÉQUIPEMENTS
# ==========================================
# Réutilise les mêmes facteurs équipement que le Bâtiment.
def calcul_co2_entreprise_equipement(type_equipement, quantite):
    facteurs = {
        "ordinateur_portable": FACTEUR_BATIMENT_ORDINATEUR_UNITE,
        "ordinateur_bureau": FACTEUR_BATIMENT_ORDINATEUR_UNITE,
        "ecran": FACTEUR_BATIMENT_ECRAN_UNITE,
        "smartphone": 8.00,
        "imprimante": FACTEUR_BATIMENT_IMPRIMANTE_UNITE,
        "television": FACTEUR_BATIMENT_TELEVISION_UNITE,
        "scanner": FACTEUR_BATIMENT_AUTRE_EQUIPEMENT_UNITE,
        "videoprojecteur": FACTEUR_BATIMENT_AUTRE_EQUIPEMENT_UNITE,
        "mobilier": FACTEUR_BATIMENT_MOBILIER_KG,
    }
    return float(quantite or 0) * facteurs.get(type_equipement, 0)


# ==========================================
# ENTREPRISE — SCOPE 3 — TRANSPORT
# ==========================================
# Même facteurs kilométriques que le Bâtiment.
def calcul_co2_entreprise_voiture(distance_km):
    return float(distance_km or 0) * FACTEUR_BATIMENT_VOITURE_ESSENCE_KM


def calcul_co2_entreprise_bus(distance_km):
    return float(distance_km or 0) * FACTEUR_BATIMENT_BUS_PASSAGER_KM


def calcul_co2_entreprise_train(distance_km):
    return float(distance_km or 0) * FACTEUR_BATIMENT_TRAIN_PASSAGER_KM


def calcul_co2_entreprise_avion(distance_km):
    return float(distance_km or 0) * FACTEUR_BATIMENT_AVION_PASSAGER_KM


# ==========================================
# ENTREPRISE — SCOPE 3 — MARCHANDISES
# ==========================================
# Méthode retenue : distance × facteur véhicule-km.
# Hypothèse : camionnette essence de livraison légère.
FACTEUR_ENTREPRISE_CAMIONNETTE_ESSENCE_KM = 0.23963


def calcul_co2_entreprise_marchandises(distance_km):
    return (
        float(distance_km or 0)
        * FACTEUR_ENTREPRISE_CAMIONNETTE_ESSENCE_KM
    )

 