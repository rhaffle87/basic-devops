import os
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO_ROOT)

def make_windows_icon(size=28):
    img = Image.new('RGBA', (size, size), (0,0,0,0))
    d = ImageDraw.Draw(img)
    g = 2
    w = (size - g) // 2
    d.rectangle([(0, 0), (w, w)], fill='#0078d7')
    d.rectangle([(w + g, 0), (size, w)], fill='#0078d7')
    d.rectangle([(0, w + g), (w, size)], fill='#0078d7')
    d.rectangle([(w + g, w + g), (size, size)], fill='#0078d7')
    return img

def make_nginx_icon(size=28):
    img = Image.new('RGBA', (size, size), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([(0,0), (size-1, size-1)], radius=5, fill='#009639')
    f = ImageFont.truetype('arialbd.ttf', int(size*0.65))
    d.text((size//2, size//2 - 1), 'N', fill='#ffffff', font=f, anchor='mm')
    return img

def make_ubuntu_icon(size=28):
    img = Image.new('RGBA', (size, size), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.ellipse([(0, 0), (size-1, size-1)], fill='#e95420')
    d.ellipse([(size*0.25, size*0.25), (size*0.75, size*0.75)], fill='#ffffff')
    d.ellipse([(size*0.35, size*0.35), (size*0.65, size*0.65)], fill='#e95420')
    return img

def make_chrome_icon(size=28):
    img = Image.new('RGBA', (size, size), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.ellipse([(0, 0), (size-1, size-1)], fill='#4285f4')
    d.ellipse([(size*0.12, size*0.12), (size*0.88, size*0.88)], fill='#ea4335')
    d.ellipse([(size*0.32, size*0.32), (size*0.68, size*0.68)], fill='#ffffff')
    d.ellipse([(size*0.38, size*0.38), (size*0.62, size*0.62)], fill='#4285f4')
    return img

def make_html5_icon(size=28):
    img = Image.new('RGBA', (size, size), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([(0,0), (size-1, size-1)], radius=5, fill='#e34f26')
    f = ImageFont.truetype('arialbd.ttf', int(size*0.6))
    d.text((size//2, size//2 - 1), '5', fill='#ffffff', font=f, anchor='mm')
    return img

def draw_arrow(draw, start, end, color='#2563eb', width=3, dashed=False):
    x1, y1 = start
    x2, y2 = end
    if not dashed:
        draw.line([start, end], fill=color, width=width)
    else:
        dist = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        segments = max(1, int(dist // 10))
        for i in range(segments):
            if i % 2 == 0:
                sx = x1 + (x2 - x1) * (i / segments)
                sy = y1 + (y2 - y1) * (i / segments)
                ex = x1 + (x2 - x1) * ((i + 1) / segments)
                ey = y1 + (y2 - y1) * ((i + 1) / segments)
                draw.line([(sx, sy), (ex, ey)], fill=color, width=width)
                
    import math
    angle = math.atan2(y2 - y1, x2 - x1)
    arrow_len = 10
    head_angle = math.pi / 6
    p1 = (x2 - arrow_len * math.cos(angle - head_angle), y2 - arrow_len * math.sin(angle - head_angle))
    p2 = (x2 - arrow_len * math.cos(angle + head_angle), y2 - arrow_len * math.sin(angle + head_angle))
    draw.polygon([end, p1, p2], fill=color)

def generate_modul07_diagram():
    w, h = 1240, 740
    img = Image.new('RGB', (w, h), color='#f8fafc')
    draw = ImageDraw.Draw(img)

    font_banner_title = ImageFont.truetype('arialbd.ttf', 17)
    font_banner_sub = ImageFont.truetype('arial.ttf', 12)
    font_box_title = ImageFont.truetype('arialbd.ttf', 14)
    font_node_title = ImageFont.truetype('arialbd.ttf', 13)
    font_node_sub = ImageFont.truetype('arial.ttf', 11)
    font_mono = ImageFont.truetype('consola.ttf', 11)
    font_edge = ImageFont.truetype('arialbd.ttf', 11)
    font_edge_sub = ImageFont.truetype('arial.ttf', 10)

    # Grid background dots
    for x in range(20, w, 30):
        for y in range(20, h, 30):
            draw.point((x, y), fill='#e2e8f0')

    # Top Banner
    draw.rounded_rectangle([(30, 18), (w - 30, 74)], radius=8, fill='#ffffff', outline='#cbd5e1', width=1)
    draw.text((w // 2, 35), 'Arsitektur Web Server Nginx & Siklus Penanganan HTTP Request (Modul 7)', fill='#0f172a', font=font_banner_title, anchor='mm')
    draw.text((w // 2, 57), 'Integrasi Host Windows 10/11  •  Lingkungan Virtualisasi WSL2 Ubuntu 22.04 LTS  •  Event-Driven Nginx Engine', fill='#64748b', font=font_banner_sub, anchor='mm')

    # ================= CONTAINER 1: WINDOWS =================
    cx1, cy1, cw1, ch1 = 35, 95, 340, 620
    draw.rounded_rectangle([(cx1, cy1), (cx1 + cw1, cy1 + ch1)], radius=10, fill='#f0f6ff', outline='#0078d7', width=2)
    # Header bar
    draw.rounded_rectangle([(cx1, cy1), (cx1 + cw1, cy1 + 42)], radius=10, fill='#0078d7')
    draw.rectangle([(cx1, cy1 + 32), (cx1 + cw1, cy1 + 42)], fill='#0078d7')
    draw.text((cx1 + 18, cy1 + 20), 'Host Windows 10/11 (Client OS)', fill='#ffffff', font=font_box_title, anchor='lm')
    win_icon = make_windows_icon(24)
    img.paste(win_icon, (cx1 + cw1 - 38, cy1 + 9), win_icon)

    # Browser Mockup
    bx, by, bw, bh = cx1 + 18, cy1 + 55, cw1 - 36, 400
    draw.rounded_rectangle([(bx, by), (bx + bw, by + bh)], radius=8, fill='#ffffff', outline='#93c5fd', width=2)
    # Browser chrome header
    draw.rounded_rectangle([(bx, by), (bx + bw, by + 68)], radius=8, fill='#f1f5f9')
    draw.rectangle([(bx, by + 58), (bx + bw, by + 68)], fill='#f1f5f9')
    draw.line([(bx, by + 68), (bx + bw, by + 68)], fill='#cbd5e1', width=1)
    
    # Chrome tab
    chrome_icon = make_chrome_icon(18)
    img.paste(chrome_icon, (bx + 10, by + 8), chrome_icon)
    draw.text((bx + 34, by + 17), 'Google Chrome • Portofolio Web', fill='#334155', font=font_node_sub, anchor='lm')
    # Address bar
    draw.rounded_rectangle([(bx + 10, by + 34), (bx + bw - 10, by + 60)], radius=4, fill='#ffffff', outline='#cbd5e1')
    draw.text((bx + 20, by + 47), '🔒 http://localhost:80/index.html', fill='#16a34a', font=font_mono, anchor='lm')

    # Web page preview inside browser
    draw.rounded_rectangle([(bx + 15, by + 80), (bx + bw - 15, by + 200)], radius=6, fill='#1e3a8a')
    draw.text((bx + bw // 2, by + 110), 'Website Portofolio Praktikan', fill='#ffffff', font=font_node_title, anchor='mm')
    draw.text((bx + bw // 2, by + 132), 'Nginx Static File Serving Active', fill='#93c5fd', font=font_node_sub, anchor='mm')
    draw.rounded_rectangle([(bx + bw // 2 - 55, by + 148), (bx + bw // 2 + 55, by + 172)], radius=12, fill='#10b981')
    draw.text((bx + bw // 2, by + 160), 'HTTP 200 OK', fill='#ffffff', font=font_edge, anchor='mm')

    # Feature checklist
    features = [
        "• Status: 200 OK (Dokumen Terunggah)",
        "• Header: Content-Type: text/html",
        "• Latency: < 1ms (Loopback Adapter)",
        "• Render: HTML5, CSS3, JavaScript",
        "• Connection: Keep-Alive Non-blocking"
    ]
    fy = by + 218
    for f in features:
        draw.text((bx + 18, fy), f, fill='#334155', font=font_mono)
        fy += 23

    # Client Socket box
    sx, sy, sw, sh = cx1 + 18, cy1 + 470, cw1 - 36, 130
    draw.rounded_rectangle([(sx, sy), (sx + sw, sy + sh)], radius=8, fill='#e0f2fe', outline='#0284c7', width=1)
    draw.text((sx + 15, sy + 22), 'Klien HTTP (OS Socket & Winsock)', fill='#0369a1', font=font_node_title)
    draw.text((sx + 15, sy + 46), 'Loopback Interface: 127.0.0.1 (localhost)', fill='#334155', font=font_node_sub)
    draw.text((sx + 15, sy + 68), 'Port Sumber Klien: TCP Dinamis :54820', fill='#64748b', font=font_mono)
    draw.text((sx + 15, sy + 90), 'Winsock NAT forwarding ke WSL2 vEthernet', fill='#0284c7', font=font_node_sub)
    draw.text((sx + 15, sy + 110), 'Target Socket: 0.0.0.0:80 (Ubuntu Server)', fill='#166534', font=font_mono)

    # ================= CONTAINER 2: WSL2 UBUNTU =================
    cx2, cy2, cw2, ch2 = 490, 95, 715, 620
    draw.rounded_rectangle([(cx2, cy2), (cx2 + cw2, cy2 + ch2)], radius=10, fill='#fff7ed', outline='#ea580c', width=2)
    # Header bar
    draw.rounded_rectangle([(cx2, cy2), (cx2 + cw2, cy2 + 42)], radius=10, fill='#ea580c')
    draw.rectangle([(cx2, cy2 + 32), (cx2 + cw2, cy2 + 42)], fill='#ea580c')
    draw.text((cx2 + 18, cy2 + 20), 'Windows Subsystem for Linux (WSL2) — Ubuntu 22.04 LTS Server', fill='#ffffff', font=font_box_title, anchor='lm')
    ub_icon = make_ubuntu_icon(24)
    img.paste(ub_icon, (cx2 + cw2 - 38, cy2 + 9), ub_icon)

    # Sub-Container Nginx
    nx, ny, nw, nh = cx2 + 22, cy2 + 55, cw2 - 44, 305
    draw.rounded_rectangle([(nx, ny), (nx + nw, ny + nh)], radius=8, fill='#f0fdf4', outline='#16a34a', width=1)
    # Header
    draw.rounded_rectangle([(nx, ny), (nx + nw, ny + 34)], radius=8, fill='#16a34a')
    draw.rectangle([(nx, ny + 24), (nx + nw, ny + 34)], fill='#16a34a')
    draw.text((nx + 15, ny + 17), 'Layanan Web Server Nginx (systemctl status nginx)', fill='#ffffff', font=font_node_title, anchor='lm')
    ng_icon = make_nginx_icon(22)
    img.paste(ng_icon, (nx + nw - 34, ny + 6), ng_icon)

    # Master Process
    mx, my, mw, mh = nx + 18, ny + 45, nw - 36, 90
    draw.rounded_rectangle([(mx, my), (mx + mw, my + mh)], radius=6, fill='#dcfce7', outline='#22c55e', width=1)
    draw.text((mx + 15, my + 18), 'Nginx Master Process', fill='#15803d', font=font_node_title)
    draw.text((mx + 15, my + 38), 'User: root | Hak Istimewa (Privileged Daemon) | PID 1240', fill='#166534', font=font_node_sub)
    draw.text((mx + 15, my + 58), '• Membaca & reload konfigurasi: /etc/nginx/sites-available/default', fill='#475569', font=font_node_sub)
    draw.text((mx + 390, my + 58), '• Binds TCP Port 80 & Manages Workers', fill='#475569', font=font_node_sub)

    # Worker Process
    wx, wy, ww, wh = nx + 18, ny + 170, nw - 36, 118
    draw.rounded_rectangle([(wx, wy), (wx + ww, wy + wh)], radius=6, fill='#bbf7d0', outline='#15803d', width=2)
    draw.text((wx + 15, wy + 20), 'Nginx Worker Process (Event-Driven & Asynchronous Engine)', fill='#14532d', font=font_node_title)
    draw.text((wx + 15, wy + 42), 'User: www-data | Non-privileged | PID 1241 | Listening: 0.0.0.0:80', fill='#166534', font=font_node_sub)
    draw.text((wx + 15, wy + 64), '• Event Loop (epoll): Menerima dan memproses ribuan request secara non-blocking', fill='#334155', font=font_node_sub)
    draw.text((wx + 15, wy + 86), '• Zero-Copy sendfile(): Mengalirkan data biner web page langsung ke network socket', fill='#334155', font=font_node_sub)

    # Sub-Container Filesystem Storage
    fx, fy, fw, fh = cx2 + 22, cy2 + 375, cw2 - 44, 225
    draw.rounded_rectangle([(fx, fy), (fx + fw, fy + fh)], radius=8, fill='#f8fafc', outline='#64748b', width=1)
    # Header
    draw.rounded_rectangle([(fx, fy), (fx + fw, fy + 34)], radius=8, fill='#64748b')
    draw.rectangle([(fx, fy + 24), (fx + fw, fy + 34)], fill='#64748b')
    draw.text((fx + 15, fy + 17), 'Linux Storage: Web Document Root (/var/www/html/)', fill='#ffffff', font=font_node_title, anchor='lm')
    h5_icon = make_html5_icon(22)
    img.paste(h5_icon, (fx + fw - 34, fy + 6), h5_icon)

    # File Card
    dx, dy, dw, dh = fx + 18, fy + 45, fw - 36, 160
    draw.rounded_rectangle([(dx, dy), (dx + dw, dy + dh)], radius=6, fill='#ffffff', outline='#cbd5e1', width=1)
    draw.text((dx + 15, dy + 20), '📂 Direktori Proyek: /var/www/html/Portfolio-responsive/', fill='#0f172a', font=font_node_title)
    draw.text((dx + 15, dy + 42), 'Owner: root:root | Hak Akses File: 755 (rwxr-xr-x) | Format: UTF-8 Static Assets', fill='#475569', font=font_node_sub)

    # File items boxes
    files = [
        ("📄 index.html", "Dokumen HTML Utama", "#fef3c7", "#d97706"),
        ("🎨 css/style.css", "Aturan Desain & CSS", "#e0e7ff", "#4f46e5"),
        ("⚡ js/main.js", "Skrip Interaksi Klien", "#fef9c3", "#ca8a04"),
        ("🖼️ img/profile.jpg", "Aset Gambar & Media", "#e0f2fe", "#0284c7")
    ]
    box_w = (dw - 45) // 4
    for i, (fn, desc, bgc, stc) in enumerate(files):
        fbx = dx + 12 + i * (box_w + 7)
        fby = dy + 68
        draw.rounded_rectangle([(fbx, fby), (fbx + box_w, fby + 72)], radius=5, fill=bgc, outline=stc, width=1)
        draw.text((fbx + 8, fby + 20), fn, fill='#0f172a', font=font_edge)
        draw.text((fbx + 8, fby + 44), desc, fill='#475569', font=font_edge_sub)

    # ================= CONNECTORS & ARROWS =================
    # Clean channel between Container 1 (right=375) and Container 2 (left=490)
    # Channel width = 115px (x from 375 to 490). Center = 432.
    
    # 1. HTTP GET Request: Host Windows -> Nginx Worker
    req_y = wy + 35
    draw_arrow(draw, (cx1 + cw1, req_y), (wx, req_y), color='#2563eb', width=3)
    # Label badge 1 in middle channel
    draw.rounded_rectangle([(382, req_y - 24), (482, req_y + 4)], radius=5, fill='#2563eb')
    draw.text((432, req_y - 10), '1. HTTP GET', fill='#ffffff', font=font_edge, anchor='mm')
    draw.text((432, req_y + 14), 'Port 80 TCP', fill='#1e40af', font=font_edge_sub, anchor='mm')

    # 2. Master Supervises Worker
    draw_arrow(draw, (mx + mw // 2, my + mh), (wx + ww // 2, wy), color='#16a34a', width=2, dashed=True)
    draw.rounded_rectangle([(mx + mw // 2 - 125, my + mh + 5), (mx + mw // 2 + 125, my + mh + 27)], radius=4, fill='#ffffff', outline='#16a34a')
    draw.text((mx + mw // 2, my + mh + 16), '2. IPC Signal: Spawn & Monitor Worker', fill='#15803d', font=font_edge_sub, anchor='mm')

    # 3. Worker Reads Storage
    draw_arrow(draw, (wx + 130, wy + wh), (dx + 130, dy), color='#d97706', width=2)
    draw.rounded_rectangle([(wx + 40, wy + wh + 9), (wx + 220, wy + wh + 29)], radius=4, fill='#ffffff', outline='#d97706')
    draw.text((wx + 130, wy + wh + 19), '3. Read Disk File (sendfile)', fill='#b45309', font=font_edge_sub, anchor='mm')

    # 4. Storage returns Data Payload
    draw_arrow(draw, (dx + 480, dy), (wx + 480, wy + wh), color='#059669', width=2, dashed=True)
    draw.rounded_rectangle([(dx + 390, wy + wh + 9), (dx + 570, wy + wh + 29)], radius=4, fill='#ffffff', outline='#059669')
    draw.text((dx + 480, wy + wh + 19), '4. Data Stream Payload', fill='#047857', font=font_edge_sub, anchor='mm')

    # 5. HTTP Response: Nginx Worker -> Host Windows
    resp_y = wy + 82
    draw_arrow(draw, (wx, resp_y), (cx1 + cw1, resp_y), color='#16a34a', width=3)
    # Label badge 5 in middle channel
    draw.rounded_rectangle([(382, resp_y - 24), (482, resp_y + 4)], radius=5, fill='#16a34a')
    draw.text((432, resp_y - 10), '5. HTTP 200 OK', fill='#ffffff', font=font_edge, anchor='mm')
    draw.text((432, resp_y + 14), 'HTML/CSS/Assets', fill='#15803d', font=font_edge_sub, anchor='mm')

    output_path = 'assets/modul-07/00_arsitektur_webserver_nginx.png'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, quality=95)
    print(f'Rendered high-res diagram: {output_path}')

if __name__ == '__main__':
    generate_modul07_diagram()
