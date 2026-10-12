# Modul 7
## Dasar Linux dan Dasar Web Server

---

### 1. Tujuan Pembelajaran
- Memahami konsep dasar sistem operasi Linux Server dan arsitektur hierarki direktori Ubuntu.
- Memahami konsep dasar web server serta cara kerja Nginx dalam melayani request HTTP.
- Memasang dan mengonfigurasi Windows Subsystem for Linux (WSL) sebagai lingkungan server lokal.
- Menginstalasi, mengoperasikan, dan memverifikasi layanan web server Nginx pada Linux.
- Menggunakan Git dasar untuk mengunduh kode sumber website statis.
- Mengonfigurasi Virtual Host (*server block*) Nginx dan menguji akses website melalui browser host Windows (`localhost`).

---

### 2. Dasar Teori

#### 2.1 Linux Server
Linux Server adalah sistem komputer yang menggunakan sistem operasi berbasis kernel Linux untuk menyediakan berbagai layanan jaringan (*network services*), seperti web server, database server, file sharing, dan application hosting. Linux server banyak digunakan di lingkungan industri karena bersifat *open-source*, memiliki stabilitas tinggi, hemat konsumsi sumber daya, serta dilengkapi manajemen perizinan (*permissions*) yang aman.

Dalam administrasi server, pemahaman struktur direktori Linux sangat penting agar administrator mengetahui lokasi file konfigurasi, data aplikasi, serta log sistem.

**Tabel 1. Struktur Direktori Utama Ubuntu Linux**
| Direktori | Deskripsi dan Fungsi |
| :--- | :--- |
| `/` | *Root directory*, direktori tertinggi tempat seluruh file dan hierarki sistem Linux berada |
| `/home` | Menyimpan file dan data pribadi milik masing-masing pengguna (*user*) |
| `/etc` | Menyimpan seluruh file konfigurasi sistem dan layanan (termasuk Nginx) |
| `/var` | Menyimpan data dinamis yang sering berubah, seperti log sistem (`/var/log`) dan file web default (`/var/www/html`) |
| `/var/www/html` | Lokasi default *document root* penyimpanan file website pada web server |
| `/bin` | Berisi file biner program dasar Linux yang esensial untuk seluruh pengguna |
| `/usr` | Menyimpan file aplikasi, pustaka (*libraries*), dan dokumentasi tambahan pengguna |
| `/tmp` | Tempat penyimpanan file sementara yang dibersihkan secara berkala oleh sistem |
| `/boot` | Berisi file kernel Linux dan konfigurasi boot loader |
| `/dev` | Menyimpan representasi file untuk perangkat keras (*device nodes*) |
| `/proc` | Sistem file semu (*virtual filesystem*) berisi status kernel dan informasi proses |

#### 2.2 Web Server dan Nginx
Web server adalah layanan perangkat lunak yang berfungsi menerima permintaan (*request*) berbasis protokol HTTP/HTTPS dari klien (melalui peramban web seperti Chrome, Firefox, Edge), kemudian memproses dan mengirimkan berkas respons (*response*) yang diminta (seperti HTML, CSS, JavaScript, gambar, atau data JSON).

##### Dekomposisi Sistem & Alur Penanganan HTTP Nginx
1. **System Summary:** Arsitektur web server Nginx mengadopsi model *asynchronous event-driven* untuk melayani permintaan berkas statis website secara non-blocking. Batasan sistem mencakup antarmuka peramban Windows host, layer daemon Nginx pada WSL2 Ubuntu, dan subsistem penyimpanan Linux *document root*.
2. **Tier & Domain Breakdown:**
   - **Client & Ingestion Tier:** Peramban web host (*Google Chrome / Edge*) yang menginisiasi TCP Handshake dan transmisi request HTTP/1.1.
   - **Control & Configuration Tier:** Nginx Master Process yang mengelola sinyal Linux (*PID controller*) dan mengevaluasi konfigurasi virtual host (`/etc/nginx/sites-available/default`).
   - **Processing & Event Core Tier:** Nginx Worker Process dengan mekanisme *event loop* (`epoll`) yang menangani koneksi konkurensi tinggi tanpa membebani memori sistem.
   - **Persistence & Storage Tier:** Linux VFS yang menyimpan berkas statis portofolio pada direktori `/var/www/html/Portfolio-responsive`.
3. **Flow Dynamics:** Klien mengirimkan request sinkron `HTTP GET /index.html` via port TCP 80. Socket listener Nginx meneruskannya ke Worker Process yang mencocokkan *server block* virtual host. Worker membaca berkas secara non-blocking dari media penyimpanan, memformat header HTTP (MIME type `text/html`), lalu mengirimkan payload berstatus `HTTP 200 OK` kembali ke peramban klien.

![Siklus Penanganan Permintaan HTTP pada Arsitektur Nginx](../assets/modul-07/00_arsitektur_nginx.png)
*Gambar 1. Siklus Penanganan Permintaan HTTP pada Arsitektur Nginx (Draw.io Production Diagram)*  
> 📐 **Berkas Desain Asli:** Berkas skematik draw.io dapat diakses dan disunting pada [`docs/diagrams/modul_07_nginx_architecture.drawio`](../docs/diagrams/modul_07_nginx_architecture.drawio).

Nginx (*Engine-X*) merupakan salah satu web server paling populer di dunia industri karena mengadopsi arsitektur *asynchronous* dan *event-driven*. Berbeda dengan web server tradisional yang membuat satu *thread/process* baru untuk setiap satu koneksi, Nginx menggunakan:
1. **Master Process:** Bertugas membaca konfigurasi, mengelola port socket, dan memonitor worker processes.
2. **Worker Process:** Menangani ribuan koneksi konkuren secara non-blocking dengan konsumsi CPU dan RAM yang sangat efisien.

Selain sebagai web server statis, Nginx juga berperan sebagai *Reverse Proxy*, *Load Balancer*, dan gerbang terminasi SSL/TLS.

#### 2.3 Windows Subsystem for Linux (WSL)
WSL merupakan fitur virtualisasi bawaan Microsoft Windows yang memungkinkan pengembang menjalankan distribusi Linux utuh (seperti Ubuntu) langsung di dalam Windows tanpa overhead berat dari hypervisor tradisional (seperti VirtualBox atau VMware). WSL2 menggunakan kernel Linux asli yang terintegrasi secara transparan dengan jaringan internal Windows, sehingga port layanan (seperti port 80 pada WSL) dapat langsung diakses melalui `localhost` pada Windows.

#### 2.4 Git Version Control
Git adalah sistem *Distributed Version Control* yang melacak setiap riwayat perubahan kode sumber. Pada tahapan dasar administrasi web server, Git digunakan untuk mengkloning (*clone*) kode proyek dari repositori online (seperti GitHub) langsung ke direktori publik server.

#### 2.5 Glosarium Perintah CLI Linux (Sintaks, Akronim, dan Fungsinya)
Tabel berikut merangkum seluruh perintah baris perintah (*Command Line Interface*) Linux yang digunakan pada modul ini, dilengkapi dengan asal-usul singkatan (*akronim*) serta deskripsi fungsinya dalam administrasi server:

**Tabel 2. Glosarium Perintah CLI Linux Modul 7**
| Perintah / Sintaks | Kepanjangan / Asal Kata (Akronim) | Deskripsi dan Fungsi Utama |
| :--- | :--- | :--- |
| `sudo` | **S**uper**u**ser **DO** | Menjalankan perintah dengan hak istimewa administratif tertinggi (*root privileges*). |
| `apt` | **A**dvanced **P**ackage **T**ool | Manajer paket utama pada Ubuntu/Debian untuk mencari, menginstal, memperbarui, dan menghapus software. |
| `apt update` | Advanced Package Tool **Update** | Memperbarui daftar katalog paket terbaru dari repositori online ke database lokal server. |
| `apt upgrade` | Advanced Package Tool **Upgrade** | Mengunduh dan menimpa paket perangkat lunak lama yang terpasang dengan versi terbaru. |
| `apt install` | Advanced Package Tool **Install** | Mengunduh paket aplikasi beserta seluruh pustaka dependensinya dari repositori resmi. |
| `cd` | **C**hange **D**irectory | Berpindah dari satu direktori kerja aktif ke direktori tujuan di dalam sistem file Linux. |
| `ls` | **L**i**S**t | Menampilkan daftar berkas dan folder yang terdapat pada direktori saat ini. |
| `ls -la` | List (**l**ong listing, **a**ll hidden) | Menampilkan detail lengkap berkas (izin akses, kepemilikan, ukuran) termasuk file tersembunyi (*dotfiles*). |
| `ip` | **I**nternet **P**rotocol | Utilitas modern untuk menampilkan konfigurasi antarmuka jaringan, routing, dan alamat IP. |
| `ip -c a` | IP (**c**olor, **a**ddress) | Menampilkan seluruh alamat IP antarmuka jaringan sistem dengan sorotan warna agar mudah dibaca. |
| `systemctl` | **SYSTEM** **C**on**T**ro**L** | Utilitas pengendali sistem inisialisasi `systemd` untuk menyalakan, mematikan, atau memonitor layanan (*service/daemon*). |
| `service` | **Service** (SysV Init Controller) | Perintah legacy pengendali daemon layanan (alternatif `systemctl` bila systemd tidak aktif di WSL). |
| `nano` | **Nano**'s ANOther editor | Editor teks berbasis terminal yang ramah pengguna untuk mengedit file konfigurasi server secara interaktif. |
| `cat` | Con**CAT**enate | Membaca dan menampilkan seluruh isi file teks langsung ke layar terminal tanpa membuka editor. |
| `mkdir` | **M**a**K**e **DIR**ectory | Membuat satu atau beberapa direktori (folder) baru pada sistem file. |
| `chown` | **CH**ange **OWN**er | Mengubah pemilik pengguna (*user*) dan grup pada suatu file atau direktori. |
| `chmod` | **CH**ange **MOD**e | Mengubah bit hak akses / izin (*permissions*) file dan folder (read, write, execute). |
| `tail` | **Tail** (Ujung Belakang) | Menampilkan baris-baris terakhir dari suatu berkas teks. |
| `tail -f` | Tail (**f**ollow) | Memantau penambahan baris baru pada file secara *real-time* (sangat berguna untuk pemantauan file log Nginx). |

---

### 3. Alat dan Kebutuhan Sistem
1. Laptop / Komputer dengan sistem operasi Windows 10 (versi 2004+) atau Windows 11.
2. Akses Terminal Windows / Command Prompt dengan hak Administrator.
3. Sambungan koneksi internet aktif untuk mengunduh paket Ubuntu dan Git repository.
4. Web Browser (Google Chrome, Microsoft Edge, atau Mozilla Firefox).

---

### 4. Langkah-Langkah Praktikum

#### a. Install WSL
1. Buka CMD di laptop masing-masing.
   
   ![Membuka Command Prompt Windows](../assets/modul-07/01_buka_cmd.png)
   *Gambar 2. Tampilan Command Prompt Windows.*

2. Pada CMD jalankan `wsl --install`.
   
   ![Menjalankan Perintah WSL Install](../assets/modul-07/02_wsl_install.png)
   *Gambar 3. Proses instalasi Ubuntu WSL.*

3. Setelah berhasil menginstall wsl-ubuntu, Anda akan diminta untuk membuat user dan password dari Ubuntu.
   
   ![Membuat Username dan Password](../assets/modul-07/03_wsl_buat_user.png)
   *Gambar 4. Pembuatan akun pengguna Ubuntu.*

4. Setelah itu akan masuk langsung ke Ubuntu menandakan Ubuntu berhasil diinstal.
   
   ![Masuk ke Terminal Ubuntu WSL](../assets/modul-07/04_masuk_ubuntu.png)
   *Gambar 5. Tampilan sesi shell terminal Ubuntu.*

#### b. Install Nginx dan Git
1. Buka Ubuntu, dan jalankan `sudo apt update && sudo apt upgrade -y` untuk memperbarui package repository Linux dalam kondisi terbaru.
   
   ![Update dan Upgrade Paket Linux](../assets/modul-07/05_apt_update_upgrade.png)
   *Gambar 6. Proses sinkronisasi repositori dan pembaruan paket.*

2. Selanjutnya jalankan `sudo apt install nginx -y` untuk melakukan install Nginx.
   
   ![Instalasi Nginx Web Server](../assets/modul-07/06_apt_install_nginx.png)
   *Gambar 7. Pemasangan paket Nginx.*

3. Setelah Nginx terinstall, jalankan service Nginx dengan `sudo service nginx start` atau `sudo systemctl start nginx`.
   
   ![Menjalankan Layanan Nginx](../assets/modul-07/07_service_nginx_start.png)
   *Gambar 8. Menjalankan service Nginx.*

4. Setelah Nginx dijalankan, cek status dari Nginx dengan `sudo systemctl status nginx` dan akan muncul indikator `active (running)`.
   
   ![Verifikasi Status Service Nginx Active](../assets/modul-07/08_systemctl_status_nginx.png)
   *Gambar 9. Status operasional layanan Nginx.*

5. Untuk mengecek lebih lanjut apakah Nginx sudah berjalan, kita bisa cek melalui browser dengan IP lokal dari WSL kita. Jalankan `ip -c a` untuk mengecek IP (cek pada antarmuka `eth0`).
   
   ![Pemeriksaan Alamat IP eth0](../assets/modul-07/09_ip_c_a.png)
   *Gambar 10. Menampilkan alamat IP WSL.*

6. Buka peramban web di Windows dan akses `http://localhost` untuk memastikan Nginx telah melayani halaman web.
   
   ![Halaman Welcome to Nginx di Browser](../assets/modul-07/10_browser_welcome_nginx.png)
   *Gambar 11. Halaman selamat datang default Nginx.*

7. Selanjutnya install Git dengan menjalankan `sudo apt install git -y`.
   
   ![Instalasi Paket Git](../assets/modul-07/11_apt_install_git.png)
   *Gambar 12. Pemasangan Git.*

8. Cek apakah Git sudah terinstall dengan menjalankan `git --version`.

#### c. Konfigurasi Webserver
1. Konfigurasi website menggunakan HTML/CSS. Masuk ke direktori web server:
   ```bash
   cd /var/www/html
   ```
2. Unduh template website portofolio dari GitHub:
   ```bash
   sudo git clone https://github.com/faizan-ahmad5/Portfolio-responsive
   ```
   ![Download Website via Git Clone](../assets/modul-07/12_git_clone_portfolio.png)
   *Gambar 13. Mengunduh source code website portofolio.*

3. Setelah berhasil terdownload, cek dengan menjalankan `ls`, folder `Portfolio-responsive` akan tampil.
   
   ![Verifikasi Direktori Hasil Unduhan](../assets/modul-07/13_ls_portfolio.png)
   *Gambar 14. Daftar berkas dalam /var/www/html.*

4. Masuk ke direktori konfigurasi virtual host Nginx:
   ```bash
   cd /etc/nginx/sites-available/
   ```
5. Buka file default untuk konfigurasi Nginx:
   ```bash
   sudo nano default
   ```
   ![Membuka File Default pada Teks Editor Nano](../assets/modul-07/14_nano_default_awal.png)
   *Gambar 15. Tampilan awal file konfigurasi default Nginx.*

6. Cari baris direktif `root /var/www/html;` yang mengatur path default document root web server.
   
   ![Direktif Root Awal](../assets/modul-07/15_root_default_awal.png)
   *Gambar 16. Direktif root bawaan Nginx.*

7. Ubah direktif `root` agar mengarah ke folder proyek `Portfolio-responsive`:
   
   ![Mengubah Root ke Folder Portfolio-responsive](../assets/modul-07/16_root_default_portfolio.png)
   *Gambar 17. Konfigurasi root baru mengarah ke folder portofolio.*

8. Simpan perubahan dengan menekan `Ctrl + O`, tekan `Enter`, lalu keluar dengan `Ctrl + X`.
9. Jalankan `sudo nginx -t` untuk memeriksa sintaks konfigurasi Nginx. Pastikan respon bernilai `syntax is ok` dan `test is successful`.
10. Terapkan konfigurasi baru dengan merestart Nginx:
    ```bash
    sudo systemctl restart nginx
    ```
11. Buka kembali browser di Windows pada `http://localhost`, dan website portofolio kini aktif tampil.

---

### 5. Edge Cases dan Troubleshooting

#### 1. Masalah: Web Browser Menampilkan `403 Forbidden`
* **Penyebab:** Hak akses (*file permissions*) pada folder `/var/www/html/Portfolio-responsive` tidak mengizinkan user Nginx (`www-data`) untuk membaca file `index.html`.
* **Solusi:** Berikan izin baca dan eksekusi direktori:
  ```bash
  sudo chown -R www-data:www-data /var/www/html/Portfolio-responsive
  sudo chmod -R 755 /var/www/html/Portfolio-responsive
  ```

#### 2. Masalah: Layanan Nginx Gagal Dimulai (`Address already in use :80`)
* **Penyebab:** Port 80 di Windows telah digunakan oleh aplikasi lain (seperti Apache XAMPP, Skype, atau IIS Windows).
* **Solusi:** Matikan service IIS di Windows PowerShell Administrator:
  ```powershell
  Stop-Service W3SVC
  ```
  Atau ubah port listen Nginx di `/etc/nginx/sites-available/default` menjadi port `8080`, lalu akses via `http://localhost:8080`.

#### 3. Masalah: Perintah `systemctl` Mengeluarkan Pesan Error Systemd
* **Penyebab:** Versi WSL belum mengaktifkan init systemd.
* **Solusi:** Gunakan perintah alternatif SysV:
  ```bash
  sudo service nginx restart
  sudo service nginx status
  ```

---

### 6. Tugas dan Evaluasi Praktikum
1. Buat sebuah file HTML kustom bernama `info.html` di dalam folder `/var/www/html/Portfolio-responsive/` yang berisi nama, NIM, dan identitas kelompok Anda.
2. Akses halaman tersebut melalui peramban web di `http://localhost/info.html` dan dokumentasikan hasil tangkapan layar (*screenshot*) respon HTTP-nya.
3. Tunjukkan status log akses Nginx secara *real-time* dengan menjalankan perintah `sudo tail -f /var/log/nginx/access.log` saat halaman web diakses dari browser.
