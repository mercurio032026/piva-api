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

