# RapidAPI Listing — P.IVA & Codice Fiscale API

## Nome API
Italian VAT & Tax Code Validator (P.IVA & Codice Fiscale)

## Categoria
Data → Validation

## Short Description (160 chars)
Validate Italian VAT numbers (Partita IVA) and Tax Codes (Codice Fiscale) instantly. Checksum verified. No registration. EU-hosted server.

## Long Description
REST API to validate Italian fiscal identifiers:

- **Partita IVA** (VAT number): 11-digit checksum validation per Italian Ministry of Finance algorithm
- **Codice Fiscale** (Tax code / SSN): full alphanumeric validation with character control check

**Why use this API?**
- Lightning fast: pure algorithmic validation, no external calls
- Always available: no rate limits on free tier for testing
- EU data residency: server hosted in Europe, no data logged
- Simple integration: plain JSON, no auth headers required on free tier

**Use cases:**
- E-commerce checkout form validation
- Invoicing software (FatturaPA)
- CRM / customer onboarding
- B2B SaaS for Italian market

## Endpoints

### GET /v1/piva/{partita_iva}
Validate a Partita IVA (Italian VAT number).
- `partita_iva` (path): 11-digit number, optionally prefixed with "IT"
- Returns: `{ valid, partita_iva, formatted }`
- On error: HTTP 422 with detail

### GET /v1/cf/{codice_fiscale}
Validate a Codice Fiscale (Italian Tax Code).
- `codice_fiscale` (path): 16-char alphanumeric code
- Returns: `{ valid, codice_fiscale }`
- On error: HTTP 422 with detail

### GET /v1/validate?piva=&cf=
Validate both in a single call.
- Query params: `piva` and/or `cf`
- Returns combined result object

## Pricing Tiers (RapidAPI)

### BASIC — Free
- 1,000 requests/month
- All endpoints
- No credit card required

### PRO — $9.99/month
- 50,000 requests/month
- Priority support

### ULTRA — $29.99/month
- 500,000 requests/month
- SLA 99.9%

## Tags
italy, italian, vat, tax-code, partita-iva, codice-fiscale, validation, fiscal, EU

## Example Request (curl)
```bash
curl "https://[API_HOST]/v1/piva/12345670017" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: [API_HOST]"
```

## Example Response
```json
{
  "valid": true,
  "partita_iva": "12345670017",
  "formatted": "IT12345670017"
}
```
