#!/bin/bash
# deploy.sh — Attivare quando arriva il dominio
# Usage: ./deploy.sh yourdomain.com

set -e

DOMAIN=$1
if [ -z "$DOMAIN" ]; then
  echo "Usage: ./deploy.sh yourdomain.com"
  exit 1
fi

echo "→ Configurando dominio: $DOMAIN"

# 1. Aggiorna nginx config con dominio reale
sed -i "s/_DOMAIN_/$DOMAIN/g" /etc/nginx/sites-available/piva-api

# 2. Attiva sito
ln -sf /etc/nginx/sites-available/piva-api /etc/nginx/sites-enabled/piva-api
rm -f /etc/nginx/sites-enabled/default

# 3. Test config
/usr/sbin/nginx -t

# 4. Reload nginx
systemctl reload nginx

# 5. SSL con certbot
apt-get install -y certbot python3-certbot-nginx
certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos --email admin@$DOMAIN

# 6. Avvia API con pm2
cd /root/projects/piva-api
pm2 start "/root/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8001" --name piva-api
pm2 save
pm2 startup

echo "✅ Deploy completato! API live su https://$DOMAIN"
