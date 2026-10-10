#!/bin/bash
# ==============================================================================
# LAB MODUL 8: AUTOMATED DEPLOYMENT & HEALTH CHECK SCRIPT
# ==============================================================================
set -eo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$PROJECT_DIR/deployment.log"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

log_message() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

echo "======================================================"
echo "    MEMULAI SIKLUS OTOMASI DEPLOYMENT APLIKASI WEB    "
echo "======================================================"

# 1. Validasi Keberadaan Direktori dan File Kunci
cd "$PROJECT_DIR"
if [ ! -f "index.html" ]; then
    log_message "[FATAL] File index.html tidak ditemukan pada $PROJECT_DIR. Deployment dibatalkan!"
    exit 1
fi
log_message "[INFO] Integritas file proyek valid."

# 2. Verifikasi Hak Akses File Web
chmod 644 "$PROJECT_DIR"/index.html
log_message "[INFO] Penyesuaian file permission selesai."

# 3. Uji Sintaks Konfigurasi Nginx
echo "[INFO] Menjalankan uji sintaks Nginx (nginx -t)..."
if ! sudo nginx -t > /dev/null 2>&1; then
    log_message "[FATAL] Sintaks Nginx tidak valid! Silakan periksa file konfigurasi."
    exit 1
fi
log_message "[INFO] Konfigurasi Nginx terverifikasi valid."

# 4. Zero-Downtime Reload Service Web Server
echo "[INFO] Menerapkan konfigurasi baru ke Nginx..."
if sudo systemctl reload nginx 2>/dev/null || sudo service nginx reload; then
    log_message "[INFO] Service Nginx berhasil dimuat ulang (reload)."
else
    log_message "[FATAL] Gagal me-reload Nginx!"
    exit 1
fi

# 5. Automated Health Check Menggunakan cURL
echo "[INFO] Melakukan HTTP Health Check ke endpoint lokal..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/ || echo "000")

if [ "$HTTP_CODE" -eq 200 ]; then
    COMMIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo "non-git")
    log_message "[SUCCESS] Deployment Berhasil! Status HTTP: $HTTP_CODE | Git Commit: $COMMIT_HASH"
    echo "======================================================"
    echo " APLIKASI BERHASIL DIRELOAD & BERJALAN DI http://localhost "
    echo "======================================================"
else
    log_message "[ERROR] Health check gagal! Mendapatkan HTTP Code: $HTTP_CODE (Ekspektasi: 200)"
    echo "======================================================"
    echo " [PERINGATAN] Endpoint tidak mengembalikan status 200 OK!"
    echo "======================================================"
    exit 1
fi
