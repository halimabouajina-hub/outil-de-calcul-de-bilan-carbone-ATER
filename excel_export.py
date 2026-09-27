from io import BytesIO
from typing import Any, Dict

try:
    import xlsxwriter
except ImportError as exc:
    raise ImportError(
        "Le module 'XlsxWriter' est nécessaire pour l'export Excel. "
        "Installe-le avec : pip install XlsxWriter"
    ) from exc


def _num(value: Any) -> float:
    """Convertit une valeur en nombre."""
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def _write_scope_sheet(
    workbook,
    sheet_name: str,
    scope_title: str,
    data: Dict[str, Any],
    postes: list,
    formats: dict
):
    """
    Crée une feuille détaillée pour un scope.
    """

    ws = workbook.add_worksheet(sheet_name)

    title = formats["title"]
    header = formats["header"]
    label = formats["label"]
    value_format = formats["editable"]
    total_format = formats["total"]
    note = formats["note"]

    # Largeur des colonnes
    ws.set_column("A:A", 40)
    ws.set_column("B:B", 22)
    ws.set_column("C:C", 18)
    ws.set_column("D:D", 22)

    # Titre
    ws.merge_range(
        "A1:D1",
        scope_title,
        title
    )
    ws.set_row(0, 28)

    # En-têtes
    ws.write("A3", "Poste", header)
    ws.write("B3", "Valeur / émission", header)
    ws.write("C3", "Unité", header)
    ws.write("D3", "Clé utilisée", header)

    row = 3

    for poste in postes:

        label_poste = poste["label"]
        key = poste["key"]

        valeur = _num(data.get(key, 0))

        ws.write(row, 0, label_poste, label)

        ws.write_number(
            row,
            1,
            valeur,
            value_format
        )

        ws.write(
            row,
            2,
            "kg CO₂e/an",
            label
        )

        ws.write(
            row,
            3,
            key,
            label
        )

        row += 1

    # Total du scope
    total_row = row

    ws.write(
        total_row,
        0,
        f"Total {sheet_name}",
        header
    )

    if row > 3:
        ws.write_formula(
            total_row,
            1,
            f"=SUM(B4:B{row})",
            total_format
        )
    else:
        ws.write_number(
            total_row,
            1,
            0,
            total_format
        )

    ws.write(
        total_row,
        2,
        "kg CO₂e/an",
        total_format
    )

    ws.write(
        total_row,
        3,
        f"Total calculé à partir des postes",
        total_format
    )

    # Total reçu du résultat
    total_key = {
        "Scope 1": "total_scope1",
        "Scope 2": "total_scope2",
        "Scope 3": "total_scope3",
    }.get(sheet_name)

    if total_key:
        received_total = _num(data.get(total_key, 0))

        row += 2

        ws.write(
            row,
            0,
            "Total enregistré dans le bilan",
            header
        )

        ws.write_number(
            row,
            1,
            received_total,
            value_format
        )

        ws.write(
            row,
            2,
            "kg CO₂e/an",
            label
        )

        ws.write(
            row,
            3,
            total_key,
            label
        )

    row += 2

    ws.merge_range(
        row,
        0,
        row + 1,
        3,
        "Les valeurs jaunes correspondent aux émissions détaillées transmises par le bilan. "
        "Le total de la feuille est recalculé automatiquement par Excel.",
        note
    )

    ws.freeze_panes(3, 0)

    return ws


def _build_workbook(
    profile: str,
    scope1: Dict[str, Any],
    scope2: Dict[str, Any],
    scope3: Dict[str, Any]
) -> BytesIO:

    output = BytesIO()

    workbook = xlsxwriter.Workbook(
        output,
        {"in_memory": True}
    )

    # =========================================================
    # FORMATS
    # =========================================================

    title = workbook.add_format({
        "bold": True,
        "font_size": 18,
        "font_color": "#ffffff",
        "bg_color": "#2c8062",
        "align": "center",
        "valign": "vcenter"
    })

    section = workbook.add_format({
        "bold": True,
        "font_size": 12,
        "font_color": "#ffffff",
        "bg_color": "#4f8f77",
        "border": 1
    })

    header = workbook.add_format({
        "bold": True,
        "bg_color": "#e7eee9",
        "border": 1
    })

    label = workbook.add_format({
        "border": 1
    })

    editable = workbook.add_format({
        "border": 1,
        "num_format": "#,##0.00",
        "bg_color": "#fff2cc"
    })

    formula = workbook.add_format({
        "border": 1,
        "num_format": "#,##0.00",
        "bg_color": "#eaf2f8"
    })

    total = workbook.add_format({
        "bold": True,
        "border": 1,
        "top": 2,
        "num_format": "#,##0.00",
        "bg_color": "#d9ead3"
    })

    percent = workbook.add_format({
        "border": 1,
        "num_format": "0.00%"
    })

    note = workbook.add_format({
        "italic": True,
        "font_color": "#6f7772",
        "text_wrap": True,
        "valign": "top"
    })

    formats = {
        "title": title,
        "section": section,
        "header": header,
        "label": label,
        "editable": editable,
        "formula": formula,
        "total": total,
        "percent": percent,
        "note": note
    }

    # =========================================================
    # POSTES PAR PROFIL
    # =========================================================

    if profile == "Individu":

        scope1_postes = [
            {
                "label": "Transport",
                "key": "transport"
            },
            {
                "label": "Gaz naturel",
                "key": "gaz_naturel"
            },
            {
                "label": "GPL",
                "key": "gpl"
            },
        ]

        scope2_postes = [
            {
                "label": "Électricité",
                "key": "electricite"
            },
        ]

        scope3_postes = [
            {
                "label": "Alimentation",
                "key": "alimentation"
            },
            {
                "label": "Transport",
                "key": "transport"
            },
            {
                "label": "Achats",
                "key": "achats"
            },
            {
                "label": "Eau",
                "key": "eau"
            },
            {
                "label": "Déchets",
                "key": "dechets"
            },
        ]

    elif profile == "Bâtiment":

        scope1_postes = [
            {
                "label": "Gaz naturel",
                "key": "gaz_naturel"
            },
            {
                "label": "GPL",
                "key": "gpl"
            },
            {
                "label": "Fioul",
                "key": "fioul"
            },
            {
                "label": "Diesel",
                "key": "diesel"
            },
            {
                "label": "Autres combustibles",
                "key": "autres_combustibles"
            },
            {
                "label": "Réfrigérants",
                "key": "refrigerants"
            },
        ]

        scope2_postes = [
            {
                "label": "Électricité",
                "key": "electricite"
            },
        ]

        scope3_postes = [
            {
                "label": "Eau",
                "key": "eau"
            },
            {
                "label": "Déchets",
                "key": "dechets"
            },
            {
                "label": "Déplacements",
                "key": "deplacements"
            },
            {
                "label": "Achats / mobilier / informatique",
                "key": "achats"
            },
            {
                "label": "Travaux / matériaux",
                "key": "travaux"
            },
        ]

    else:

        scope1_postes = [
            {
                "label": "Essence",
                "key": "essence"
            },
            {
                "label": "Diesel",
                "key": "diesel"
            },
            {
                "label": "GPL",
                "key": "gpl"
            },
            {
                "label": "Gaz naturel",
                "key": "gaz_naturel"
            },
            {
                "label": "Fioul",
                "key": "fioul"
            },
            {
                "label": "Diesel site",
                "key": "diesel_site"
            },
            {
                "label": "Réfrigérants",
                "key": "refrigerants"
            },
        ]

        scope2_postes = [
            {
                "label": "Électricité",
                "key": "electricite"
            },
        ]

        scope3_postes = [
            {
                "label": "Vêtements & EPI",
                "key": "vetements_epi"
            },
            {
                "label": "Équipements",
                "key": "equipements"
            },
            {
                "label": "Domicile → travail",
                "key": "domicile_travail"
            },
            {
                "label": "Déplacements professionnels",
                "key": "deplacements_professionnels"
            },
            {
                "label": "Marchandises amont",
                "key": "marchandises_amont"
            },
            {
                "label": "Marchandises aval",
                "key": "marchandises_aval"
            },
            {
                "label": "Déchets",
                "key": "dechets"
            },
            {
                "label": "Eau",
                "key": "eau"
            },
        ]

    # =========================================================
    # FEUILLES DES SCOPES
    # =========================================================

    _write_scope_sheet(
        workbook,
        "Scope 1",
        f"Tunicarbone — {profile} — Scope 1",
        scope1,
        scope1_postes,
        formats
    )

    _write_scope_sheet(
        workbook,
        "Scope 2",
        f"Tunicarbone — {profile} — Scope 2",
        scope2,
        scope2_postes,
        formats
    )

    _write_scope_sheet(
        workbook,
        "Scope 3",
        f"Tunicarbone — {profile} — Scope 3",
        scope3,
        scope3_postes,
        formats
    )

    # =========================================================
    # FEUILLE SYNTHÈSE
    # =========================================================

    ws = workbook.add_worksheet("Synthèse")

    ws.set_column("A:A", 36)
    ws.set_column("B:B", 24)
    ws.set_column("C:C", 18)

    ws.merge_range(
        "A1:C1",
        f"Tunicarbone — Bilan {profile}",
        title
    )

    ws.set_row(0, 30)

    # Profil
    ws.write("A3", "Profil", header)
    ws.write("B3", profile, label)

    # -------------------------
    # Scope 1
    # -------------------------

    ws.write(
        "A5",
        "Scope 1",
        header
    )

    ws.write_formula(
        "B5",
        "='Scope 1'!B10",
        formula
    )

    ws.write(
        "C5",
        "kg CO₂e/an",
        label
    )

    # -------------------------
    # Scope 2
    # -------------------------

    ws.write(
        "A6",
        "Scope 2",
        header
    )

    ws.write_formula(
        "B6",
        "='Scope 2'!B8",
        formula
    )

    ws.write(
        "C6",
        "kg CO₂e/an",
        label
    )

    # -------------------------
    # Scope 3
    # -------------------------

    ws.write(
        "A7",
        "Scope 3",
        header
    )

    # Le total est placé après les postes.
    if profile == "Individu":
        scope3_total_row = 9
    elif profile == "Bâtiment":
        scope3_total_row = 9
    else:
        scope3_total_row = 12

    ws.write_formula(
        "B7",
        f"='Scope 3'!B{scope3_total_row}",
        formula
    )

    ws.write(
        "C7",
        "kg CO₂e/an",
        label
    )

    # -------------------------
    # Total général
    # -------------------------

    ws.write(
        "A9",
        "Empreinte carbone totale",
        header
    )

    ws.write_formula(
        "B9",
        "=SUM(B5:B7)",
        total
    )

    ws.write(
        "C9",
        "kg CO₂e/an",
        total
    )

    # -------------------------
    # Pourcentages
    # -------------------------

    ws.write(
        "A11",
        "Répartition des émissions",
        section
    )

    ws.merge_range(
        "A11:C11",
        "Répartition des émissions",
        section
    )

    ws.write(
        "A12",
        "Scope 1 (%)",
        header
    )

    ws.write_formula(
        "B12",
        '=IF(B9=0,0,B5/B9)',
        percent
    )

    ws.write(
        "A13",
        "Scope 2 (%)",
        header
    )

    ws.write_formula(
        "B13",
        '=IF(B9=0,0,B6/B9)',
        percent
    )

    ws.write(
        "A14",
        "Scope 3 (%)",
        header
    )

    ws.write_formula(
        "B14",
        '=IF(B9=0,0,B7/B9)',
        percent
    )

    # -------------------------
    # Explication
    # -------------------------

    ws.merge_range(
        "A16:C18",
        "Les feuilles « Scope 1 », « Scope 2 » et « Scope 3 » "
        "présentent le détail des émissions utilisé pour le bilan. "
        "Les cellules jaunes peuvent être modifiées. "
        "Les totaux de chaque scope et la synthèse sont recalculés automatiquement.",
        note
    )

    ws.freeze_panes(4, 0)

    # =========================================================
    # ORDRE DES FEUILLES
    # =========================================================

    # xlsxwriter crée les feuilles dans l'ordre de création.
    # Nous voulons Synthèse en premier.
    # On ne peut pas simplement déplacer une worksheet après création,
    # donc on recrée ici un ordre logique via worksheet.set_first_sheet().
    ws.activate()
    ws.set_first_sheet()

    # =========================================================
    # FIN
    # =========================================================

    workbook.close()

    output.seek(0)

    return output


# =============================================================
# EXPORT INDIVIDU
# =============================================================

def build_individu_excel(
    scope1: Dict[str, Any],
    scope2: Dict[str, Any],
    scope3: Dict[str, Any]
) -> BytesIO:

    return _build_workbook(
        "Individu",
        scope1,
        scope2,
        scope3
    )


# =============================================================
# EXPORT BÂTIMENT
# =============================================================

def build_batiment_excel(
    scope1: Dict[str, Any],
    scope2: Dict[str, Any],
    scope3: Dict[str, Any]
) -> BytesIO:

    return _build_workbook(
        "Bâtiment",
        scope1,
        scope2,
        scope3
    )


# =============================================================
# EXPORT ENTREPRISE
# =============================================================

def build_entreprise_excel(
    scope1: Dict[str, Any],
    scope2: Dict[str, Any],
    scope3: Dict[str, Any]
) -> BytesIO:

    return _build_workbook(
        "Entreprise",
        scope1,
        scope2,
        scope3
    ) 