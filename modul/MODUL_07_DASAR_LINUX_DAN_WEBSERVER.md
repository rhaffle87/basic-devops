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

![Arsitektur Web Server Nginx](../assets/modul-07/00_arsitektur_webserver_nginx.png)
*Gambar 1. Arsitektur Komponen Web Server Nginx dan Alur Komunikasi HTTP antara Host Windows dan WSL2 Ubuntu*

> **Diagram Arsitektur Draw.io**: Berkas diagram vektor dapat disunting langsung di [`assets/modul-07/00_arsitektur_webserver_nginx.drawio`](../assets/modul-07/00_arsitektur_webserver_nginx.drawio) atau dibuka via [Draw.io Online Viewer/Editor](https://viewer.diagrams.net/?tags=%7B%7D&lightbox=1&edit=_blank#R5Vxbc9o8Gv4te8EMuYDxGbgkJLSdpmmmpNtvrzLClkHFtvhkOST761cnGx9kQoCEfN1OJ9iyrePznp5XdseedOzpUxx1LOMRkhThpGNfdSzL7BvsLyuFiY8DlCxk8c%2F7aW%2FIL9jTjn3dMcYdexI%2FhSiC7NYlTqm8LSBgg7CsoFKt5fUNWbN82jL4f3sSILAgIGYnCYihvHfMnqNwRTPSu12g5Kn3DQdZ1BvIalEg70rEJUD8ZS%2FeXi%2FXnrcRP30iYL1ktUA%2B3OBJjdQy1FCDZ1kyzAsWJG%2FF3BbM0H9VB838tgwFMK3cSDGOKFpXC32cJNCnlTJACN5UbwtxVG11DRawUTDzQdQs%2FYUCuqyPi1%2F4DNFiqZoe5BdikN%2BsCtIlCPCmVNScx3w2Cca09fJ2yicwikqrpdrpWNPXP1sMk8CEtlS3s8Z%2F9Xrs4B5RgdZLwFaDsANW%2Buq%2BUF7Jw1xVIWAOokytR8fyItbByzmfUfqslsn7O%2BMzdhnihPZSASLepDlcMyBebq%2BzowX%2F3cKf3fUL8spmkDyKLgt5EL3zQLxmN8u%2F%2FBa0irKUHdzBBCQLwP6wk8%2F393fs5wf8O4NMRi2jK2SJHQwu8t6ySZznbRcjIPUS3nsB5QiTyrA6lu05A2c4b47kS0Ihk%2B4U8Z5g0f4vlAQc92z8fPVMszyYecbmWozmhimeVcaHwU7%2BjQjNQIRSWdOv2Q2f95%2FzLKEZO7CsvuHwZ%2B5n%2BsquHxluelcEsd%2FSHF5zDQJLsyCHmA%2FbqiyiRXCWBJCjwGSXN0u2RLM18PnVDdMurGxJmTaVl5lejCbFTNnhMAShz8pTSvAKlq7488CFZnEll2Jewga84MrTZ51na593ieGAwqdWwTB3CW9DLUIcQ0qe2bmq0VGCpRRiLmebknYxhqpwWdIsrqu0mtJoi6LmfaWe3aOEbW%2BBnny%2FvR9%2Fub3%2BwdEkhaqBsu4kQlAg9xvwl2y9Lw4UfP9hk1dak%2FodyN62%2Fn120YBUukFxBBgE%2BfIDQpWBsT1WUIUbs3Lq4lCDLiP0wlCHLsMYDINBA12WEueZ6oqZn8smTFudV2pywQhWQX4GPI7cBh5tUwtH4wx43CLgBi%2FwgThDzFngUNMYlzp8lmDND1Es3ITy0vBFQcxPGCsdQvG6VHoD5jC6w8zKSPdsjinFMbtB1DRO19JXMTjw8pMQPXE0XqrGrpaUcidnzKfSmvpB0v%2BdMvcKPZJ%2BAhngp4sl%2BxPARz6edHvIjvISJU%2FD0mEPE8SUMoj66eNiX4hVJPNwqFleFWtNqFleE2l52fsqvlyrXHIfUjgGExyvcSJLD1Nv87yul3DXppq819tF8U%2BnuUa274aBVnO9KyaqkPCa5pD51E1QON451M8WDJ8hCMQBW51D8bAkrMvM0T0CEM7rAWGGbjja6SjtufwlNB%2B%2B%2FGZ1%2BU3N8rua5R%2BcxRkSC8YOvggte7jt8VVFR5if97UjeYfVwWE2pAL3kyFm2ASMo7Ehzlm1xT2Yl6LjQ3CjhO2B8praY2IZWX3CeCFayhGri0KNvDhdixCwGU2rQHS8DT91sbQmGrzDhOIQR5ymkuF10QHZWEsAyOBDa8qr5DOXI7YIhlTjhMUoCHhl74vImgftNRFpGB%2FErRkHAYFpWtitnz9ujgRkRqJWQO4iNEwP2A7QwGlqdEbTzsjpjMSMMeVV6K5WIqGG%2FwgzTEjGdDw09PCfMycFPvUF1k5KRLQ6XIV9fQHUTER8lCxuxNmVaWhCxdAcWODMitfWaF5bh%2FPhOeJEwendcQPIyS24EQwdW1TC6fbDEL%2BB84dHUVUL3AP0qNWjXK311CLzFkt0E1uoQGYABF9ptPCVL7UwB%2F5qIVAr1bUJbTCUADFKWrzAZqVh01KtGnNM2Az1CAhQxj0GL78geNWNWtTxXJDoRbniW4tq6p1na8HZ1rpduCNgRdFKmIMWQrTVMlXaNfS9TDCJQdSYgyLsaXb0CkXgGSScAMURXJZ4zBuUZE%2BtVqwoFsuz34rFgLC6e4I1GJtuPoTSqhTDqi9uQXUWK8ZvX%2FN%2BpmxuA4FgG1pwGBr7rGs%2Bj2ZeWsGrUkrVSbRtx3TdnVAtVG1Z7GYU0Ez6onsS43XXQrHtwqIa37%2Fu%2Bcw3ZuUm3B%2BazeTBOE0h5WYwwoBr%2Bn2qmQJBQjbzArc46c2ZzVmJQe5CQ730XQjwAgkNulvPYZ01%2FNsz%2Fitog%2FOQQreQbjBZcUSzZedBlMETMSTki3WYdUlwAB981cBLDv5Xft9WGrrfZ0VXXplzeqWKLekAZ%2BC63kiv8VGSss7wkGdyJ8VenHU5j3%2FR7MwNxuu5vAUEYC3AKeyhNeAp7b65bwBxjABBI7RCqOX4raHjNzl%2Bs%2B%2FqhKru3b2rOLlVF83RMKyORpxG584tWXLB63nH6%2BQREZzEx5Cum7QZoGzTCLNsnj6nFMbCGpKtrTe6vDMXZYUfByBdSjloyYzmSeQ3ykKF4QAGWhUP3KHhnyILNWJRmWmdIwv1YhpqYH2YNFSx%2FMdmoTJV0Z%2BeiMrHqQ566wig5JUZKCnHh0PMc9wPkX16CVy5AroXf49FWCRr%2B9MBpoYpfw%2FNcR6NsMHwJYQ5H4QInP287FUMcF9t78hDXm7K0MHerP%2BQyHpquLvhAbbwOFt2XXWlNfZpJPApwkXLEJXtv7vD2mFXPe3ujiB0dHZVkZR6z2%2BXZbWaltX0PNd2DrCsJwCmVdN8TWB6uiTredJsBelypObTI%2FCP03xqmPL3QM1XTNURuq%2BGMefj5uVygH0DKRXK545gX2ZFblkUfkwAH6sqD961atotLGp7p08f7puacN9kEYat501%2FpnnA3iAqxE7mlvTjYCJGgR5RBBecgzOuAIxFZl1d%2B3IlSADHeIF6fSdaQ8MJfoPxHPhASwvGMGYQQIHcUrvCSYgWmdqqm%2FcTlRJSkPolceaUedoDjwBFYM6TuUz0Q5BF5elEr6JOv8FkASMc8d7OWQAs%2BGLFXkmeZo0JP%2BEpMyMQExjzZ5KADWMlJzTfAr1EQbbm8o3JisPx7fmZwA99ONBZaabBXBe%2BwM%2Fok2vu4YTNCXRmXWVqzLIu5h0aZ1Sav9SCn1Bp5hh6O6Wp6XS3tmVdblW%2F%2BNjqdLPZ9AJAwU6VWk1HGOP0OeEp4AQLwa2pVvMDq9YEEuYnSd0JV%2FIVB0l4B4Agob6k9irrrRT6gPCHEk1W5iX9KN7q4DUTNM%2FEMEnxWkeKYqZ9RWEA1WsTMWRqEaViUxhcYw7tKRS4ijDzFfdrNbcgc0hWIFVhD0pLw6SYyEz2VikjNjWie%2BlauIHGil8vSOS3V8fzeTgIDG3QlEO7SUb%2Bg5Sx6e6pjc%2FCnTfDd8WgT5kzVRDaswI4h8XwBfDqUbxiqCqN6WhyGeRfYT9TFP4P4Q8aXTbkR74fZco0Gvsrd%2BFM3y7Cb02OFhvbThDhF1nx80f4tmvsF%2BKbZwnxeUbePUGIv9299SdH%2BLy%2Fbv57YIRfEuX%2Fixh%2Fq%2FquEGErg8U4ZpRkPs0IlPoqV2HHOK9tOvIE3usUR0HutT7DVe4T6jQn31klNlb1lEfAvNrqhsk39WZ3eHZT%2Bf76902ymySwxy9yBZ8B3yEwXqUwbalpwI220SWbJ9Lj%2F3e683t7vFQG4JqJUcgfi30rrgr7yzu7du%2B0ats7RZtdCOr7Y%2B3O0NFNQXlbq3Yuu1d4xc0xO8woiEF5jkrNtDU8vO6Mh7qGfR5WTcUc9f02XsrocnvKfL69W722OqNxZ2zqmvwtWvQJWtP%2B79YWxc4cvtcw3N0oLyS6Qrn8b7Fnq%2F3lLAfY8%2BF7UxonMRIHkhqmcaY9KLfXk%2Fsv329nhUm4vvp0PSubhD3qMfvaLwEUbwyJquokyqHvScNgAR9YYHqMzbF0nETgwGCo1Uzl8X26vpcL8pKqOT2DYELHAKG2h3clDkCymd2vBW0g9std7BsW8%2FnN3X5W65I5qczfut6W1kKP7T18I5sq%2FA0pfVYyCDKKq4qgyWG6ng2bcYitEeZ6VAKfEP2rdPwf7pL2bXV29aQ8VHHynJ8kTLL%2BKp%2FIp5z8dPuYOMufU9%2BtCRofTaltBOLcTEZ82LK3kYVyC0i1FOABiofACFDu8FQ%2B%2FvKeasTqlzMzs2zNk%2BepcCwL6vFgSU%2Fz6lrl%2FQiBaqchxZi%2B3E3Eh08WCd9Kz%2FvOjNsmKY2LX5%2FKvbDNFMgdEFxrvkn244pfS6KfB%2FmczSjaKsuiUZNFqySLhjDUuTSae8qifKiQxuNlsbINoyGR5WTlnyaRdr8sez8gCNKjCTEhjQFKV8z4guAY66uLoeaOaxv6GEoM5odoU7xCgfxS5NpNYRKor4Slz6kPoqgl7PkAchaMBgPDa9%2Bo2iJaZkW07INkyz69cBVbixuiVU5pNUTrODf7%2FLLl9CuiRCDNiMhBXInUFNP6z%2Fy1mhNIGX0Dk2c4g6E70MqZGNhXSBLxEbsZZWIeq2ksBscCbCDWQb5VtB3sxzVuhjvyvNHrjdtW4ryyxBn7SpxXkTjzbSWuwsP9adbMrYSXguDjktdt5LdVnCnjziPjy3R98gCz3dssj3D7cp%2FRFZ8EkDTnu73ZVOzUbHbzEgfPFQ2nf7n1H%2BfovibONCpx5sDdTx2Y1UBz4L5dpLnT%2BG7D0H%2BIJhC3tXwRVFVR%2BvZq9dOv4n1T%2BfXX%2FIuy4gHhLoqS%2FwE%3D).

```mermaid
sequenceDiagram
    autonumber
    actor Client as Web Browser (Host Windows)
    participant NginxMaster as Nginx Master Process
    participant NginxWorker as Nginx Worker Process
    participant Storage as Filesystem (/var/www/html)

    Client->>NginxWorker: HTTP GET /index.html (Port 80)
    Note over NginxMaster,NginxWorker: Event-driven & Asynchronous
    NginxWorker->>Storage: Baca berkas index.html
    Storage-->>NginxWorker: Berkas biner/teks
    NginxWorker-->>Client: HTTP 200 OK (Payload HTML)
```
*Siklus Penanganan Permintaan HTTP pada Nginx (Sequence Diagram)*

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
