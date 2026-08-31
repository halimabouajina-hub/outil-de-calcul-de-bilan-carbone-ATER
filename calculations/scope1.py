def calculate_scope1(data):

    # =========================
    # VOITURE
    # =========================

    transport = 0

    if data.get("voiture") == "oui":

        km_semaine = float(data.get("km_semaine", 0))
        consommation = float(data.get("consommation", 0))
        carburant = data.get("carburant")

        # Distance annuelle
        km_annuel = km_semaine * 52

        # Consommation annuelle en litres
        litres_annuels = km_annuel * consommation / 100

        # Facteurs d'émission
facteur_essence = 2.31  # kg CO2e / litre
facteur_diesel = 2.62   # kg CO2e / litre

if carburant == "essence":
    transport = litres_annuels * facteur_essence

elif carburant == "diesel":
    transport = litres_annuels * facteur_diesel