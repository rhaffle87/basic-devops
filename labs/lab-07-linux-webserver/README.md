# Lab 07: Dasar Linux dan Web Server Nginx

Direktori ini menyediakan berkas template dan starter kit untuk praktikum **Modul 7: Dasar Linux Server dan Dasar Web Server**.

## Isi Direktori
- `index.html`: Contoh halaman web portofolio statis yang siap digunakan untuk pengujian document root Nginx.
- `nginx-default.conf`: Berkas konfigurasi template Virtual Host (*Server Block*) untuk `/etc/nginx/sites-available/default`.

## Petunjuk Penggunaan Cepat

1. Salin berkas `index.html` ke direktori web root di Ubuntu WSL:
   ```bash
   sudo mkdir -p /var/www/html/Portfolio-responsive
   sudo cp index.html /var/www/html/Portfolio-responsive/
   ```

2. Terapkan konfigurasi Nginx:
   ```bash
   sudo cp nginx-default.conf /etc/nginx/sites-available/default
   sudo nginx -t
   sudo systemctl restart nginx
   ```

3. Buka browser di Windows dan akses `http://localhost`.
