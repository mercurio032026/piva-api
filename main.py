from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
import re
from typing import Optional

app = FastAPI(
    title="P.IVA & Codice Fiscale API",
    description="REST API per validare codici fiscali e partite IVA italiane",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# --- Validazione Codice Fiscale ---
CF_REGEX = re.compile(r'^[A-Z]{6}[0-9LMNPQRSTUV]{2}[ABCDEHLMPRST]{1}[0-9LMNPQRSTUV]{2}[A-Z]{1}[0-9LMNPQRSTUV]{3}[A-Z]{1}$', re.IGNORECASE)

ODD_MAP = {'0':1,'1':0,'2':5,'3':7,'4':9,'5':13,'6':15,'7':17,'8':19,'9':21,
           'A':1,'B':0,'C':5,'D':7,'E':9,'F':13,'G':15,'H':17,'I':19,'J':21,
           'K':2,'L':4,'M':18,'N':20,'O':11,'P':3,'Q':6,'R':8,'S':12,'T':14,
           'U':16,'V':10,'W':22,'X':25,'Y':24,'Z':23}

EVEN_MAP = {str(i): i for i in range(10)}
EVEN_MAP.update({chr(65+i): i for i in range(26)})

def validate_cf(cf: str) -> dict:
    cf = cf.upper().strip()
    if not CF_REGEX.match(cf):
        return {"valid": False, "error": "Formato non valido"}
    
    total = sum(ODD_MAP.get(c, 0) if i % 2 == 0 else EVEN_MAP.get(c, 0) for i, c in enumerate(cf[:15]))
    check = chr(65 + (total % 26))
    
    if cf[15] != check:
        return {"valid": False, "error": "Carattere di controllo errato"}
    
    return {"valid": True, "codice_fiscale": cf}

# --- Validazione Partita IVA ---
def validate_piva(piva: str) -> dict:
    piva = piva.strip().replace(" ", "")
    if piva.upper().startswith("IT"):
        piva = piva[2:]
    
    if not re.match(r'^\d{11}$', piva):
        return {"valid": False, "error": "La P.IVA deve essere di 11 cifre"}
    
    odd_sum = sum(int(piva[i]) for i in range(0, 10, 2))
    even_sum = 0
    for i in range(1, 10, 2):
        d = int(piva[i]) * 2
        even_sum += d if d < 10 else d - 9
    
    total = odd_sum + even_sum
    check = (10 - (total % 10)) % 10
    
    if check != int(piva[10]):
        return {"valid": False, "error": "Cifra di controllo errata"}
    
    return {"valid": True, "partita_iva": piva, "formatted": f"IT{piva}"}

# --- Routes ---

@app.get("/")
def root():
    return {
        "name": "P.IVA & CF API",
        "version": "1.0.0",
        "endpoints": {
            "validate_piva": "/v1/piva/{partita_iva}",
            "validate_cf": "/v1/cf/{codice_fiscale}",
            "health": "/health"
        }
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/v1/piva/{partita_iva}")
def check_piva(partita_iva: str):
    result = validate_piva(partita_iva)
    if not result["valid"]:
        raise HTTPException(status_code=422, detail=result["error"])
    return result

@app.get("/v1/cf/{codice_fiscale}")
def check_cf(codice_fiscale: str):
    result = validate_cf(codice_fiscale)
    if not result["valid"]:
        raise HTTPException(status_code=422, detail=result["error"])
    return result

@app.get("/v1/validate")
def validate_both(piva: Optional[str] = None, cf: Optional[str] = None):
    if not piva and not cf:
        raise HTTPException(status_code=400, detail="Fornire almeno 'piva' o 'cf' come query param")
    
    response = {}
    if piva:
        response["partita_iva"] = validate_piva(piva)
    if cf:
        response["codice_fiscale"] = validate_cf(cf)
    return response



# --- IBAN Validator (Italian) ---

def validate_iban_it(iban: str) -> dict:
    iban = iban.upper().replace(" ", "").replace("-", "")
    
    if not iban.startswith("IT"):
        return {"valid": False, "error": "Solo IBAN italiani (IT) supportati"}
    
    if len(iban) != 27:
        return {"valid": False, "error": f"Lunghezza errata: {len(iban)} invece di 27"}
    
    # Move first 4 chars to end, convert letters to numbers
    rearranged = iban[4:] + iban[:4]
    numeric = ""
    for c in rearranged:
        if c.isdigit():
            numeric += c
        elif c.isalpha():
            numeric += str(ord(c) - ord('A') + 10)
        else:
            return {"valid": False, "error": "Carattere non valido"}
    
    if int(numeric) % 97 != 1:
        return {"valid": False, "error": "Checksum IBAN non valido"}
    
    return {
        "valid": True,
        "iban": iban,
        "country": "IT",
        "check_digits": iban[2:4],
        "cin": iban[4],
        "abi": iban[5:10],
        "cab": iban[10:15],
        "conto": iban[15:27]
    }


@app.get("/v1/iban/{iban}")
def check_iban(iban: str):
    result = validate_iban_it(iban)
    if not result["valid"]:
        raise HTTPException(status_code=422, detail=result["error"])
    return result


# --- Codice Fiscale Generator ---

MONTH_CODES = {'01':'A','02':'B','03':'C','04':'D','05':'E','06':'H',
               '07':'L','08':'M','09':'P','10':'R','11':'S','12':'T'}

OMOCODIA_CHARS = "LMNPQRSTUV"

def generate_cf(cognome: str, nome: str, data_nascita: str, sesso: str, codice_comune: str) -> dict:
    """Genera CF da dati anagrafici. data_nascita: YYYY-MM-DD, sesso: M/F"""
    
    def extract_consonants(s):
        return [c for c in s.upper() if c.isalpha() and c not in 'AEIOU']
    
    def extract_vowels(s):
        return [c for c in s.upper() if c.isalpha() and c in 'AEIOU']
    
    # Cognome: 3 consonanti, poi vocali, poi X
    cons = extract_consonants(cognome)
    vow = extract_vowels(cognome)
    pool = cons + vow + ['X', 'X', 'X']
    cf_cognome = ''.join(pool[:3])
    
    # Nome: se >= 4 consonanti, prendi 1a, 3a, 4a; altrimenti come cognome
    cons = extract_consonants(nome)
    vow = extract_vowels(nome)
    if len(cons) >= 4:
        cf_nome = cons[0] + cons[2] + cons[3]
    else:
        pool = cons + vow + ['X', 'X', 'X']
        cf_nome = ''.join(pool[:3])
    
    # Data
    year = data_nascita[:4]
    month = data_nascita[5:7]
    day = int(data_nascita[8:10])
    
    cf_anno = year[2:4]
    cf_mese = MONTH_CODES.get(month, '?')
    cf_giorno = str(day if sesso.upper() == 'M' else day + 40).zfill(2)
    
    # Comune
    cf_comune = codice_comune.upper()
    
    # Assemble first 15 chars
    partial = cf_cognome + cf_nome + cf_anno + cf_mese + cf_giorno + cf_comune
    
    # Checksum
    total = sum(
        ODD_MAP.get(c, 0) if i % 2 == 0 else EVEN_MAP.get(c, 0) 
        for i, c in enumerate(partial)
    )
    check = chr(65 + (total % 26))
    
    cf = partial + check
    
    return {
        "codice_fiscale": cf,
        "componenti": {
            "cognome": cf_cognome,
            "nome": cf_nome,
            "anno": cf_anno,
            "mese": cf_mese,
            "giorno": cf_giorno,
            "comune": cf_comune,
            "controllo": check
        }
    }


@app.get("/v1/cf/genera")
def genera_cf(cognome: str, nome: str, data_nascita: str, sesso: str, codice_comune: str):
    """Genera un Codice Fiscale dai dati anagrafici.
    
    - cognome: cognome della persona
    - nome: nome della persona  
    - data_nascita: data di nascita (YYYY-MM-DD)
    - sesso: M o F
    - codice_comune: codice catastale del comune (es. H501 per Roma)
    """
    try:
        result = generate_cf(cognome, nome, data_nascita, sesso, codice_comune)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# --- Italian Holidays API ---

def get_italian_holidays(year: int) -> list:
    """Restituisce le festività italiane per un dato anno."""
    import datetime
    
    # Easter calculation (Anonymous Gregorian algorithm)
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    easter = datetime.date(year, month, day)
    pasquetta = easter + datetime.timedelta(days=1)
    
    holidays = [
        {"data": f"{year}-01-01", "nome": "Capodanno", "tipo": "fisso"},
        {"data": f"{year}-01-06", "nome": "Epifania", "tipo": "fisso"},
        {"data": easter.isoformat(), "nome": "Pasqua", "tipo": "mobile"},
        {"data": pasquetta.isoformat(), "nome": "Lunedì dell'Angelo", "tipo": "mobile"},
        {"data": f"{year}-04-25", "nome": "Festa della Liberazione", "tipo": "fisso"},
        {"data": f"{year}-05-01", "nome": "Festa dei Lavoratori", "tipo": "fisso"},
        {"data": f"{year}-06-02", "nome": "Festa della Repubblica", "tipo": "fisso"},
        {"data": f"{year}-08-15", "nome": "Ferragosto", "tipo": "fisso"},
        {"data": f"{year}-11-01", "nome": "Ognissanti", "tipo": "fisso"},
        {"data": f"{year}-12-08", "nome": "Immacolata Concezione", "tipo": "fisso"},
        {"data": f"{year}-12-25", "nome": "Natale", "tipo": "fisso"},
        {"data": f"{year}-12-26", "nome": "Santo Stefano", "tipo": "fisso"},
    ]
    
    return holidays


@app.get("/v1/festivita/{anno}")
def festivita(anno: int):
    """Restituisce tutte le festività italiane per l'anno specificato."""
    if anno < 1946 or anno > 2100:
        raise HTTPException(status_code=400, detail="Anno deve essere tra 1946 e 2100")
    return {"anno": anno, "festivita": get_italian_holidays(anno)}


@app.get("/v1/festivita/{anno}/oggi")
def is_today_holiday(anno: int):
    """Controlla se oggi è una festività italiana."""
    import datetime
    today = datetime.date.today().isoformat()
    holidays = get_italian_holidays(anno)
    match = [h for h in holidays if h["data"] == today]
    return {"data": today, "festivo": len(match) > 0, "festivita": match[0] if match else None}

