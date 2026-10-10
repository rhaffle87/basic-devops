import os
import sys
from PIL import Image, ImageDraw, ImageFont

# Set working directory ke root repositori agar path assets/ selalu konsisten
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO_ROOT)

def render_terminal(output_path, title, lines, width=960, min_height=380):
    font_title = ImageFont.truetype('arial.ttf', 13)
    font_code = ImageFont.truetype('consola.ttf', 14)
    line_height = 22
    calc_height = 55 + len(lines) * line_height + 25
    height = max(min_height, calc_height)
    
    img = Image.new('RGB', (width, height), color='#181818')
    draw = ImageDraw.Draw(img)
    
    # Title bar
    draw.rectangle([(0, 0), (width, 36)], fill='#252526')
    draw.ellipse([(14, 12), (26, 24)], fill='#ff5f56')
    draw.ellipse([(34, 12), (46, 24)], fill='#ffbd2e')
    draw.ellipse([(54, 12), (66, 24)], fill='#27c93f')
    
    # Window Title
    bbox_t = draw.textbbox((0, 0), title, font=font_title)
    t_w = bbox_t[2] - bbox_t[0]
    draw.text(((width - t_w)//2, 10), title, fill='#9da5b4', font=font_title)
    draw.line([(0, 36), (width, 36)], fill='#333333', width=1)
    
    y = 50
    for item in lines:
        if len(item) == 4:
            prompt, p_col, cmd, c_col = item
            draw.text((20, y), prompt, fill=p_col, font=font_code)
            if cmd:
                bbox_p = draw.textbbox((20, y), prompt, font=font_code)
                draw.text((bbox_p[2], y), cmd, fill=c_col, font=font_code)
        elif len(item) == 2:
            text, col = item
            draw.text((20, y), text, fill=col, font=font_code)
        y += line_height
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)
    print(f'Generated: {output_path}')

def render_browser(output_path, url, title, card_title, subtitle, badge_text, badge_color, info_text, bg_col='#0f172a', card_bg='#1e293b', width=960, height=480):
    font_title = ImageFont.truetype('arial.ttf', 13)
    font_url = ImageFont.truetype('arial.ttf', 13)
    font_h1 = ImageFont.truetype('arialbd.ttf', 24)
    font_p = ImageFont.truetype('arial.ttf', 15)
    font_badge = ImageFont.truetype('arialbd.ttf', 13)
    font_info = ImageFont.truetype('consola.ttf', 13)
    
    img = Image.new('RGB', (width, height), color=bg_col)
    draw = ImageDraw.Draw(img)
    
    # Browser chrome header
    draw.rectangle([(0, 0), (width, 70)], fill='#1f232a')
    draw.ellipse([(14, 14), (24, 24)], fill='#ff5f56')
    draw.ellipse([(32, 14), (42, 24)], fill='#ffbd2e')
    draw.ellipse([(50, 14), (60, 24)], fill='#27c93f')
    
    # Tab
    draw.rectangle([(90, 8), (280, 38)], fill='#2c313a')
    draw.text((105, 14), title, fill='#e5e7eb', font=font_title)
    
    # URL bar
    draw.rectangle([(80, 42), (width - 30, 64)], fill='#14171c')
    draw.text((95, 45), url, fill='#9ca3af', font=font_url)
    
    # Card Center
    card_w, card_h = 620, 260
    cx = (width - card_w) // 2
    cy = 120
    draw.rectangle([(cx, cy), (cx + card_w, cy + card_h)], fill=card_bg, outline='#334155', width=1)
    
    # Text inside card
    bbox_h1 = draw.textbbox((0, 0), card_title, font=font_h1)
    draw.text((cx + (card_w - (bbox_h1[2]-bbox_h1[0]))//2, cy + 35), card_title, fill='#38bdf8', font=font_h1)
    
    bbox_sub = draw.textbbox((0, 0), subtitle, font=font_p)
    draw.text((cx + (card_w - (bbox_sub[2]-bbox_sub[0]))//2, cy + 80), subtitle, fill='#cbd5e1', font=font_p)
    
    # Badge
    bbox_b = draw.textbbox((0, 0), badge_text, font=font_badge)
    bw = bbox_b[2] - bbox_b[0] + 24
    bx = cx + (card_w - bw) // 2
    by = cy + 120
    draw.rounded_rectangle([(bx, by), (bx + bw, by + 28)], radius=14, fill=badge_color)
    draw.text((bx + 12, by + 6), badge_text, fill='#ffffff', font=font_badge)
    
    # Status box
    bbox_inf = draw.textbbox((0, 0), info_text, font=font_info)
    iw = bbox_inf[2] - bbox_inf[0] + 30
    ix = cx + (card_w - iw) // 2
    iy = cy + 175
    draw.rectangle([(ix, iy), (ix + iw, iy + 32)], fill='#0f172a', outline='#1e293b')
    draw.text((ix + 15, iy + 8), info_text, fill='#4ade80', font=font_info)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)
    print(f'Generated: {output_path}')

# ==========================================
# GENERATE MODUL 08 ASSETS
# ==========================================
print('--- Generating Modul 8 Assets ---')

render_terminal(
    'assets/modul-08/01_git_init_status.png',
    'Ubuntu WSL2 — ~/web-devops',
    [
        ('user@devops-lab:~$ ', '#4af626', 'mkdir -p ~/web-devops && cd ~/web-devops', '#ffffff'),
        ('user@devops-lab:~/web-devops$ ', '#4af626', 'git init', '#ffffff'),
        ('Initialized empty Git repository in /home/user/web-devops/.git/', '#aaaaaa'),
        ('user@devops-lab:~/web-devops$ ', '#4af626', 'git config user.name "Praktikan DevOps"', '#ffffff'),
        ('user@devops-lab:~/web-devops$ ', '#4af626', 'git config user.email "praktikan@lab.local"', '#ffffff'),
        ('user@devops-lab:~/web-devops$ ', '#4af626', 'git status', '#ffffff'),
        ('On branch main', '#aaaaaa'),
        ('No commits yet', '#aaaaaa'),
        ('nothing to commit (create/copy files and use "git add" to track)', '#aaaaaa'),
        ('user@devops-lab:~/web-devops$ ', '#4af626', '', '#ffffff'),
    ]
)

render_terminal(
    'assets/modul-08/02_nano_index_html.png',
    'GNU nano 6.2 — index.html',
    [
        ('  GNU nano 6.2                    index.html                             ', '#000000'),
        ('<!DOCTYPE html>', '#ffffff'),
        ('<html lang="id">', '#ffffff'),
        ('<head>', '#ffffff'),
        ('    <meta charset="UTF-8">', '#ffffff'),
        ('    <title>DevOps Training Lab</title>', '#5bc0be'),
        ('</head>', '#ffffff'),
        ('<body>', '#ffffff'),
        ('    <div class="container">', '#ffffff'),
        ('        <h1>Platform Server Pelatihan Internal</h1>', '#38bdf8'),
        ('        <p>Modul 8: Otomasi Git & Shell Scripting</p>', '#cbd5e1'),
        ('        <p><span class="version-badge">Rilis: Versi 1.0.0 (Manual)</span></p>', '#facc15'),
        ('        <div class="status-box">Status Web Server: Berjalan Normal</div>', '#4ade80'),
        ('    </div>', '#ffffff'),
        ('</body>', '#ffffff'),
        ('</html>', '#ffffff'),
        ('^G Help       ^O WriteOut   ^W Where Is   ^K Cut        ^T Execute    ^C Location', '#ffffff'),
        ('^X Exit       ^R Read File  ^\\ Replace    ^U Paste      ^J Justify    ^/ Go To Line', '#ffffff')
    ]
)

render_terminal(
    'assets/modul-08/03_git_commit_v1.png',
    'Ubuntu WSL2 — ~/web-devops',
    [
        ('user@devops-lab:~/web-devops$ ', '#4af626', 'git status', '#ffffff'),
        ('Untracked files:', '#aaaaaa'),
        ('  (use "git add <file>..." to include in what will be committed)', '#aaaaaa'),
        ('	index.html', '#ff5f56'),
        ('user@devops-lab:~/web-devops$ ', '#4af626', 'git add index.html', '#ffffff'),
        ('user@devops-lab:~/web-devops$ ', '#4af626', 'git commit -m "feat: inisialisasi source code website rilis v1.0.0"', '#ffffff'),
        ('[main (root-commit) 4a2b91c] feat: inisialisasi source code website rilis v1.0.0', '#aaaaaa'),
        (' 1 file changed, 25 insertions(+)', '#aaaaaa'),
        (' create mode 100644 index.html', '#aaaaaa'),
        ('user@devops-lab:~/web-devops$ ', '#4af626', 'git log --oneline', '#ffffff'),
        ('4a2b91c (HEAD -> main) feat: inisialisasi source code website rilis v1.0.0', '#facc15'),
        ('user@devops-lab:~/web-devops$ ', '#4af626', '', '#ffffff')
    ]
)

render_terminal(
    'assets/modul-08/04_nginx_config_reload.png',
    'Ubuntu WSL2 — Nginx Config Verification',
    [
        ('user@devops-lab:~/web-devops$ ', '#4af626', 'chmod 755 $HOME && chmod -R 755 $HOME/web-devops', '#ffffff'),
        ('user@devops-lab:~/web-devops$ ', '#4af626', 'sudo nginx -t', '#ffffff'),
        ('nginx: the configuration file /etc/nginx/nginx.conf syntax is ok', '#27c93f'),
        ('nginx: configuration file /etc/nginx/nginx.conf test is successful', '#27c93f'),
        ('user@devops-lab:~/web-devops$ ', '#4af626', 'sudo systemctl reload nginx', '#ffffff'),
        ('user@devops-lab:~/web-devops$ ', '#4af626', 'sudo systemctl status nginx --no-pager', '#ffffff'),
        ('* nginx.service - A high performance web server and a reverse proxy', '#aaaaaa'),
        ('     Loaded: loaded (/lib/systemd/system/nginx.service; enabled)', '#aaaaaa'),
        ('     Active: active (running) since Sat 2026-10-10 18:15:32 UTC; 4s ago', '#27c93f'),
        ('user@devops-lab:~/web-devops$ ', '#4af626', '', '#ffffff')
    ]
)

render_browser(
    'assets/modul-08/05_browser_v1_live.png',
    'http://localhost',
    'DevOps Training Lab',
    'Platform Server Pelatihan Internal',
    'Modul 8: Otomasi Git & Shell Scripting',
    'Rilis: Versi 1.0.0 (Manual)',
    '#0284c7',
    'Status Web Server: Berjalan Normal'
)

render_terminal(
    'assets/modul-08/06_nano_deploy_script.png',
    'GNU nano 6.2 — deploy.sh',
    [
        ('  GNU nano 6.2                     deploy.sh                             ', '#000000'),
        ('#!/bin/bash', '#5bc0be'),
        ('set -eo pipefail', '#ffffff'),
        ('PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"', '#ffffff'),
        ('LOG_FILE="$PROJECT_DIR/deployment.log"', '#ffffff'),
        ('TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")', '#ffffff'),
        ('log_message() { echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"; }', '#facc15'),
        ('echo "=== MEMULAI SIKLUS OTOMASI DEPLOYMENT APLIKASI WEB ==="', '#38bdf8'),
        ('cd "$PROJECT_DIR"', '#ffffff'),
        ('test -f "index.html" || { log_message "[FATAL] File index.html tidak ada!"; exit 1; }', '#ff5f56'),
        ('sudo nginx -t > /dev/null 2>&1 || { log_message "[FATAL] Sintaks Nginx invalid!"; exit 1; }', '#ff5f56'),
        ('sudo systemctl reload nginx && log_message "[INFO] Nginx reloaded successfully."', '#27c93f'),
        ('HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/)', '#ffffff'),
        ('if [ "$HTTP_CODE" -eq 200 ]; then', '#ffffff'),
        ('    log_message "[SUCCESS] Deployment Berhasil! Status HTTP: $HTTP_CODE"', '#27c93f'),
        ('fi', '#ffffff')
    ]
)

render_terminal(
    'assets/modul-08/07_chmod_deploy_run.png',
    'Ubuntu WSL2 — Automated Deployment Run',
    [
        ('user@devops-lab:~/web-devops$ ', '#4af626', 'chmod +x deploy.sh', '#ffffff'),
        ('user@devops-lab:~/web-devops$ ', '#4af626', './deploy.sh', '#ffffff'),
        ('======================================================', '#38bdf8'),
        ('    MEMULAI SIKLUS OTOMASI DEPLOYMENT APLIKASI WEB    ', '#38bdf8'),
        ('======================================================', '#38bdf8'),
        ('[INFO] Integritas file proyek valid.', '#27c93f'),
        ('[INFO] Penyesuaian file permission selesai.', '#27c93f'),
        ('[INFO] Menjalankan uji sintaks Nginx (nginx -t)...', '#aaaaaa'),
        ('[INFO] Konfigurasi Nginx terverifikasi valid.', '#27c93f'),
        ('[INFO] Menerapkan konfigurasi baru ke Nginx...', '#aaaaaa'),
        ('[INFO] Service Nginx berhasil dimuat ulang (reload).', '#27c93f'),
        ('[INFO] Melakukan HTTP Health Check ke endpoint lokal...', '#aaaaaa'),
        ('[SUCCESS] Deployment Berhasil! Status HTTP: 200 | Git Commit: 7f3e1a0', '#27c93f'),
        ('======================================================', '#38bdf8'),
        (' APLIKASI BERHASIL DIRELOAD & BERJALAN DI http://localhost ', '#27c93f'),
        ('======================================================', '#38bdf8'),
        ('user@devops-lab:~/web-devops$ ', '#4af626', '', '#ffffff')
    ]
)

render_terminal(
    'assets/modul-08/08_deploy_log_audit.png',
    'Ubuntu WSL2 — Audit Log Verification',
    [
        ('user@devops-lab:~/web-devops$ ', '#4af626', 'cat deployment.log', '#ffffff'),
        ('[2026-10-10 18:20:10] [INFO] Integritas file proyek valid.', '#aaaaaa'),
        ('[2026-10-10 18:20:10] [INFO] Penyesuaian file permission selesai.', '#aaaaaa'),
        ('[2026-10-10 18:20:11] [INFO] Konfigurasi Nginx terverifikasi valid.', '#aaaaaa'),
        ('[2026-10-10 18:20:11] [INFO] Service Nginx berhasil dimuat ulang (reload).', '#aaaaaa'),
        ('[2026-10-10 18:20:12] [SUCCESS] Deployment Berhasil! Status HTTP: 200 | Git Commit: 4a2b91c', '#27c93f'),
        ('[2026-10-10 18:25:40] [INFO] Integritas file proyek valid.', '#aaaaaa'),
        ('[2026-10-10 18:25:40] [INFO] Penyesuaian file permission selesai.', '#aaaaaa'),
        ('[2026-10-10 18:25:41] [INFO] Konfigurasi Nginx terverifikasi valid.', '#aaaaaa'),
        ('[2026-10-10 18:25:41] [INFO] Service Nginx berhasil dimuat ulang (reload).', '#aaaaaa'),
        ('[2026-10-10 18:25:42] [SUCCESS] Deployment Berhasil! Status HTTP: 200 | Git Commit: 7f3e1a0', '#27c93f'),
        ('user@devops-lab:~/web-devops$ ', '#4af626', '', '#ffffff')
    ]
)

render_browser(
    'assets/modul-08/09_browser_v2_automated.png',
    'http://localhost',
    'DevOps Training Lab',
    'Platform Server Pelatihan Internal',
    'Modul 8: Otomasi Git & Shell Scripting',
    'Rilis: Versi 2.0.0 (Automated Script)',
    '#10b981',
    'Status Web Server: Berjalan Normal'
)

# ==========================================
# GENERATE MODUL 09 ASSETS
# ==========================================
print('--- Generating Modul 9 Assets ---')

render_terminal(
    'assets/modul-09/01_docker_hello_world.png',
    'Ubuntu WSL2 — Docker Service Verification',
    [
        ('user@devops-lab:~$ ', '#4af626', 'sudo service docker start', '#ffffff'),
        (' * Starting Docker: docker', '#aaaaaa'),
        ('                                                                   [ OK ]', '#27c93f'),
        ('user@devops-lab:~$ ', '#4af626', 'docker run --rm hello-world', '#ffffff'),
        ('Hello from Docker!', '#38bdf8'),
        ('This message shows that your installation appears to be working correctly.', '#aaaaaa'),
        ('To generate this message, Docker took the following steps:', '#aaaaaa'),
        (' 1. The Docker client contacted the Docker daemon.', '#aaaaaa'),
        (' 2. The Docker daemon pulled the "hello-world" image from Docker Hub.', '#aaaaaa'),
        (' 3. The Docker daemon created a new container from that image.', '#aaaaaa'),
        (' 4. The Docker daemon streamed that output to the Docker client.', '#aaaaaa'),
        ('user@devops-lab:~$ ', '#4af626', '', '#ffffff')
    ]
)

render_terminal(
    'assets/modul-09/02_dockerfile_view.png',
    'Ubuntu WSL2 — cat Dockerfile',
    [
        ('user@devops-lab:~/docker-web$ ', '#4af626', 'cat Dockerfile', '#ffffff'),
        ('# Menggunakan image Nginx versi Alpine Linux yang sangat ringan (~23MB)', '#666666'),
        ('FROM nginx:alpine', '#5bc0be'),
        ('LABEL maintainer="Tim Pelatihan Internal DevOps"', '#facc15'),
        ('RUN rm -rf /usr/share/nginx/html/*', '#ffffff'),
        ('COPY ./src /usr/share/nginx/html', '#ffffff'),
        ('EXPOSE 80', '#5bc0be'),
        ('CMD ["nginx", "-g", "daemon off;"]', '#38bdf8'),
        ('user@devops-lab:~/docker-web$ ', '#4af626', '', '#ffffff')
    ]
)

render_terminal(
    'assets/modul-09/03_docker_build.png',
    'Ubuntu WSL2 — docker build',
    [
        ('user@devops-lab:~/docker-web$ ', '#4af626', 'docker build -t my-devops-web:v1 .', '#ffffff'),
        ('[+] Building 2.1s (7/7) FINISHED', '#38bdf8'),
        (' => [internal] load build definition from Dockerfile              0.0s', '#aaaaaa'),
        (' => => transferring dockerfile: 312B                             0.0s', '#aaaaaa'),
        (' => [internal] load .dockerignore                                0.0s', '#aaaaaa'),
        (' => [internal] load metadata for docker.io/library/nginx:alpine  1.4s', '#aaaaaa'),
        (' => [1/3] FROM docker.io/library/nginx:alpine@sha256:d8b...      0.0s', '#aaaaaa'),
        (' => [2/3] RUN rm -rf /usr/share/nginx/html/*                    0.3s', '#aaaaaa'),
        (' => [3/3] COPY ./src /usr/share/nginx/html                       0.1s', '#aaaaaa'),
        (' => exporting to image                                           0.2s', '#aaaaaa'),
        (' => => exporting layers                                          0.2s', '#aaaaaa'),
        (' => => writing image sha256:8f41e0...                            0.0s', '#aaaaaa'),
        (' => => naming to docker.io/library/my-devops-web:v1              0.0s', '#27c93f'),
        ('user@devops-lab:~/docker-web$ ', '#4af626', '', '#ffffff')
    ]
)

render_terminal(
    'assets/modul-09/04_docker_images.png',
    'Ubuntu WSL2 — docker images',
    [
        ('user@devops-lab:~/docker-web$ ', '#4af626', 'docker images', '#ffffff'),
        ('REPOSITORY          TAG       IMAGE ID       CREATED          SIZE', '#38bdf8'),
        ('my-devops-web       v1        8f41e0b921fa   12 seconds ago   23.6MB', '#ffffff'),
        ('nginx               alpine    904b839211c4   2 days ago       23.5MB', '#aaaaaa'),
        ('hello-world         latest    d2c94e258dcb   5 months ago     13.3kB', '#aaaaaa'),
        ('user@devops-lab:~/docker-web$ ', '#4af626', '', '#ffffff')
    ]
)

render_terminal(
    'assets/modul-09/05_docker_run_ps.png',
    'Ubuntu WSL2 — docker run & ps',
    [
        ('user@devops-lab:~/docker-web$ ', '#4af626', 'docker run -d --name web-container-v1 -p 8080:80 my-devops-web:v1', '#ffffff'),
        ('c8f391e0a2948bb3198f8b02194857bdf82173510b019842a84759cbda0281c7', '#aaaaaa'),
        ('user@devops-lab:~/docker-web$ ', '#4af626', 'docker ps', '#ffffff'),
        ('CONTAINER ID   IMAGE             COMMAND                  STATUS         PORTS                  NAMES', '#38bdf8'),
        ('c8f391e0a294   my-devops-web:v1  "/docker-entrypoint.\u2026"  Up 4 seconds   0.0.0.0:8080->80/tcp   web-container-v1', '#ffffff'),
        ('user@devops-lab:~/docker-web$ ', '#4af626', '', '#ffffff')
    ]
)

render_browser(
    'assets/modul-09/06_browser_docker_8080.png',
    'http://localhost:8080',
    'Docker Containerization Lab',
    'Aplikasi Web Terkontainerisasi',
    'Modul 9: Docker Engine & Nginx Alpine',
    'Dockerized Container v1.0',
    '#5bc0be',
    'Berjalan secara terisolasi tanpa merusak host system.',
    bg_col='#0b132b',
    card_bg='#1c2541'
)

render_terminal(
    'assets/modul-09/07_docker_compose_up.png',
    'Ubuntu WSL2 — docker compose up & ps',
    [
        ('user@devops-lab:~/docker-web$ ', '#4af626', 'docker compose up -d', '#ffffff'),
        ('[+] Running 2/2', '#38bdf8'),
        (' \u2714 Network docker-web_devops-net     Created                         0.1s', '#27c93f'),
        (' \u2714 Container devops-production-web  Started                         0.3s', '#27c93f'),
        ('user@devops-lab:~/docker-web$ ', '#4af626', 'docker compose ps', '#ffffff'),
        ('NAME                   IMAGE                 COMMAND                  SERVICE   STATUS         PORTS', '#38bdf8'),
        ('devops-production-web  docker-web-web:latest "/docker-entrypoint.\u2026"  web       Up 6 seconds   0.0.0.0:8080->80/tcp', '#ffffff'),
        ('user@devops-lab:~/docker-web$ ', '#4af626', '', '#ffffff')
    ]
)

render_terminal(
    'assets/modul-09/08_docker_stats_logs.png',
    'Ubuntu WSL2 — docker stats & logs',
    [
        ('user@devops-lab:~/docker-web$ ', '#4af626', 'docker stats --no-stream', '#ffffff'),
        ('CONTAINER ID   NAME                   CPU %     MEM USAGE / LIMIT     MEM %     NET I/O           BLOCK I/O', '#38bdf8'),
        ('c8f391e0a294   devops-production-web  0.00%     5.82MiB / 3.84GiB     0.15%     1.24kB / 2.58kB   0B / 0B', '#ffffff'),
        ('user@devops-lab:~/docker-web$ ', '#4af626', 'docker compose logs --tail=4', '#ffffff'),
        ('devops-production-web  | 172.18.0.1 - - [10/Oct/2026:18:30:12 +0000] "GET / HTTP/1.1" 200 812', '#aaaaaa'),
        ('devops-production-web  | 172.18.0.1 - - [10/Oct/2026:18:30:13 +0000] "GET /favicon.ico HTTP/1.1" 404 153', '#aaaaaa'),
        ('devops-production-web  | 172.18.0.1 - - [10/Oct/2026:18:30:15 +0000] "GET / HTTP/1.1" 200 812', '#27c93f'),
        ('user@devops-lab:~/docker-web$ ', '#4af626', '', '#ffffff')
    ]
)

# ==========================================
# GENERATE MODUL 10 ASSETS
# ==========================================
print('--- Generating Modul 10 Assets ---')

render_terminal(
    'assets/modul-10/01_project_structure.png',
    'Ubuntu WSL2 — CI/CD Workspace Structure',
    [
        ('user@devops-lab:~/cicd-devops$ ', '#4af626', 'ls -la .github/workflows/', '#ffffff'),
        ('total 12', '#aaaaaa'),
        ('drwxr-xr-x 2 user user 4096 Oct 10 18:35 .', '#aaaaaa'),
        ('drwxr-xr-x 3 user user 4096 Oct 10 18:35 ..', '#aaaaaa'),
        ('-rw-r--r-- 1 user user 2410 Oct 10 18:36 ci-cd.yml', '#27c93f'),
        ('user@devops-lab:~/cicd-devops$ ', '#4af626', 'head -n 12 .github/workflows/ci-cd.yml', '#ffffff'),
        ('name: Automated CI/CD Pipeline', '#38bdf8'),
        ('on:', '#ffffff'),
        ('  push:', '#ffffff'),
        ('    branches: [ "main" ]', '#facc15'),
        ('  pull_request:', '#ffffff'),
        ('    branches: [ "main" ]', '#facc15'),
        ('permissions:', '#ffffff'),
        ('  contents: read', '#aaaaaa'),
        ('  packages: write', '#27c93f'),
        ('jobs:', '#ffffff'),
        ('  code-quality:', '#38bdf8'),
        ('user@devops-lab:~/cicd-devops$ ', '#4af626', '', '#ffffff')
    ]
)

render_terminal(
    'assets/modul-10/02_git_push_main.png',
    'Ubuntu WSL2 — git push origin main',
    [
        ('user@devops-lab:~/cicd-devops$ ', '#4af626', 'git add .', '#ffffff'),
        ('user@devops-lab:~/cicd-devops$ ', '#4af626', 'git commit -m "ci: tambahkan workflow pipeline github actions"', '#ffffff'),
        ('[main 5d12a8b] ci: tambahkan workflow pipeline github actions', '#aaaaaa'),
        (' 3 files changed, 85 insertions(+)', '#aaaaaa'),
        (' create mode 100644 .github/workflows/ci-cd.yml', '#aaaaaa'),
        (' create mode 100644 Dockerfile', '#aaaaaa'),
        (' create mode 100644 index.html', '#aaaaaa'),
        ('user@devops-lab:~/cicd-devops$ ', '#4af626', 'git push origin main', '#ffffff'),
        ('Enumerating objects: 6, done.', '#aaaaaa'),
        ('Counting objects: 100% (6/6), done.', '#aaaaaa'),
        ('Writing objects: 100% (6/6), 1.42 KiB | 1.42 MiB/s, done.', '#aaaaaa'),
        ('To https://github.com/rhaffle87/my-devops-cicd.git', '#aaaaaa'),
        ('   3a19b2f..5d12a8b  main -> main', '#27c93f'),
        ('user@devops-lab:~/cicd-devops$ ', '#4af626', '', '#ffffff')
    ]
)

# Mockup UI for GitHub Actions
def render_github_actions_mock(output_path, status='success'):
    font_title = ImageFont.truetype('arialbd.ttf', 16)
    font_p = ImageFont.truetype('arial.ttf', 13)
    font_bold = ImageFont.truetype('arialbd.ttf', 13)
    
    img = Image.new('RGB', (960, 420), color='#0d1117')
    draw = ImageDraw.Draw(img)
    
    # Header bar
    draw.rectangle([(0, 0), (960, 60)], fill='#161b22', outline='#30363d')
    draw.text((25, 20), 'Actions', fill='#f0f6fc', font=font_title)
    draw.text((105, 22), '/ Automated CI/CD Pipeline #12', fill='#8b949e', font=font_p)
    
    # Run info
    draw.rectangle([(25, 80), (935, 140)], fill='#161b22', outline='#30363d')
    if status == 'success':
        draw.ellipse([(45, 100), (65, 120)], fill='#238636')
        draw.text((75, 102), 'ci: tambahkan workflow pipeline github actions', fill='#f0f6fc', font=font_bold)
        draw.text((450, 103), 'Workflow run passed in 48s \u2014 commit 5d12a8b', fill='#8b949e', font=font_p)
    else:
        draw.ellipse([(45, 100), (65, 120)], fill='#da3633')
        draw.text((75, 102), 'fix: simulasi kegagalan verifikasi html', fill='#f0f6fc', font=font_bold)
        draw.text((450, 103), 'Workflow run failed in 12s \u2014 commit 9e4f201', fill='#8b949e', font=font_p)
        
    # Jobs box
    # Job 1
    draw.rectangle([(50, 170), (450, 360)], fill='#161b22', outline='#30363d')
    draw.rectangle([(50, 170), (450, 210)], fill='#21262d')
    col1 = '#238636' if status == 'success' else '#da3633'
    draw.ellipse([(65, 182), (81, 198)], fill=col1)
    draw.text((90, 182), 'code-quality (Lint & Integrity)', fill='#f0f6fc', font=font_bold)
    
    steps_j1 = [
        ('\u2714 Unduh Source Code (Checkout)', '#3fb950', '2s'),
        ('\u2714 Validasi Integritas File', '#3fb950', '1s'),
        ('\u2714 Validasi HTML Sintaks Sederhana' if status == 'success' else '\u2716 Validasi HTML Sintaks Sederhana', '#3fb950' if status == 'success' else '#f85149', '1s'),
        ('\u2714 Complete Job' if status == 'success' else '\u2716 Process completed with exit code 1', '#8b949e' if status == 'success' else '#f85149', '')
    ]
    y = 225
    for s_name, s_col, s_dur in steps_j1:
        draw.text((70, y), s_name, fill=s_col, font=font_p)
        draw.text((410, y), s_dur, fill='#8b949e', font=font_p)
        y += 28
        
    # Job 2
    draw.rectangle([(510, 170), (910, 360)], fill='#161b22', outline='#30363d')
    draw.rectangle([(510, 170), (910, 210)], fill='#21262d')
    col2 = '#238636' if status == 'success' else '#8b949e'
    draw.ellipse([(525, 182), (541, 198)], fill=col2)
    draw.text((550, 182), 'build-and-push (GHCR Publish)', fill='#f0f6fc', font=font_bold)
    
    if status == 'success':
        steps_j2 = [
            ('\u2714 Setup Docker Buildx', '#3fb950', '4s'),
            ('\u2714 Login ke GitHub Container Registry', '#3fb950', '1s'),
            ('\u2714 Ekstrak Metadata Tagging Image', '#3fb950', '1s'),
            ('\u2714 Pembangunan dan Push ke GHCR', '#3fb950', '32s')
        ]
    else:
        steps_j2 = [
            ('\u229d Setup Docker Buildx (Skipped)', '#8b949e', ''),
            ('\u229d Login ke GitHub Container Registry (Skipped)', '#8b949e', ''),
            ('\u229d Ekstrak Metadata Tagging (Skipped)', '#8b949e', ''),
            ('\u229d Pembangunan dan Push Image (Cancelled)', '#8b949e', '')
        ]
    y = 225
    for s_name, s_col, s_dur in steps_j2:
        draw.text((530, y), s_name, fill=s_col, font=font_p)
        if s_dur:
            draw.text((865, y), s_dur, fill='#8b949e', font=font_p)
        y += 28
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)
    print(f'Generated: {output_path}')

def render_github_packages_mock(output_path, width=960, height=420):
    font_title = ImageFont.truetype('arialbd.ttf', 16)
    font_h2 = ImageFont.truetype('arialbd.ttf', 15)
    font_p = ImageFont.truetype('arial.ttf', 13)
    font_bold = ImageFont.truetype('arialbd.ttf', 12)
    font_code = ImageFont.truetype('consola.ttf', 13)

    img = Image.new('RGB', (width, height), color='#0d1117')
    draw = ImageDraw.Draw(img)

    # Header bar
    draw.rectangle([(0, 0), (width, 60)], fill='#161b22', outline='#30363d')
    draw.text((25, 20), 'Packages', fill='#f0f6fc', font=font_title)
    draw.text((115, 22), '/ rhaffle87', fill='#8b949e', font=font_p)

    # Package card
    draw.rectangle([(25, 80), (width - 25, 220)], fill='#161b22', outline='#30363d')
    draw.rounded_rectangle([(45, 100), (105, 150)], radius=6, fill='#1f6feb')
    draw.text((50, 118), 'DOCKER', fill='#ffffff', font=font_bold)

    # Package Info
    draw.text((120, 100), 'ghcr.io/rhaffle87/my-devops-cicd', fill='#58a6ff', font=font_h2)
    draw.text((120, 128), 'Docker container image diterbitkan secara otomatis oleh pipeline GitHub Actions.', fill='#8b949e', font=font_p)
    
    # Tags & metadata
    draw.rounded_rectangle([(120, 160), (180, 185)], radius=12, fill='#21262d', outline='#30363d')
    draw.text((130, 164), 'latest', fill='#3fb950', font=font_bold)

    draw.rounded_rectangle([(190, 160), (260, 185)], radius=12, fill='#21262d', outline='#30363d')
    draw.text((200, 164), '5d12a8b', fill='#8b949e', font=font_bold)

    draw.text((280, 165), 'Published 2 minutes ago by @rhaffle87 \u2022 Public Registry', fill='#8b949e', font=font_p)

    # CLI Pull command snippet box
    draw.rectangle([(25, 250), (width - 25, 340)], fill='#161b22', outline='#30363d')
    draw.text((45, 265), 'Pull this package from the command line:', fill='#f0f6fc', font=font_bold)
    draw.rectangle([(45, 290), (width - 45, 325)], fill='#0d1117', outline='#30363d')
    draw.text((55, 298), 'docker pull ghcr.io/rhaffle87/my-devops-cicd:latest', fill='#79c0ff', font=font_code)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)
    print(f'Generated: {output_path}')

def render_browser_ssl_warning(output_path, width=960, height=480):
    font_title = ImageFont.truetype('arial.ttf', 13)
    font_url = ImageFont.truetype('arial.ttf', 13)
    font_h1 = ImageFont.truetype('arialbd.ttf', 22)
    font_p = ImageFont.truetype('arial.ttf', 14)
    font_btn = ImageFont.truetype('arialbd.ttf', 13)
    font_code = ImageFont.truetype('consola.ttf', 12)

    img = Image.new('RGB', (width, height), color='#ffffff')
    draw = ImageDraw.Draw(img)

    # Browser chrome header
    draw.rectangle([(0, 0), (width, 70)], fill='#dee1e6')
    draw.ellipse([(14, 14), (24, 24)], fill='#ff5f56')
    draw.ellipse([(32, 14), (42, 24)], fill='#ffbd2e')
    draw.ellipse([(50, 14), (60, 24)], fill='#27c93f')

    # Tab
    draw.rectangle([(90, 8), (280, 38)], fill='#ffffff')
    draw.text((105, 14), 'Privacy error', fill='#3c4043', font=font_title)

    # URL bar with Not Secure / Red badge
    draw.rectangle([(80, 42), (width - 30, 64)], fill='#ffffff', outline='#dadce0')
    draw.rectangle([(85, 45), (175, 61)], fill='#fce8e6', outline='#fad2cf')
    draw.text((90, 47), '\u26a0 Not secure', fill='#c5221f', font=font_title)
    draw.text((185, 45), 'https://localhost', fill='#3c4043', font=font_url)

    # Warning text
    draw.text((80, 140), 'Your connection is not private', fill='#202124', font=font_h1)
    draw.text((80, 180), 'Attackers might be trying to steal your information from localhost (for example, passwords, messages, or credit cards).', fill='#5f6368', font=font_p)
    draw.text((80, 220), 'NET::ERR_CERT_AUTHORITY_INVALID', fill='#5f6368', font=font_code)

    # Buttons
    # Advanced Button
    draw.rectangle([(80, 280), (180, 316)], fill='#ffffff', outline='#dadce0')
    draw.text((100, 290), 'Advanced', fill='#1a73e8', font=font_btn)

    # Back to safety button
    draw.rectangle([(width - 200, 280), (width - 60, 316)], fill='#1a73e8')
    draw.text((width - 175, 290), 'Back to safety', fill='#ffffff', font=font_btn)

    # Explanation text for Advanced
    draw.text((80, 340), 'This server could not prove that it is localhost; its security certificate is not trusted by your operating system.', fill='#5f6368', font=font_p)
    draw.text((80, 370), '\u2192 Proceed to localhost (unsafe)', fill='#1a73e8', font=font_btn)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)
    print(f'Generated: {output_path}')

render_github_actions_mock('assets/modul-10/03_github_actions_workflow.png', status='success')
render_github_packages_mock('assets/modul-10/04_github_packages_ui.png')

render_terminal(
    'assets/modul-10/05_ghcr_packages.png',
    'Ubuntu WSL2 — Pull Published Image from GHCR',
    [
        ('user@devops-lab:~$ ', '#4af626', 'docker pull ghcr.io/rhaffle87/my-devops-cicd:latest', '#ffffff'),
        ('latest: Pulling from rhaffle87/my-devops-cicd', '#aaaaaa'),
        ('4abcf2c29fed: Already exists', '#aaaaaa'),
        ('12e9b084931a: Pull complete', '#27c93f'),
        ('Digest: sha256:d8b2910fae94821034bc0281a8c9b2041e8c9b28a8d', '#aaaaaa'),
        ('Status: Downloaded newer image for ghcr.io/rhaffle87/my-devops-cicd:latest', '#27c93f'),
        ('docker.io/rhaffle87/my-devops-cicd:latest', '#38bdf8'),
        ('user@devops-lab:~$ ', '#4af626', 'docker images | grep my-devops-cicd', '#ffffff'),
        ('ghcr.io/rhaffle87/my-devops-cicd  latest    e1892fbc018a   2 minutes ago   23.6MB', '#ffffff'),
        ('user@devops-lab:~$ ', '#4af626', '', '#ffffff')
    ]
)

render_github_actions_mock('assets/modul-10/06_broken_build_ci_alert.png', status='failed')

# ==========================================
# GENERATE MODUL 11 ASSETS
# ==========================================
print('--- Generating Modul 11 Assets ---')

render_terminal(
    'assets/modul-11/01_openssl_cert_gen.png',
    'Ubuntu WSL2 — OpenSSL Self-Signed Generation',
    [
        ('user@devops-lab:~/nginx-proxy-lab/certs$ ', '#4af626', 'openssl req -x509 -nodes -days 365 -newkey rsa:2048 \\', '#ffffff'),
        ('>   -keyout server.key \\', '#ffffff'),
        ('>   -out server.crt \\', '#ffffff'),
        ('>   -subj "/C=ID/ST=JawaTimur/L=Surabaya/O=PelatihanInternal/CN=localhost"', '#ffffff'),
        ('Generating a RSA private key', '#aaaaaa'),
        ('......................................................+++++', '#aaaaaa'),
        ('writing new private key to \'server.key\'', '#27c93f'),
        ('-----', '#aaaaaa'),
        ('user@devops-lab:~/nginx-proxy-lab/certs$ ', '#4af626', 'ls -la', '#ffffff'),
        ('-rw------- 1 user user 1704 Oct 10 18:40 server.key', '#ffbd2e'),
        ('-rw-r--r-- 1 user user 1326 Oct 10 18:40 server.crt', '#27c93f'),
        ('user@devops-lab:~/nginx-proxy-lab/certs$ ', '#4af626', '', '#ffffff')
    ]
)

render_terminal(
    'assets/modul-11/02_nginx_proxy_conf.png',
    'Ubuntu WSL2 — cat proxy/nginx.conf',
    [
        ('user@devops-lab:~/nginx-proxy-lab$ ', '#4af626', 'cat proxy/nginx.conf', '#ffffff'),
        ('events { worker_connections 1024; }', '#ffffff'),
        ('http {', '#ffffff'),
        ('    upstream my_cluster {', '#38bdf8'),
        ('        server app1:80;', '#facc15'),
        ('        server app2:80;', '#facc15'),
        ('    }', '#38bdf8'),
        ('    server {', '#ffffff'),
        ('        listen 80;', '#ffffff'),
        ('        server_name localhost;', '#ffffff'),
        ('        return 301 https://$host$request_uri;', '#ff5f56'),
        ('    }', '#ffffff'),
        ('    server {', '#ffffff'),
        ('        listen 443 ssl;', '#27c93f'),
        ('        ssl_certificate     /etc/nginx/certs/server.crt;', '#aaaaaa'),
        ('        ssl_certificate_key /etc/nginx/certs/server.key;', '#aaaaaa'),
        ('        location / { proxy_pass http://my_cluster; }', '#38bdf8'),
        ('    }', '#ffffff'),
        ('}', '#ffffff')
    ]
)

render_terminal(
    'assets/modul-11/03_docker_compose_cluster.png',
    'Ubuntu WSL2 — 3 Containers Cluster Running',
    [
        ('user@devops-lab:~/nginx-proxy-lab$ ', '#4af626', 'docker compose up -d', '#ffffff'),
        ('[+] Running 4/4', '#38bdf8'),
        (' \u2714 Network nginx-proxy-lab_internal-net  Created                       0.1s', '#27c93f'),
        (' \u2714 Container backend-alpha                 Started                       0.3s', '#27c93f'),
        (' \u2714 Container backend-beta                  Started                       0.3s', '#27c93f'),
        (' \u2714 Container nginx-gateway                 Started                       0.4s', '#27c93f'),
        ('user@devops-lab:~/nginx-proxy-lab$ ', '#4af626', 'docker compose ps', '#ffffff'),
        ('NAME            IMAGE          COMMAND                  SERVICE         STATUS         PORTS', '#38bdf8'),
        ('backend-alpha   nginx:alpine   "/docker-entrypoint.\u2026"  app1            Up 8 seconds   80/tcp', '#ffffff'),
        ('backend-beta    nginx:alpine   "/docker-entrypoint.\u2026"  app2            Up 8 seconds   80/tcp', '#ffffff'),
        ('nginx-gateway   nginx:alpine   "/docker-entrypoint.\u2026"  reverse-proxy   Up 7 seconds   0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp', '#27c93f'),
        ('user@devops-lab:~/nginx-proxy-lab$ ', '#4af626', '', '#ffffff')
    ]
)

render_terminal(
    'assets/modul-11/04_curl_http_redirect.png',
    'Ubuntu WSL2 — HTTP 301 Redirect Check',
    [
        ('user@devops-lab:~/nginx-proxy-lab$ ', '#4af626', 'curl -I http://localhost', '#ffffff'),
        ('HTTP/1.1 301 Moved Permanently', '#facc15'),
        ('Server: nginx/1.25.4', '#aaaaaa'),
        ('Date: Sat, 10 Oct 2026 18:45:10 GMT', '#aaaaaa'),
        ('Content-Type: text/html', '#aaaaaa'),
        ('Content-Length: 169', '#aaaaaa'),
        ('Connection: keep-alive', '#aaaaaa'),
        ('Location: https://localhost/', '#27c93f'),
        ('user@devops-lab:~/nginx-proxy-lab$ ', '#4af626', '', '#ffffff')
    ]
)

render_terminal(
    'assets/modul-11/05_curl_load_balancer_round_robin.png',
    'Ubuntu WSL2 — Round-Robin Load Balancer Verification',
    [
        ('user@devops-lab:~/nginx-proxy-lab$ ', '#4af626', 'for i in {1..4}; do curl -sk https://localhost | grep "Backend Server Instance"; done', '#ffffff'),
        ('    <h1>Backend Server Instance: ALPHA [01]</h1>', '#38bdf8'),
        ('    <h1>Backend Server Instance: BETA [02]</h1>', '#4ade80'),
        ('    <h1>Backend Server Instance: ALPHA [01]</h1>', '#38bdf8'),
        ('    <h1>Backend Server Instance: BETA [02]</h1>', '#4ade80'),
        ('user@devops-lab:~/nginx-proxy-lab$ ', '#4af626', '# Load balancing round-robin berhasil bergantian 50:50!', '#aaaaaa'),
        ('user@devops-lab:~/nginx-proxy-lab$ ', '#4af626', '', '#ffffff')
    ]
)

render_browser_ssl_warning('assets/modul-11/06_browser_ssl_warning.png')

render_browser(
    'assets/modul-11/07_browser_https_instance_alpha.png',
    'https://localhost (SSL Encrypted)',
    'Reverse Proxy Gateway',
    'Backend Server Instance: ALPHA [01]',
    'Melayani request melalui Nginx Load Balancer Round-Robin',
    'HTTPS / TLSv1.3 Active',
    '#10b981',
    'Upstream Node: app1 (172.19.0.2:80) | Status: 200 OK',
    bg_col='#0f172a',
    card_bg='#1e3a8a'
)

render_browser(
    'assets/modul-11/08_browser_https_instance_beta.png',
    'https://localhost (SSL Encrypted)',
    'Reverse Proxy Gateway',
    'Backend Server Instance: BETA [02]',
    'Melayani request melalui Nginx Load Balancer Round-Robin',
    'HTTPS / TLSv1.3 Active',
    '#10b981',
    'Upstream Node: app2 (172.19.0.3:80) | Status: 200 OK',
    bg_col='#0f172a',
    card_bg='#065f46'
)

render_terminal(
    'assets/modul-11/09_observability_access_logs.png',
    'Ubuntu WSL2 — Nginx Observability Real-time Stream',
    [
        ('user@devops-lab:~/nginx-proxy-lab$ ', '#4af626', 'docker compose logs -f reverse-proxy', '#ffffff'),
        ('nginx-gateway  | 172.19.0.1 - - [10/Oct/2026:18:48:01] "GET / HTTP/2.0" 200 412 Upstream: 172.19.0.2:80 Status: 200 ResponseTime: 0.001s', '#38bdf8'),
        ('nginx-gateway  | 172.19.0.1 - - [10/Oct/2026:18:48:02] "GET / HTTP/2.0" 200 410 Upstream: 172.19.0.3:80 Status: 200 ResponseTime: 0.001s', '#4ade80'),
        ('nginx-gateway  | 172.19.0.1 - - [10/Oct/2026:18:48:04] "GET / HTTP/2.0" 200 412 Upstream: 172.19.0.2:80 Status: 200 ResponseTime: 0.000s', '#38bdf8'),
        ('nginx-gateway  | 172.19.0.1 - - [10/Oct/2026:18:48:05] "GET / HTTP/2.0" 200 410 Upstream: 172.19.0.3:80 Status: 200 ResponseTime: 0.001s', '#4ade80'),
        ('^CGracefully stopping... (press Ctrl+C again to force)', '#aaaaaa'),
        ('user@devops-lab:~/nginx-proxy-lab$ ', '#4af626', '', '#ffffff')
    ]
)

print('All assets successfully generated!')

