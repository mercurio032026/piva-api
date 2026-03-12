"""
Database allergeni EU — 14 allergeni obbligatori (Reg. UE 1169/2011)
Mappatura ingredienti italiani comuni → allergeni
"""

# I 14 allergeni obbligatori EU
ALLERGENI_EU = {
    1: {"id": 1, "nome": "Glutine", "en": "Gluten", "icona": "🌾", "descrizione": "Cereali contenenti glutine: grano, segale, orzo, avena, farro, kamut"},
    2: {"id": 2, "nome": "Crostacei", "en": "Crustaceans", "icona": "🦐", "descrizione": "Crostacei e prodotti a base di crostacei"},
    3: {"id": 3, "nome": "Uova", "en": "Eggs", "icona": "🥚", "descrizione": "Uova e prodotti a base di uova"},
    4: {"id": 4, "nome": "Pesce", "en": "Fish", "icona": "🐟", "descrizione": "Pesce e prodotti a base di pesce"},
    5: {"id": 5, "nome": "Arachidi", "en": "Peanuts", "icona": "🥜", "descrizione": "Arachidi e prodotti a base di arachidi"},
    6: {"id": 6, "nome": "Soia", "en": "Soy", "icona": "🫘", "descrizione": "Soia e prodotti a base di soia"},
    7: {"id": 7, "nome": "Latte", "en": "Milk", "icona": "🥛", "descrizione": "Latte e prodotti a base di latte (incluso lattosio)"},
    8: {"id": 8, "nome": "Frutta a guscio", "en": "Tree nuts", "icona": "🌰", "descrizione": "Mandorle, nocciole, noci, anacardi, pistacchi, noci di macadamia, noci del Brasile, noci pecan"},
    9: {"id": 9, "nome": "Sedano", "en": "Celery", "icona": "🥬", "descrizione": "Sedano e prodotti a base di sedano"},
    10: {"id": 10, "nome": "Senape", "en": "Mustard", "icona": "🟡", "descrizione": "Senape e prodotti a base di senape"},
    11: {"id": 11, "nome": "Semi di sesamo", "en": "Sesame", "icona": "⚪", "descrizione": "Semi di sesamo e prodotti a base di semi di sesamo"},
    12: {"id": 12, "nome": "Anidride solforosa e solfiti", "en": "Sulphites", "icona": "🍷", "descrizione": "Anidride solforosa e solfiti in concentrazioni > 10 mg/kg o 10 mg/litro"},
    13: {"id": 13, "nome": "Lupini", "en": "Lupin", "icona": "🌸", "descrizione": "Lupini e prodotti a base di lupini"},
    14: {"id": 14, "nome": "Molluschi", "en": "Molluscs", "icona": "🦪", "descrizione": "Molluschi e prodotti a base di molluschi"},
}

# Database ingredienti → allergeni (Italian common ingredients)
# Ogni ingrediente mappa a una lista di ID allergeni
INGREDIENTI_DB = {
    # Cereali e derivati (Glutine)
    "farina": [1], "farina 00": [1], "farina 0": [1], "farina integrale": [1],
    "farina di grano": [1], "farina di frumento": [1], "farina di farro": [1],
    "pane": [1, 7], "pane grattugiato": [1, 7], "pangrattato": [1, 7],
    "pasta": [1], "pasta di semola": [1], "pasta fresca": [1, 3],
    "pasta all'uovo": [1, 3], "spaghetti": [1], "penne": [1], "rigatoni": [1],
    "fusilli": [1], "tagliatelle": [1, 3], "lasagne": [1, 3],
    "gnocchi": [1], "semola": [1], "semolino": [1],
    "orzo": [1], "farro": [1], "avena": [1], "segale": [1], "kamut": [1],
    "cous cous": [1], "couscous": [1], "bulgur": [1],
    "pizza": [1, 7], "focaccia": [1, 7], "grissini": [1, 7],
    "crackers": [1, 7], "biscotti": [1, 3, 7], "brioche": [1, 3, 7],
    "cornetto": [1, 3, 7], "croissant": [1, 3, 7],
    
    # Riso e cereali senza glutine
    "riso": [], "riso arborio": [], "riso carnaroli": [], "riso basmati": [],
    "polenta": [], "farina di mais": [], "mais": [], "miglio": [],
    "quinoa": [], "amaranto": [], "grano saraceno": [],
    
    # Uova
    "uovo": [3], "uova": [3], "tuorlo": [3], "albume": [3],
    "uovo sodo": [3], "frittata": [3], "maionese": [3, 10],
    
    # Latte e derivati
    "latte": [7], "latte intero": [7], "latte scremato": [7], "latte parzialmente scremato": [7],
    "panna": [7], "panna fresca": [7], "panna montata": [7], "panna da cucina": [7],
    "burro": [7], "ricotta": [7], "mascarpone": [7], "mozzarella": [7],
    "parmigiano": [7], "parmigiano reggiano": [7], "grana padano": [7],
    "pecorino": [7], "gorgonzola": [7], "fontina": [7], "taleggio": [7],
    "provolone": [7], "scamorza": [7], "stracchino": [7], "crescenza": [7],
    "formaggio": [7], "yogurt": [7], "besciamella": [1, 7],
    "burrata": [7], "fiordilatte": [7], "caciocavallo": [7],
    "latte condensato": [7], "latte in polvere": [7],
    
    # Pesce
    "pesce": [4], "merluzzo": [4], "baccalà": [4], "tonno": [4],
    "salmone": [4], "branzino": [4], "spigola": [4], "orata": [4],
    "sogliola": [4], "trota": [4], "pesce spada": [4], "sardine": [4],
    "acciughe": [4], "alici": [4], "sgombro": [4], "nasello": [4],
    "rombo": [4], "dentice": [4], "cernia": [4], "anguilla": [4],
    "colatura di alici": [4], "bottarga": [4], "surimi": [4, 1, 3],
    
    # Crostacei
    "gamberi": [2], "gamberoni": [2], "gamberetti": [2], "scampi": [2],
    "aragosta": [2], "astice": [2], "granchio": [2], "mazzancolle": [2],
    
    # Molluschi
    "cozze": [14], "vongole": [14], "calamari": [14], "polpo": [14],
    "seppie": [14], "totani": [14], "moscardini": [14], "ostriche": [14],
    "capesante": [14], "cannolicchi": [14], "telline": [14], "lumache": [14],
    
    # Frutta a guscio
    "mandorle": [8], "nocciole": [8], "noci": [8], "pistacchi": [8],
    "anacardi": [8], "pinoli": [8], "noci pecan": [8], "noci di macadamia": [8],
    "noci del brasile": [8], "pesto": [8, 7], "pesto alla genovese": [8, 7],
    "nutella": [7, 8, 6], "praline": [7, 8],
    
    # Arachidi
    "arachidi": [5], "burro di arachidi": [5], "olio di arachidi": [5],
    
    # Soia
    "soia": [6], "salsa di soia": [6], "tofu": [6], "edamame": [6],
    "latte di soia": [6], "lecitina di soia": [6], "tempeh": [6],
    "olio di soia": [6], "miso": [6],
    
    # Sedano
    "sedano": [9], "sedano rapa": [9], "sale di sedano": [9],
    
    # Senape
    "senape": [10], "mostarda": [10], "salsa senape": [10],
    
    # Sesamo
    "sesamo": [11], "semi di sesamo": [11], "tahini": [11], "gomasio": [11],
    
    # Solfiti
    "vino": [12], "vino bianco": [12], "vino rosso": [12], "aceto": [12],
    "aceto balsamico": [12], "aceto di vino": [12], "frutta secca": [12],
    "marsala": [12], "prosecco": [12], "spumante": [12],
    
    # Lupini
    "lupini": [13], "farina di lupini": [13],
    
    # Salumi e insaccati
    "prosciutto crudo": [], "prosciutto cotto": [7], "salame": [],
    "mortadella": [7, 8], "pancetta": [], "guanciale": [],
    "speck": [], "bresaola": [], "coppa": [], "lardo": [],
    "salsiccia": [12], "wurstel": [1, 7, 12],
    "nduja": [],
    
    # Condimenti e salse
    "olio d'oliva": [], "olio extravergine": [], "olio evo": [],
    "sale": [], "pepe": [], "aglio": [], "cipolla": [],
    "pomodoro": [], "passata di pomodoro": [], "pelati": [],
    "concentrato di pomodoro": [], "sugo": [],
    "ragù": [9, 7], "carbonara": [3, 7],
    "amatriciana": [1], "cacio e pepe": [1, 7],
    "salsa rosa": [3, 10], "ketchup": [], "worcestershire": [4],
    "dado": [9], "brodo": [9],
    
    # Verdure (senza allergeni comuni)
    "pomodori": [], "zucchine": [], "melanzane": [], "peperoni": [],
    "carote": [], "patate": [], "spinaci": [], "basilico": [],
    "prezzemolo": [], "rosmarino": [], "salvia": [], "origano": [],
    "funghi": [], "carciofi": [], "asparagi": [], "broccoli": [],
    "cavolfiore": [], "cavolo": [], "insalata": [], "rucola": [],
    "radicchio": [], "finocchio": [], "piselli": [], "fagioli": [],
    "lenticchie": [], "ceci": [],
    
    # Frutta
    "limone": [], "arancia": [], "mela": [], "pera": [], "banana": [],
    "fragole": [], "lamponi": [], "mirtilli": [], "pesca": [],
    "albicocca": [], "ciliegia": [], "uva": [], "fico": [], "kiwi": [],
    
    # Dolci comuni
    "tiramisù": [1, 3, 7], "pannacotta": [7], "panna cotta": [7],
    "gelato": [3, 7], "sorbetto": [], "crema pasticcera": [1, 3, 7],
    "cioccolato": [7], "cioccolato fondente": [], "cacao": [],
    "zucchero": [], "miele": [],
    "cannoli": [1, 3, 7], "sfogliatella": [1, 3, 7],
    "millefoglie": [1, 3, 7], "profiteroles": [1, 3, 7],
    "babà": [1, 3, 7], "pastiera": [1, 3, 7],
    "amaretti": [3, 8], "cantucci": [1, 3, 8],
}

def find_allergeni(ingredienti: list[str]) -> dict:
    """Dato un elenco di ingredienti, restituisce gli allergeni presenti."""
    found_allergeni = set()
    ingredient_map = {}  # allergene_id -> [ingredienti che lo causano]
    unknown = []
    
    for ing in ingredienti:
        ing_lower = ing.lower().strip()
        if ing_lower in INGREDIENTI_DB:
            allergen_ids = INGREDIENTI_DB[ing_lower]
            for aid in allergen_ids:
                found_allergeni.add(aid)
                if aid not in ingredient_map:
                    ingredient_map[aid] = []
                ingredient_map[aid].append(ing)
        else:
            # Try partial match
            matched = False
            for key, aids in INGREDIENTI_DB.items():
                if ing_lower in key or key in ing_lower:
                    for aid in aids:
                        found_allergeni.add(aid)
                        if aid not in ingredient_map:
                            ingredient_map[aid] = []
                        ingredient_map[aid].append(ing)
                    matched = True
                    break
            if not matched:
                unknown.append(ing)
    
    allergeni_list = []
    for aid in sorted(found_allergeni):
        info = ALLERGENI_EU[aid].copy()
        info["causato_da"] = ingredient_map.get(aid, [])
        allergeni_list.append(info)
    
    return {
        "allergeni_trovati": len(allergeni_list),
        "allergeni": allergeni_list,
        "ingredienti_non_riconosciuti": unknown,
        "nota": "Verifica sempre con il produttore. Questo strumento è un supporto, non sostituisce l'analisi professionale."
    }
