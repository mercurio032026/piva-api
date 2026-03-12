# 🇮🇹 P.IVA API

REST API to validate Italian **Partita IVA** (VAT numbers) and **Codice Fiscale** (Tax Codes).

## Features
- ⚡ Lightning fast — pure algorithmic validation, no external calls
- 🔒 Privacy-first — no data logged, no tracking
- 🇪🇺 EU-hosted server
- 📖 OpenAPI docs included

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v1/piva/{partita_iva}` | Validate a Partita IVA |
| GET | `/v1/cf/{codice_fiscale}` | Validate a Codice Fiscale |
| GET | `/v1/validate?piva=&cf=` | Validate both in one call |
| GET | `/docs` | Interactive API documentation |

## Quick Start

```bash
# Validate a P.IVA
curl https://your-domain/v1/piva/12345670017

# Response
{
  "valid": true,
  "partita_iva": "12345670017",
  "formatted": "IT12345670017"
}
```

## Run locally

```bash
pip install fastapi uvicorn
uvicorn main:app --host 0.0.0.0 --port 8001
```

## Available on RapidAPI
Coming soon.

## License
MIT
