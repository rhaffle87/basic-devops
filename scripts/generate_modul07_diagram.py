import os
import math
import io
import fitz
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO_ROOT)

def load_svg_icon(path, size=38):
    doc = fitz.open(path)
    page = doc[0]
    scale = size / max(page.rect.width, page.rect.height)
    mat = fitz.Matrix(scale, scale)
    pix = page.get_pixmap(matrix=mat, alpha=True)
    img = Image.open(io.BytesIO(pix.tobytes('png')))
    res = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    x = (size - img.width) // 2
    y = (size - img.height) // 2
    res.paste(img, (x, y), img)
    return res

def draw_pill_card(img, draw, x, y, w, h, icon, title, subtitle, stroke_color, bg_color='#ffffff'):
    # Subtle ambient drop shadow
    draw.rounded_rectangle([(x, y + 2), (x + w, y + h + 2)], radius=12, fill='#f1f5f9')
    # Card background and colored border stroke
    draw.rounded_rectangle([(x, y), (x + w, y + h)], radius=12, fill=bg_color, outline=stroke_color, width=2)
    # Paste icon
    if icon:
        img.paste(icon, (x + 16, y + (h - icon.height) // 2), icon)
    # Card text
    f_title = ImageFont.truetype('arialbd.ttf', 13)
    f_sub = ImageFont.truetype('arial.ttf', 11)
    draw.text((x + 66, y + 20), title, fill='#0f172a', font=f_title)
    draw.text((x + 66, y + 42), subtitle, fill='#64748b', font=f_sub)

def draw_arrow(draw, points, color='#2563eb', width=2, dashed=False, arrow_at_end=True):
    width = int(width)
    for i in range(len(points) - 1):
        p1 = points[i]
        p2 = points[i+1]
        x1, y1 = p1
        x2, y2 = p2
        if not dashed:
            draw.line([p1, p2], fill=color, width=width)
        else:
            dist = math.hypot(x2 - x1, y2 - y1)
            segments = max(1, int(dist // 8))
            for s in range(segments):
                if s % 2 == 0:
                    sx = x1 + (x2 - x1) * (s / segments)
                    sy = y1 + (y2 - y1) * (s / segments)
                    ex = x1 + (x2 - x1) * ((s + 1) / segments)
                    ey = y1 + (y2 - y1) * ((s + 1) / segments)
                    draw.line([(sx, sy), (ex, ey)], fill=color, width=width)
    
    if arrow_at_end and len(points) >= 2:
        x1, y1 = points[-2]
        x2, y2 = points[-1]
        angle = math.atan2(y2 - y1, x2 - x1)
        arrow_len = 9
        head_angle = math.pi / 6
        pa = (x2 - arrow_len * math.cos(angle - head_angle), y2 - arrow_len * math.sin(angle - head_angle))
        pb = (x2 - arrow_len * math.cos(angle + head_angle), y2 - arrow_len * math.sin(angle + head_angle))
        draw.polygon([points[-1], pa, pb], fill=color)

def draw_edge_badge(draw, cx, cy, text, color='#0f172a'):
    f = ImageFont.truetype('arialbd.ttf', 10)
    bbox = f.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad_x = 8
    pad_y = 5
    bx1 = cx - tw // 2 - pad_x
    by1 = cy - th // 2 - pad_y
    bx2 = cx + tw // 2 + pad_x
    by2 = cy + th // 2 + pad_y
    draw.rounded_rectangle([(bx1, by1), (bx2, by2)], radius=4, fill='#ffffff', outline='#cbd5e1', width=1)
    draw.text((cx, cy), text, fill=color, font=f, anchor='mm')

def generate_modul07_diagram():
    w, h = 1160, 920
    img = Image.new('RGB', (w, h), color='#ffffff')
    draw = ImageDraw.Draw(img)

    # Title Header (Clean & Minimalist)
    font_header = ImageFont.truetype('arialbd.ttf', 16)
    font_sub = ImageFont.truetype('arial.ttf', 11)
    draw.text((w // 2, 28), 'Arsitektur Web Server Nginx & Siklus Komunikasi HTTP (Modul 7)', fill='#0f172a', font=font_header, anchor='mm')
    draw.text((w // 2, 50), 'Production Architecture with Official Service Components & Lightweight Isolation', fill='#64748b', font=font_sub, anchor='mm')

    # Load authentic colored logos
    icon_chrome = load_svg_icon('assets/logos/chrome.svg', 38)
    icon_curl = load_svg_icon('assets/logos/bash.svg', 38)
    icon_win = load_svg_icon('assets/logos/windows.svg', 38)
    icon_ubuntu = load_svg_icon('assets/logos/ubuntu.svg', 22)
    icon_linux = load_svg_icon('assets/logos/linux.svg', 22)
    icon_nginx = load_svg_icon('assets/logos/nginx.svg', 38)
    icon_html5 = load_svg_icon('assets/logos/html5.svg', 38)
    icon_terminal = load_svg_icon('assets/logos/terminal.svg', 36)
    icon_settings = load_svg_icon('assets/logos/settings.svg', 34)

    # ================= ROW 1: CLIENT LAYER =================
    # Card 1: Google Chrome
    c1_x, c1_y, c1_w, c1_h = 310, 85, 240, 72
    draw_pill_card(img, draw, c1_x, c1_y, c1_w, c1_h, icon_chrome, 'Google Chrome', 'Host Web Browser (Port 80)', '#2563eb')

    # Card 2: Terminal / cURL Client
    c2_x, c2_y, c2_w, c2_h = 610, 85, 240, 72
    draw_pill_card(img, draw, c2_x, c2_y, c2_w, c2_h, icon_curl, 'Terminal / curl', 'HTTP CLI Test Client', '#0284c7')

    # ================= ROW 2: HOST OS GATEWAY =================
    # Card 3: Windows 10/11 Winsock
    c3_x, c3_y, c3_w, c3_h = 460, 210, 240, 72
    draw_pill_card(img, draw, c3_x, c3_y, c3_w, c3_h, icon_win, 'Windows 10/11 OS', 'Winsock TCP Stack (127.0.0.1)', '#0078d7')

    # ================= ROW 3: WSL2 CONTAINER =================
    cnt_x, cnt_y, cnt_w, cnt_h = 130, 330, 900, 540
    draw.rounded_rectangle([(cnt_x, cnt_y), (cnt_x + cnt_w, cnt_y + cnt_h)], radius=8, fill='#f8fafc', outline='#334155', width=2)
    
    # Header bar
    draw.rounded_rectangle([(cnt_x, cnt_y), (cnt_x + cnt_w, cnt_y + 36)], radius=8, fill='#1e293b')
    draw.rectangle([(cnt_x, cnt_y + 24), (cnt_x + cnt_w, cnt_y + 36)], fill='#1e293b')
    
    font_cnt_title = ImageFont.truetype('arialbd.ttf', 12)
    draw.text((cnt_x + 25, cnt_y + 18), 'Windows Subsystem for Linux (WSL2) — Ubuntu 22.04 LTS Environment', fill='#ffffff', font=font_cnt_title, anchor='lm')
    
    # Official OS logos in header bar (Right aligned)
    img.paste(icon_ubuntu, (cnt_x + cnt_w - 60, cnt_y + 7), icon_ubuntu)
    img.paste(icon_linux, (cnt_x + cnt_w - 32, cnt_y + 7), icon_linux)

    # Inside Container - Row 3.1: Nginx Master
    cm_x, cm_y, cm_w, cm_h = 460, 400, 240, 72
    draw_pill_card(img, draw, cm_x, cm_y, cm_w, cm_h, icon_nginx, 'Nginx Master', 'Privileged Daemon • Root PID 1240', '#059669')

    # Inside Container - Row 3.2: Nginx Worker
    cw_x, cw_y, cw_w, cw_h = 460, 530, 240, 72
    draw_pill_card(img, draw, cw_x, cw_y, cw_w, cw_h, icon_nginx, 'Nginx Worker', 'epoll Event Loop • www-data', '#10b981')

    # Inside Container - Row 3.3: Sub-Services (Config, Storage, Logs)
    cv_x, cv_y, cv_w, cv_h = 170, 680, 240, 72
    draw_pill_card(img, draw, cv_x, cv_y, cv_w, cv_h, icon_settings, 'Virtual Host Config', '/etc/nginx/sites-available', '#8b5cf6')

    cs_x, cs_y, cs_w, cs_h = 460, 680, 240, 72
    draw_pill_card(img, draw, cs_x, cs_y, cs_w, cs_h, icon_html5, 'Document Root (HTML5)', '/var/www/html/Portfolio', '#ea580c')

    cl_x, cl_y, cl_w, cl_h = 750, 680, 240, 72
    draw_pill_card(img, draw, cl_x, cl_y, cl_w, cl_h, icon_terminal, 'Access & Error Logs', '/var/log/nginx/access.log', '#64748b')

    # ================= CONNECTORS & EDGES =================
    # 1. Chrome -> Winsock
    p1_chrome = (c1_x + c1_w // 2, c1_y + c1_h)
    p1_sock = (c3_x + c3_w // 4, c3_y)
    draw_arrow(draw, [p1_chrome, (p1_chrome[0], 182), (p1_sock[0], 182), p1_sock], color='#2563eb', width=2)
    draw_edge_badge(draw, p1_chrome[0], 182, 'HTTP GET', color='#1d4ed8')

    # 2. Curl -> Winsock
    p2_curl = (c2_x + c2_w // 2, c2_y + c2_h)
    p2_sock = (c3_x + c3_w * 3 // 4, c3_y)
    draw_arrow(draw, [p2_curl, (p2_curl[0], 182), (p2_sock[0], 182), p2_sock], color='#0284c7', width=2)
    draw_edge_badge(draw, p2_curl[0], 182, 'CLI GET', color='#0369a1')

    # 3. Winsock -> Nginx Master (Direct Vertical Down Spine at X=580)
    spine_x = c3_x + c3_w // 2
    draw_arrow(draw, [(spine_x, c3_y + c3_h), (spine_x, cm_y)], color='#0078d7', width=2)
    draw_edge_badge(draw, spine_x, 308, 'Port 80 TCP', color='#0284c7')

    # 4. Master -> Worker (Direct Vertical Down Spine at X=580)
    draw_arrow(draw, [(spine_x, cm_y + cm_h), (spine_x, cw_y)], color='#059669', width=2)
    draw_edge_badge(draw, spine_x, (cm_y + cm_h + cw_y) // 2, 'IPC Spawn', color='#047857')

    # 5. Master -> Virtual Host Config (Orthogonal Purple Dashed)
    p_master_left = (cm_x, cm_y + cm_h // 2)
    p_vhost_top = (cv_x + cv_w // 2, cv_y)
    draw_arrow(draw, [p_master_left, (p_vhost_top[0], p_master_left[1]), p_vhost_top], color='#8b5cf6', width=2, dashed=True)
    draw_edge_badge(draw, p_vhost_top[0], p_master_left[1], 'Read Config', color='#7c3aed')

    # 6. Worker -> Document Root Storage (Direct Vertical Down Spine at X=580)
    draw_arrow(draw, [(spine_x, cw_y + cw_h), (spine_x, cs_y)], color='#ea580c', width=2)
    draw_edge_badge(draw, spine_x, (cw_y + cw_h + cs_y) // 2, 'sendfile()', color='#c2410c')

    # 7. Worker -> Access Logs (Orthogonal Slate Dashed)
    p_worker_right = (cw_x + cw_w, cw_y + cw_h // 2)
    p_logs_top = (cl_x + cl_w // 2, cl_y)
    draw_arrow(draw, [p_worker_right, (p_logs_top[0], p_worker_right[1]), p_logs_top], color='#64748b', width=2, dashed=True)
    draw_edge_badge(draw, p_logs_top[0], p_worker_right[1], 'Write Log', color='#475569')

    # 8. Worker -> Chrome (HTTP 200 OK Response via Outer Left Channel)
    p_worker_left = (cw_x, cw_y + cw_h // 2)
    draw_arrow(draw, [
        p_worker_left,
        (60, p_worker_left[1]),
        (60, c1_y + c1_h // 2),
        (c1_x, c1_y + c1_h // 2)
    ], color='#10b981', width=2)
    draw_edge_badge(draw, 60, (p_worker_left[1] + c1_y + c1_h // 2) // 2, 'HTTP 200 OK', color='#047857')

    output_path = 'assets/modul-07/00_arsitektur_webserver_nginx.png'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, quality=95)
    print(f'Rendered modern light-theme service diagram: {output_path}')

if __name__ == '__main__':
    generate_modul07_diagram()
