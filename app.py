from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def accueil():
    return render_template("accueil.html")


@app.route("/individu")
def individu():
    return render_template("individu.html")


# ==========================================
# BÂTIMENT — PAGES
# ==========================================

@app.route("/batiment")
def batiment():
    return render_template("batiment.html")


@app.route("/scope1_batiment")
def scope1_batiment():
    return render_template("scope1_batiment.html")


@app.route("/scope2_batiment")
def scope2_batiment():
    return render_template("scope2_batiment.html")


@app.route("/scope3_batiment")
def scope3_batiment():
    return render_template("scope3_batiment.html")


@app.route("/resultat_batiment")
def resultat_batiment():
    return render_template("resultat_batiment.html")


@app.route("/scope1")
def scope1():
    return render_template("scope1_individu.html")


@app.route("/scope2individu")
def scope2_individu():
    return render_template("scope2individu.html")


@app.route("/scope3individu")
def scope3_individu():
    return render_template("scope3individu.html")


@app.route("/calcul-scope1", methods=["POST"])
def calcul_scope1():

    from facteurs import (
        calcul_co2_essence,
        calcul_co2_diesel,
        calcul_co2_gpl,
        calcul_co2_gaz_m3,
        calcul_co2_gpl_bouteilles
    )

    donnees = request.get_json()

    # ==========================================
    # VARIABLES
    # ==========================================

    voiture = donnees.get("voiture")
    carburant = donnees.get("carburant")
    km_semaine = donnees.get("km_semaine")
    consommation = donnees.get("consommation")

    gaz_naturel = donnees.get("gaz_naturel")
    consommation_gaz = donnees.get("consommation_gaz")
    facture_gaz = donnees.get("facture_gaz")
    connait_gaz = donnees.get("connait_gaz")

    gpl = donnees.get("gpl")
    bouteilles_gpl = donnees.get("bouteilles_gpl")


    # ==========================================
    # INITIALISATION
    # ==========================================

    emissions_transport = 0
    emissions_gaz = 0
    emissions_gpl = 0


    # ==========================================
    # VOITURE
    # ==========================================

    if (
        voiture == "oui"
        and km_semaine is not None
        and consommation is not None
    ):

        # km/semaine → km/an

        km_annuels = (
            float(km_semaine)
            * 52
        )

        # L/100 km → litres/an

        litres_annuels = (
            km_annuels
            * float(consommation)
            / 100
        )


        if carburant == "essence":

            emissions_transport = calcul_co2_essence(
                litres_annuels
            )


        elif carburant == "diesel":

            emissions_transport = calcul_co2_diesel(
                litres_annuels
            )


        elif carburant == "gpl":

            emissions_transport = calcul_co2_gpl(
                litres_annuels
            )


    # ==========================================
    # GAZ NATUREL
    # ==========================================

    if gaz_naturel == "oui":

        consommation_mensuelle = 0


        # ------------------------------------------
        # CAS 1 : consommation connue
        # ------------------------------------------

        if (
            connait_gaz == "oui"
            and consommation_gaz is not None
        ):

            consommation_mensuelle = float(
                consommation_gaz
            )


        # ------------------------------------------
        # CAS 2 : consommation inconnue
        # Estimation avec la facture STEG
        #
        # Hypothèse du projet :
        # 1 TND ≈ 0,75 m³
        # ------------------------------------------

        elif (
            connait_gaz == "non"
            and facture_gaz is not None
        ):

            facture_mensuelle = float(
                facture_gaz
            )

            consommation_mensuelle = (
                facture_mensuelle
                * 0.75
            )


        # ------------------------------------------
        # Passage mensuel → annuel
        # ------------------------------------------

        consommation_annuelle = (
            consommation_mensuelle
            * 12
        )


        # ------------------------------------------
        # Calcul CO₂e
        # ------------------------------------------

        emissions_gaz = calcul_co2_gaz_m3(
            consommation_annuelle
        )


    # ==========================================
    # GPL DOMESTIQUE
    # ==========================================

    if (
        gpl == "oui"
        and bouteilles_gpl is not None
    ):

        emissions_gpl = (
            calcul_co2_gpl_bouteilles(
                float(bouteilles_gpl)
                * 12
            )
        )


    # ==========================================
    # TOTAL SCOPE 1
    # ==========================================

    total_scope1 = (
        emissions_transport
        + emissions_gaz
        + emissions_gpl
    )


    # ==========================================
    # RESULTAT
    # ==========================================

    resultat = {

        "transport": round(
            emissions_transport,
            2
        ),

        "gaz_naturel": round(
            emissions_gaz,
            2
        ),

        "gpl": round(
            emissions_gpl,
            2
        ),

        "total_scope1": round(
            total_scope1,
            2
        )

    }


    print(
        "Résultat Scope 1 :",
        resultat
    )


    return {
        "message": "Calcul Scope 1 effectué",
        "resultat": resultat
    }
@app.route("/calcul-scope2", methods=["POST"])
def calcul_scope2():

    from facteurs import calcul_co2_electricite

    donnees = request.get_json()

    connait_electricite = donnees.get(
        "connait_electricite"
    )

    consommation_electricite = donnees.get(
        "consommation_electricite"
    )

    facture_electricite = donnees.get(
        "facture_electricite"
    )


    # ==========================================
    # INITIALISATION
    # ==========================================

    emissions_electricite = 0


    # ==========================================
    # CAS 1 :
    # CONSOMMATION CONNUE
    # ==========================================

    if (
        connait_electricite == "oui"
        and consommation_electricite is not None
    ):

        consommation_mensuelle = float(
            consommation_electricite
        )


    # ==========================================
    # CAS 2 :
    # CONSOMMATION INCONNUE
    # FACTURE STEG
    # ==========================================

    elif (
        connait_electricite == "non"
        and facture_electricite is not None
    ):

        facture_mensuelle = float(
            facture_electricite
        )

        # Hypothèse du projet
        # à définir pour convertir
        # la facture en kWh

        consommation_mensuelle = (
            facture_mensuelle
            * 3.125
        )

# Hypothèse du projet :
# Lorsque la consommation en kWh n'est pas connue,on fait l'estimation a partir de la facture du steg , 
#comme le prix d'un kwh depedn de la consoommation de la maison , on a pris comme estimation 1dt=3.125kwh 
    else:
        consommation_mensuelle = 0


    # ==========================================
    # MENSUEL → ANNUEL
    # ==========================================

    consommation_annuelle = (
        consommation_mensuelle
        * 12
    )


    # ==========================================
    # CALCUL CO2e
    # ==========================================

    emissions_electricite = (
        calcul_co2_electricite(
            consommation_annuelle
        )
    )


    # ==========================================
    # RESULTAT
    # ==========================================

    resultat = {

        "electricite": round(
            emissions_electricite,
            2
        ),

        "total_scope2": round(
            emissions_electricite,
            2
        )

    }


    print(
        "Résultat Scope 2 :",
        resultat
    )


    return {
        "message": "Calcul Scope 2 effectué",
        "resultat": resultat
    }
@app.route("/calcul-scope3", methods=["POST"])
def calcul_scope3():

    from facteurs import (
        calcul_co2_viande_rouge,
        calcul_co2_poulet,
        calcul_co2_poisson,
        calcul_co2_produits_laitiers,
        calcul_co2_bus,
        calcul_co2_train,
        calcul_co2_taxi,
        calcul_co2_avion,
        calcul_co2_vetements,
        calcul_co2_chaussures,
        calcul_co2_smartphones,
        calcul_co2_ordinateurs,
        calcul_co2_televisions,
        calcul_co2_eau,
        calcul_co2_dechets
    )

    donnees = request.get_json()

    # ==========================================
    # INITIALISATION
    # ==========================================

    emissions_alimentation = 0
    emissions_transport = 0
    emissions_achats = 0
    emissions_eau = 0
    emissions_dechets = 0


    # ==========================================
    # ALIMENTATION
    # ==========================================

    viande_rouge = donnees.get(
        "viande_rouge", 0
    )

    poulet = donnees.get(
        "poulet", 0
    )

    poisson = donnees.get(
        "poisson", 0
    )

    produits_laitiers = donnees.get(
        "produits_laitiers", 0
    )


    emissions_alimentation = (

        calcul_co2_viande_rouge(
            float(viande_rouge)
        )

        + calcul_co2_poulet(
            float(poulet)
        )

        + calcul_co2_poisson(
            float(poisson)
        )

        + calcul_co2_produits_laitiers(
            float(produits_laitiers)
        )

    )


    # ==========================================
    # TRANSPORT — BUS
    # ==========================================

    jours_bus = donnees.get(
        "jours_bus", 0
    )

    distance_bus = donnees.get(
        "distance_bus", 0
    )

    emissions_bus = calcul_co2_bus(
        float(jours_bus),
        float(distance_bus)
    )


    # ==========================================
    # TRANSPORT — TRAIN
    # ==========================================

    trajets_train = donnees.get(
        "trajets_train", 0
    )

    distance_train = donnees.get(
        "distance_train", 0
    )

    emissions_train = calcul_co2_train(
        float(trajets_train),
        float(distance_train)
    )


    # ==========================================
    # TRANSPORT — TAXI
    # ==========================================

    trajets_taxi = donnees.get(
        "trajets_taxi", 0
    )

    distance_taxi = donnees.get(
        "distance_taxi", 0
    )

    emissions_taxi = calcul_co2_taxi(
        float(trajets_taxi),
        float(distance_taxi)
    )


    # ==========================================
    # AVION
    # ==========================================

    voyages_court = donnees.get(
        "voyages_avion_court", 0
    )

    voyages_moyen = donnees.get(
        "voyages_avion_moyen", 0
    )

    voyages_long = donnees.get(
        "voyages_avion_long", 0
    )


    emissions_avion = (

        calcul_co2_avion(
            float(voyages_court),
            "court"
        )

        + calcul_co2_avion(
            float(voyages_moyen),
            "moyen"
        )

        + calcul_co2_avion(
            float(voyages_long),
            "long"
        )

    )


    emissions_transport = (

        emissions_bus
        + emissions_train
        + emissions_taxi
        + emissions_avion

    )


    # ==========================================
    # ACHATS
    # ==========================================

    vetements = donnees.get(
        "vetements", 0
    )

    chaussures = donnees.get(
        "chaussures", 0
    )

    smartphones = donnees.get(
        "smartphones", 0
    )

    ordinateurs = donnees.get(
        "ordinateurs", 0
    )

    televisions = donnees.get(
        "televisions", 0
    )


    emissions_achats = (

        calcul_co2_vetements(
            float(vetements)
        )

        + calcul_co2_chaussures(
            float(chaussures)
        )

        + calcul_co2_smartphones(
            float(smartphones)
        )

        + calcul_co2_ordinateurs(
            float(ordinateurs)
        )

        + calcul_co2_televisions(
            float(televisions)
        )

    )


    # ==========================================
    # EAU
    # ==========================================

    consommation_eau = donnees.get(
        "consommation_eau"
    )

    facture_eau = donnees.get(
        "facture_eau"
    )

    connait_eau = donnees.get(
        "connait_eau"
    )


    if (
        connait_eau == "oui"
        and consommation_eau is not None
    ):

        consommation_eau_annuelle = float(
            consommation_eau
        )


    elif (
        connait_eau == "non"
        and facture_eau is not None
    ):

        facture_eau_mensuelle = float(
            facture_eau
        )

        # Hypothèse du projet :
        # à définir comme pour la facture STEG

        consommation_eau_annuelle = (
            facture_eau_mensuelle
            * 3.125
            * 12
        )


    else:

        consommation_eau_annuelle = 0


    emissions_eau = calcul_co2_eau(
        consommation_eau_annuelle
    )


    # ==========================================
    # DÉCHETS
    # ==========================================

    habitants = donnees.get(
        "habitants", 0
    )

    # Valeur provisoire :
    # production moyenne de déchets
    # par habitant et par an.
    #
    # À préciser selon le mode de gestion.

    production_dechets_tonnes = (
        float(habitants)
        * 0.365
    )


    emissions_dechets = calcul_co2_dechets(
        production_dechets_tonnes
    )


    # ==========================================
    # TOTAL SCOPE 3
    # ==========================================

    total_scope3 = (

        emissions_alimentation
        + emissions_transport
        + emissions_achats
        + emissions_eau
        + emissions_dechets

    )


    # ==========================================
    # RÉSULTAT
    # ==========================================

    resultat = {

        "alimentation": round(
            emissions_alimentation,
            2
        ),

        "transport": round(
            emissions_transport,
            2
        ),

        "achats": round(
            emissions_achats,
            2
        ),

        "eau": round(
            emissions_eau,
            2
        ),

        "dechets": round(
            emissions_dechets,
            2
        ),

        "total_scope3": round(
            total_scope3,
            2
        )

    }


    print(
        "Résultat Scope 3 :",
        resultat
    )


    return {
        "message": "Calcul Scope 3 effectué",
        "resultat": resultat
    }



# ==========================================
# BÂTIMENT — CALCUL SCOPE 1
# ==========================================

@app.route("/calcul-scope1-batiment", methods=["POST"])
def calcul_scope1_batiment():

    from facteurs import (
        calcul_co2_batiment_gaz_naturel,
        calcul_co2_batiment_gpl,
        calcul_co2_batiment_fioul,
        calcul_co2_batiment_diesel,
        calcul_co2_batiment_refrigerant
    )

    donnees = request.get_json() or {}

    emissions_gaz = calcul_co2_batiment_gaz_naturel(
        float(donnees.get("gaz_naturel_m3", 0) or 0)
    )
    emissions_gpl = calcul_co2_batiment_gpl(
        float(donnees.get("gpl_kg", 0) or 0)
    )
    emissions_fioul = calcul_co2_batiment_fioul(
        float(donnees.get("fioul_litres", 0) or 0)
    )
    emissions_diesel = calcul_co2_batiment_diesel(
        float(donnees.get("diesel_litres", 0) or 0)
    )

    emissions_refrigerant = 0

    if donnees.get("refrigerant") == "oui":
        emissions_refrigerant = calcul_co2_batiment_refrigerant(
            donnees.get("type_refrigerant"),
            float(donnees.get("quantite_refrigerant", 0) or 0)
        )

    # Autres combustibles : facteurs non figés à ce stade.
    emissions_autres = 0

    total = (
        emissions_gaz
        + emissions_gpl
        + emissions_fioul
        + emissions_diesel
        + emissions_autres
        + emissions_refrigerant
    )

    resultat = {
        "gaz_naturel": round(emissions_gaz, 2),
        "gpl": round(emissions_gpl, 2),
        "fioul": round(emissions_fioul, 2),
        "diesel": round(emissions_diesel, 2),
        "autres_combustibles": round(emissions_autres, 2),
        "refrigerants": round(emissions_refrigerant, 2),
        "total_scope1": round(total, 2)
    }

    print("Résultat Scope 1 Bâtiment :", resultat)

    return {
        "message": "Calcul Scope 1 bâtiment effectué",
        "resultat": resultat
    }


# ==========================================
# BÂTIMENT — CALCUL SCOPE 2
# ==========================================

@app.route("/calcul-scope2-batiment", methods=["POST"])
def calcul_scope2_batiment():

    from facteurs import calcul_co2_batiment_electricite

    donnees = request.get_json() or {}

    electricite_achetee = float(
        donnees.get("electricite_achetee", 0) or 0
    )

    emissions_electricite = calcul_co2_batiment_electricite(
        electricite_achetee
    )

    resultat = {
        "electricite": round(emissions_electricite, 2),
        "total_scope2": round(emissions_electricite, 2),
        "photovoltaique": donnees.get("photovoltaique", "non"),
        "production_photovoltaique": round(
            float(donnees.get("production_photovoltaique", 0) or 0), 2
        ),
        "autoconsommation_photovoltaique": round(
            float(donnees.get("autoconsommation_photovoltaique", 0) or 0), 2
        ),
        "electricite_injectee": round(
            float(donnees.get("electricite_injectee", 0) or 0), 2
        )
    }

    print("Résultat Scope 2 Bâtiment :", resultat)

    return {
        "message": "Calcul Scope 2 bâtiment effectué",
        "resultat": resultat
    }


# ==========================================
# BÂTIMENT — CALCUL SCOPE 3
# ==========================================

@app.route("/calcul-scope3-batiment", methods=["POST"])
def calcul_scope3_batiment():

    from facteurs import (
        calcul_co2_eau,
        calcul_co2_beton,
        calcul_co2_ciment,
        calcul_co2_acier,
        calcul_co2_brique,
        calcul_co2_verre,
        calcul_co2_isolation,
        calcul_co2_dechet_batiment,
        calcul_co2_batiment_voiture,
        calcul_co2_batiment_bus,
        calcul_co2_batiment_train,
        calcul_co2_batiment_avion,
        calcul_co2_aluminium,
        calcul_co2_batiment_equipements,
    )

    donnees = request.get_json() or {}

    # ==========================================
    # EAU
    # ==========================================
    emissions_eau = calcul_co2_eau(
        float(donnees.get("consommation_eau", 0) or 0)
    )

    # ==========================================
    # DÉCHETS
    # ==========================================
    # Le formulaire bâtiment ne demande pas de traitement.
    # Hypothèse bâtiment : enfouissement comme traitement par défaut.
    dechets = donnees.get("dechets", {}) or {}

    emissions_dechets = 0
    categories_dechets = {
        "papier_carton": "papier_carton",
        "plastique": "plastique",
        "verre": "verre",
        "metaux": "metaux",
        "organiques": "organique_mixte",
        "menagers": "residuel",
    }

    for champ, type_facteur in categories_dechets.items():
        quantite = float(dechets.get(champ, 0) or 0)
        emissions_dechets += calcul_co2_dechet_batiment(
            type_facteur,
            quantite,
            "enfouissement"
        )

    # ==========================================
    # DÉPLACEMENTS
    # ==========================================
    # Les distances saisies dans le formulaire sont déjà annuelles.
    # Voiture : essence par défaut car le formulaire bâtiment
    # ne distingue pas le carburant.
    domicile = donnees.get("domicile_travail", {}) or {}
    professionnels = donnees.get("deplacements_professionnels", {}) or {}

    emissions_deplacements = 0

    emissions_deplacements += calcul_co2_batiment_voiture(
        float(domicile.get("voiture", 0) or 0),
        "essence"
    )
    emissions_deplacements += calcul_co2_batiment_bus(
        float(domicile.get("bus", 0) or 0)
    )
    emissions_deplacements += calcul_co2_batiment_train(
        float(domicile.get("train", 0) or 0)
    )

    emissions_deplacements += calcul_co2_batiment_voiture(
        float(professionnels.get("voiture", 0) or 0),
        "essence"
    )
    emissions_deplacements += calcul_co2_batiment_train(
        float(professionnels.get("train", 0) or 0)
    )
    emissions_deplacements += calcul_co2_batiment_avion(
        float(professionnels.get("avion", 0) or 0)
    )

    # ==========================================
    # ACHATS / MOBILIER / INFORMATIQUE
    # ==========================================
    # Les facteurs par unité sont centralisés dans facteurs.py.
    emissions_achats = 0

    emissions_achats += calcul_co2_batiment_equipements(
        "mobilier",
        float(donnees.get("mobilier_kg", 0) or 0)
    )
    emissions_achats += calcul_co2_batiment_equipements(
        "ordinateur",
        float((donnees.get("informatique", {}) or {}).get("ordinateurs", 0) or 0)
    )
    emissions_achats += calcul_co2_batiment_equipements(
        "ecran",
        float((donnees.get("informatique", {}) or {}).get("ecrans", 0) or 0)
    )
    emissions_achats += calcul_co2_batiment_equipements(
        "imprimante",
        float((donnees.get("informatique", {}) or {}).get("imprimantes", 0) or 0)
    )

    # Autres équipements sélectionnés + quantités.
    quantites_autres = donnees.get("quantites_autres_equipements", {}) or {}
    for type_equipement, quantite in quantites_autres.items():
        emissions_achats += calcul_co2_batiment_equipements(
            type_equipement,
            float(quantite or 0)
        )

    # ==========================================
    # TRAVAUX / RÉNOVATION / MATÉRIAUX
    # ==========================================
    emissions_travaux = 0

    if donnees.get("travaux") == "oui":

        emissions_travaux += calcul_co2_beton(
            float(donnees.get("beton_kg", 0) or 0)
        )

        emissions_travaux += calcul_co2_ciment(
            float(donnees.get("ciment_kg", 0) or 0),
            donnees.get("type_ciment")
        )

        emissions_travaux += calcul_co2_acier(
            float(donnees.get("acier_kg", 0) or 0)
        )

        emissions_travaux += calcul_co2_brique(
            float(donnees.get("briques_kg", 0) or 0)
        )

        emissions_travaux += calcul_co2_verre(
            float(donnees.get("verre_kg", 0) or 0),
            donnees.get("type_verre")
        )

        emissions_travaux += calcul_co2_isolation(
            float(donnees.get("isolation_kg", 0) or 0),
            donnees.get("type_isolation")
        )

        emissions_travaux += calcul_co2_aluminium(
            float(donnees.get("aluminium_kg", 0) or 0)
        )

    # ==========================================
    # TOTAL SCOPE 3
    # ==========================================
    total = (
        emissions_eau
        + emissions_dechets
        + emissions_deplacements
        + emissions_achats
        + emissions_travaux
    )

    resultat = {
        "eau": round(emissions_eau, 2),
        "dechets": round(emissions_dechets, 2),
        "deplacements": round(emissions_deplacements, 2),
        "achats": round(emissions_achats, 2),
        "travaux": round(emissions_travaux, 2),
        "total_scope3": round(total, 2)
    }

    print("Résultat Scope 3 Bâtiment :", resultat)

    return {
        "message": "Calcul Scope 3 bâtiment effectué",
        "resultat": resultat
    }




# ==========================================
# ENTREPRISE — PAGES
# ==========================================

@app.route("/entreprise")
def entreprise():
    return render_template("entreprise.html")


@app.route("/scope1_entreprise")
def scope1_entreprise():
    return render_template("scope1_entreprise.html")


@app.route("/scope2_entreprise")
def scope2_entreprise():
    return render_template("scope2_entreprise.html")


@app.route("/scope3_entreprise")
def scope3_entreprise():
    return render_template("scope3_entreprise.html")


@app.route("/resultat_entreprise")
def resultat_entreprise():
    return render_template("resultat_entreprise.html")


# ==========================================
# ENTREPRISE — CALCUL SCOPE 1
# ==========================================

@app.route("/calcul-scope1-entreprise", methods=["POST"])
def calcul_scope1_entreprise():

    from facteurs import (
        calcul_co2_essence,
        calcul_co2_diesel,
        calcul_co2_gpl,
        calcul_co2_gaz_m3,
        calcul_co2_batiment_gpl,
        calcul_co2_batiment_fioul,
        calcul_co2_batiment_diesel,
        calcul_co2_batiment_refrigerant,
    )

    d = request.get_json() or {}

    essence = calcul_co2_essence(
        float(d.get("essence_litres", 0) or 0)
    )

    diesel = calcul_co2_diesel(
        float(d.get("diesel_litres", 0) or 0)
    )

    gpl_vehicules = calcul_co2_gpl(
        float(d.get("gpl_litres", 0) or 0)
    )

    gaz = calcul_co2_gaz_m3(
        float(d.get("gaz_naturel_m3", 0) or 0)
    )

    gpl_site = calcul_co2_batiment_gpl(
        float(d.get("gpl_site_kg", 0) or 0)
    )

    fioul = calcul_co2_batiment_fioul(
        float(d.get("fioul_litres", 0) or 0)
    )

    diesel_site = calcul_co2_batiment_diesel(
        float(d.get("diesel_site_litres", 0) or 0)
    )

    refrigerants = 0

    if d.get("refrigerant") == "oui":
        refrigerants = calcul_co2_batiment_refrigerant(
            d.get("type_refrigerant"),
            float(d.get("quantite_refrigerant", 0) or 0),
        )

    total = (
        essence
        + diesel
        + gpl_vehicules
        + gaz
        + gpl_site
        + fioul
        + diesel_site
        + refrigerants
    )

    resultat = {
        "essence": round(essence, 2),
        "diesel": round(diesel, 2),
        "gpl": round(gpl_vehicules + gpl_site, 2),
        "gaz_naturel": round(gaz, 2),
        "fioul": round(fioul, 2),
        "diesel_site": round(diesel_site, 2),
        "refrigerants": round(refrigerants, 2),
        "total_scope1": round(total, 2),
    }

    return {
        "message": "Calcul Scope 1 entreprise effectué",
        "resultat": resultat,
    }


# ==========================================
# ENTREPRISE — CALCUL SCOPE 2
# ==========================================

@app.route("/calcul-scope2-entreprise", methods=["POST"])
def calcul_scope2_entreprise():

    from facteurs import calcul_co2_electricite

    d = request.get_json() or {}

    consommation_totale = float(
        d.get("consommation_electricite", 0) or 0
    )

    pv = d.get("photovoltaique", "non")

    production_pv = max(
        float(d.get("production_photovoltaique", 0) or 0),
        0,
    )

    autoconsommation_pv = max(
        float(d.get("autoconsommation_photovoltaique", 0) or 0),
        0,
    )

    autoconsommation_pv = min(
        autoconsommation_pv,
        production_pv,
    )

    electricite_achetee = max(
        consommation_totale - autoconsommation_pv,
        0,
    )

    emissions = calcul_co2_electricite(
        electricite_achetee
    )

    injectee = 0

    if pv == "oui":
        injectee = max(
            production_pv - autoconsommation_pv,
            0,
        )

    resultat = {
        "consommation_totale": round(consommation_totale, 2),
        "electricite_achetee": round(electricite_achetee, 2),
        "photovoltaique": pv,
        "production_photovoltaique": round(production_pv, 2),
        "autoconsommation_photovoltaique": round(autoconsommation_pv, 2),
        "electricite_injectee": round(injectee, 2),
        "electricite": round(emissions, 2),
        "total_scope2": round(emissions, 2),
    }

    return {
        "message": "Calcul Scope 2 entreprise effectué",
        "resultat": resultat,
    }


# ==========================================
# ENTREPRISE — CALCUL SCOPE 3
# ==========================================

@app.route("/calcul-scope3-entreprise", methods=["POST"])
def calcul_scope3_entreprise():

    from facteurs import (
        calcul_co2_entreprise_vetement,
        calcul_co2_entreprise_equipement,
        calcul_co2_entreprise_voiture,
        calcul_co2_entreprise_bus,
        calcul_co2_entreprise_train,
        calcul_co2_entreprise_avion,
        calcul_co2_entreprise_marchandises,
        calcul_co2_eau,
    )

    d = request.get_json() or {}

    # Vêtements / EPI
    vetements = 0
    for item in (
        "polo",
        "pantalon",
        "veste",
        "combinaison",
        "chaussures_securite",
        "bottes_securite",
        "gants",
        "casque",
    ):
        vetements += calcul_co2_entreprise_vetement(
            item,
            d.get(f"vetement_{item}", 0),
        )

    # Équipements / immobilisations
    equipements = 0
    for item in (
        "ordinateur_portable",
        "ordinateur_bureau",
        "ecran",
        "smartphone",
        "imprimante",
        "television",
        "scanner",
        "videoprojecteur",
        "mobilier",
    ):
        equipements += calcul_co2_entreprise_equipement(
            item,
            d.get(f"equipement_{item}", 0),
        )

    # Domicile-travail
    domicile_travail = (
        calcul_co2_entreprise_voiture(d.get("domicile_voiture_km", 0))
        + calcul_co2_entreprise_bus(d.get("domicile_bus_km", 0))
        + calcul_co2_entreprise_train(d.get("domicile_train_km", 0))
    )

    # Déplacements professionnels
    deplacements_pro = (
        calcul_co2_entreprise_voiture(d.get("pro_voiture_km", 0))
        + calcul_co2_entreprise_bus(d.get("pro_bus_km", 0))
        + calcul_co2_entreprise_train(d.get("pro_train_km", 0))
        + calcul_co2_entreprise_avion(d.get("pro_avion_km", 0))
    )

    transport = domicile_travail + deplacements_pro

    # Marchandises par kilométrage
    marchandises_amont = calcul_co2_entreprise_marchandises(
        d.get("transport_amont_km", 0)
    )
    marchandises_aval = calcul_co2_entreprise_marchandises(
        d.get("transport_aval_km", 0)
    )
    marchandises = marchandises_amont + marchandises_aval

    # Déchets : recyclé / non recyclé
    facteurs_recyclage = {
        "papier_carton": 4.65358,
        "plastique": 4.65358,
        "verre": 4.65358,
        "metaux": 1.01398,
        "organiques": 0.0,
        "residuels": 4.65358,
    }

    facteurs_enfouissement = {
        "papier_carton": 1164.51317,
        "plastique": 9.00687,
        "verre": 9.00687,
        "metaux": 1.26435,
        "organiques": 656.10991,
        "residuels": 497.28993,
    }

    dechets = 0

    for item in facteurs_recyclage:
        total_t = max(
            float(d.get(f"dechets_{item}", 0) or 0),
            0,
        )

        recycle_t = min(
            max(float(d.get(f"recycles_{item}", 0) or 0), 0),
            total_t,
        )

        non_recycle_t = total_t - recycle_t

        dechets += (
            recycle_t * facteurs_recyclage[item]
            + non_recycle_t * facteurs_enfouissement[item]
        )

    # Eau
    eau = calcul_co2_eau(
        float(d.get("consommation_eau", 0) or 0)
    )

    # Voyages professionnels
    voyages = float(
        d.get("voyages_avion", 0) or 0
    )

    # Même hypothèse que l'ancien calcul avion de l'Individu :
    # court-courrier = 500 km et facteur 0,125 kgCO2e/passager-km.
    voyages_avion = (
        voyages
        * 500
        * 0.125
    )

    total = (
        vetements
        + equipements
        + transport
        + marchandises
        + dechets
        + eau
        + voyages_avion
    )

    resultat = {
        "vetements_epi": round(vetements, 2),
        "equipements": round(equipements, 2),
        "domicile_travail": round(domicile_travail, 2),
        "deplacements_professionnels": round(deplacements_pro, 2),
        "transport": round(transport, 2),
        "marchandises_amont": round(marchandises_amont, 2),
        "marchandises_aval": round(marchandises_aval, 2),
        "marchandises": round(marchandises, 2),
        "dechets": round(dechets, 2),
        "eau": round(eau, 2),
        "voyages_avion": round(voyages_avion, 2),
        "total_scope3": round(total, 2),
    }

    return {
        "message": "Calcul Scope 3 entreprise effectué",
        "resultat": resultat,
    }

@app.route("/resultat")
def resultat():
    return render_template("resultat.html")

if __name__ == "__main__":
    app.run(debug=True) 

    