import os
import urllib.parse
import base64
import zlib
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO_ROOT)

def trim_image(im, padding=35):
    bg = Image.new(im.mode, im.size, (255, 255, 255))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        w, h = im.size
        x1 = max(0, bbox[0] - padding)
        y1 = max(0, bbox[1] - padding)
        x2 = min(w, bbox[2] + padding)
        y2 = min(h, bbox[3] + padding)
        return im.crop((x1, y1, x2, y2))
    return im

def export_drawio(xml_content, drawio_path, png_path, svg_path=None, viewport=(1600, 1000)):
    # 1. Save drawio XML
    os.makedirs(os.path.dirname(drawio_path), exist_ok=True)
    os.makedirs(os.path.dirname(png_path), exist_ok=True)
    if svg_path:
        os.makedirs(os.path.dirname(svg_path), exist_ok=True)
        
    with open(drawio_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    print(f"[1/3] Saved Draw.io XML: {drawio_path}")

    # 2. Render via Playwright
    encoded = urllib.parse.quote(xml_content)
    compressed = zlib.compress(encoded.encode('utf-8'))[2:-4]
    b64 = base64.b64encode(compressed).decode('utf-8')
    url = f"https://viewer.diagrams.net/?highlight=none&edit=0&layers=0&nav=0&page-id=0#R{b64}"

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': viewport[0], 'height': viewport[1]}, device_scale_factor=2)
        page.goto(url, wait_until='networkidle', timeout=25000)
        page.wait_for_timeout(3000)
        
        if svg_path:
            svg_content = page.eval_on_selector('svg', 'el => el.outerHTML')
            with open(svg_path, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            print(f"[2/3] Exported SVG: {svg_path}")
            
        page.screenshot(path=png_path)
        browser.close()

    # 3. Trim PNG margins
    im = Image.open(png_path).convert('RGB')
    trimmed = trim_image(im)
    trimmed.save(png_path)
    print(f"[3/3] Exported Trimmed PNG: {png_path} ({trimmed.size[0]}x{trimmed.size[1]})\n")

# ==============================================================================
# 1. MODUL 07 - NGINX WEB SERVER ARCHITECTURE & HTTP REQUEST LIFECYCLE
# ==============================================================================
xml_modul_07 = """<mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1300" pageHeight="700" background="#ffffff">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>

    <mxCell id="c_client" value="&lt;b&gt;Client &amp; Ingestion Environment (Host Windows)&lt;/b&gt;" style="swimlane;startSize=28;fillColor=#f8fafc;strokeColor=#cbd5e1;fontColor=#0f172a;fontStyle=1;fontSize=12;rounded=1;html=1;" vertex="1" parent="1">
      <mxGeometry x="40" y="40" width="240" height="540" as="geometry"/>
    </mxCell>
    <mxCell id="node_browser" value="&lt;b&gt;Google Chrome / Edge&lt;/b&gt;&lt;br&gt;User Agent Client" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#0284c7;strokeColor=#0369a1;fontColor=#ffffff;fontSize=12;fontFamily=Helvetica;" vertex="1" parent="c_client">
      <mxGeometry x="25" y="70" width="190" height="70" as="geometry"/>
    </mxCell>
    <mxCell id="node_http_req" value="&lt;b&gt;HTTP Request Payload&lt;/b&gt;&lt;br&gt;GET /index.html HTTP/1.1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f1f5f9;strokeColor=#94a3b8;fontColor=#334155;fontSize=11;fontFamily=Helvetica;" vertex="1" parent="c_client">
      <mxGeometry x="25" y="210" width="190" height="60" as="geometry"/>
    </mxCell>
    <mxCell id="node_browser_render" value="&lt;b&gt;DOM Render Engine&lt;/b&gt;&lt;br&gt;HTML5 / CSS Portfolio Display" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#10b981;strokeColor=#059669;fontColor=#ffffff;fontSize=12;fontFamily=Helvetica;" vertex="1" parent="c_client">
      <mxGeometry x="25" y="390" width="190" height="70" as="geometry"/>
    </mxCell>

    <mxCell id="c_nginx" value="&lt;b&gt;Nginx Web Server Core (WSL2 Ubuntu Daemon)&lt;/b&gt;" style="swimlane;startSize=28;fillColor=#f0fdf4;strokeColor=#86efac;fontColor=#065f46;fontStyle=1;fontSize=12;rounded=1;html=1;" vertex="1" parent="1">
      <mxGeometry x="320" y="40" width="560" height="540" as="geometry"/>
    </mxCell>
    <mxCell id="node_master" value="&lt;b&gt;Nginx Master Process&lt;/b&gt;&lt;br&gt;PID Controller &amp;amp; Config Manager" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#15803d;strokeColor=#166534;fontColor=#ffffff;fontSize=12;fontFamily=Helvetica;" vertex="1" parent="c_nginx">
      <mxGeometry x="40" y="60" width="230" height="75" as="geometry"/>
    </mxCell>
    <mxCell id="node_config" value="&lt;b&gt;/etc/nginx/sites-available/default&lt;/b&gt;&lt;br&gt;Virtual Host Server Block (:80)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ecfdf5;strokeColor=#a7f3d0;fontColor=#065f46;fontSize=11;fontFamily=Helvetica;" vertex="1" parent="c_nginx">
      <mxGeometry x="310" y="60" width="210" height="75" as="geometry"/>
    </mxCell>
    <mxCell id="node_socket" value="&lt;b&gt;TCP Socket Listener&lt;/b&gt;&lt;br&gt;0.0.0.0:80 (Non-blocking Socket)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dbeafe;strokeColor=#93c5fd;fontColor=#1e3a8a;fontSize=11;fontFamily=Helvetica;" vertex="1" parent="c_nginx">
      <mxGeometry x="40" y="200" width="230" height="60" as="geometry"/>
    </mxCell>
    <mxCell id="node_worker" value="&lt;b&gt;Nginx Worker Process&lt;/b&gt;&lt;br&gt;Event-Driven Loop (epoll / kqueue)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#059669;strokeColor=#047857;fontColor=#ffffff;fontSize=12;fontFamily=Helvetica;" vertex="1" parent="c_nginx">
      <mxGeometry x="40" y="320" width="230" height="75" as="geometry"/>
    </mxCell>
    <mxCell id="node_vhost_router" value="&lt;b&gt;Location / Router&lt;/b&gt;&lt;br&gt;try_files $uri $uri/ =404" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ecfdf5;strokeColor=#a7f3d0;fontColor=#065f46;fontSize=11;fontFamily=Helvetica;" vertex="1" parent="c_nginx">
      <mxGeometry x="310" y="320" width="210" height="75" as="geometry"/>
    </mxCell>
    <mxCell id="node_resp_formatter" value="&lt;b&gt;HTTP Response Formatter&lt;/b&gt;&lt;br&gt;Header: Content-Type: text/html" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dcfce7;strokeColor=#86efac;fontColor=#14532d;fontSize=11;fontFamily=Helvetica;" vertex="1" parent="c_nginx">
      <mxGeometry x="40" y="445" width="480" height="55" as="geometry"/>
    </mxCell>

    <mxCell id="c_storage" value="&lt;b&gt;Persistence / Filesystem Tier&lt;/b&gt;" style="swimlane;startSize=28;fillColor=#fefce8;strokeColor=#fef08a;fontColor=#713f12;fontStyle=1;fontSize=12;rounded=1;html=1;" vertex="1" parent="1">
      <mxGeometry x="920" y="40" width="320" height="540" as="geometry"/>
    </mxCell>
    <mxCell id="node_doc_root" value="&lt;b&gt;Document Root Directory&lt;/b&gt;&lt;br&gt;/var/www/html/Portfolio-responsive" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#eab308;strokeColor=#ca8a04;fontColor=#ffffff;fontSize=12;fontFamily=Helvetica;" vertex="1" parent="c_storage">
      <mxGeometry x="30" y="180" width="260" height="70" as="geometry"/>
    </mxCell>
    <mxCell id="node_files" value="&lt;b&gt;Static Assets Storage&lt;/b&gt;&lt;br&gt;index.html, style.css, assets/*.png" style="shape=cylinder3;whiteSpace=wrap;html=1;fillColor=#fef9c3;strokeColor=#fde047;fontColor=#713f12;fontSize=11;fontFamily=Helvetica;" vertex="1" parent="c_storage">
      <mxGeometry x="60" y="310" width="200" height="90" as="geometry"/>
    </mxCell>

    <mxCell id="e_1" edge="1" parent="1" source="node_browser" target="node_http_req" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=2;strokeColor=#0284c7;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_2" edge="1" parent="1" source="node_http_req" target="node_socket" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=2;strokeColor=#0284c7;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_master_sig" edge="1" parent="1" source="node_master" target="node_worker" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;dashed=1;strokeWidth=2;strokeColor=#15803d;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_master_cfg" edge="1" parent="1" source="node_master" target="node_config" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=2;strokeColor=#15803d;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_socket_worker" edge="1" parent="1" source="node_socket" target="node_worker" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=2;strokeColor=#059669;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_worker_router" edge="1" parent="1" source="node_worker" target="node_vhost_router" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=2;strokeColor=#059669;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_router_root" edge="1" parent="1" source="node_vhost_router" target="node_doc_root" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=2;strokeColor=#059669;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_root_files" edge="1" parent="1" source="node_doc_root" target="node_files" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=2;strokeColor=#ca8a04;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_files_fmt" edge="1" parent="1" source="node_files" target="node_resp_formatter" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=2;strokeColor=#059669;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_fmt_browser" edge="1" parent="1" source="node_resp_formatter" target="node_browser_render" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=3;strokeColor=#10b981;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
  </root>
</mxGraphModel>"""

# ==============================================================================
# 2. MODUL 08 - GIT & SHELL SCRIPTING AUTOMATED DEPLOYMENT PIPELINE
# ==============================================================================
xml_modul_08 = """<mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1350" pageHeight="720" background="#ffffff">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>

    <mxCell id="c_vc" value="&lt;b&gt;Version Control &amp;amp; Release Source&lt;/b&gt;" style="swimlane;startSize=28;fillColor=#f8fafc;strokeColor=#cbd5e1;fontColor=#0f172a;fontStyle=1;fontSize=12;rounded=1;html=1;" vertex="1" parent="1">
      <mxGeometry x="40" y="40" width="250" height="580" as="geometry"/>
    </mxCell>
    <mxCell id="n_dev" value="&lt;b&gt;Developer Workspace&lt;/b&gt;&lt;br&gt;Ubuntu WSL2 CLI" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#3b82f6;strokeColor=#2563eb;fontColor=#ffffff;fontSize=12;fontFamily=Helvetica;" vertex="1" parent="c_vc">
      <mxGeometry x="25" y="70" width="200" height="65" as="geometry"/>
    </mxCell>
    <mxCell id="n_commit" value="&lt;b&gt;Git Snapshot (HEAD)&lt;/b&gt;&lt;br&gt;git commit -m &#39;release: v2.0&#39;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f1f5f9;strokeColor=#94a3b8;fontColor=#334155;fontSize=11;fontFamily=Helvetica;" vertex="1" parent="c_vc">
      <mxGeometry x="25" y="210" width="200" height="65" as="geometry"/>
    </mxCell>
    <mxCell id="n_rev" value="&lt;b&gt;git rev-parse --short HEAD&lt;/b&gt;&lt;br&gt;Release Artifact Metadata" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e2e8f0;strokeColor=#64748b;fontColor=#0f172a;fontSize=11;fontFamily=Helvetica;" vertex="1" parent="c_vc">
      <mxGeometry x="25" y="420" width="200" height="65" as="geometry"/>
    </mxCell>

    <mxCell id="c_engine" value="&lt;b&gt;Defensive Shell Scripting Engine (deploy.sh)&lt;/b&gt;" style="swimlane;startSize=28;fillColor=#f0fdf4;strokeColor=#86efac;fontColor=#065f46;fontStyle=1;fontSize=12;rounded=1;html=1;" vertex="1" parent="1">
      <mxGeometry x="330" y="40" width="620" height="580" as="geometry"/>
    </mxCell>
    <mxCell id="n_flags" value="&lt;b&gt;Safety Guards Initializer&lt;/b&gt;&lt;br&gt;set -eo pipefail (Fail-Fast Policy)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#16a34a;strokeColor=#15803d;fontColor=#ffffff;fontSize=12;fontFamily=Helvetica;" vertex="1" parent="c_engine">
      <mxGeometry x="40" y="60" width="240" height="65" as="geometry"/>
    </mxCell>
    <mxCell id="n_chk_integrity" value="&lt;b&gt;1. Pre-Flight File Check&lt;/b&gt;&lt;br&gt;test -f index.html (Abort on Fail)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dcfce7;strokeColor=#86efac;fontColor=#166534;fontSize=11;fontFamily=Helvetica;" vertex="1" parent="c_engine">
      <mxGeometry x="40" y="170" width="240" height="60" as="geometry"/>
    </mxCell>
    <mxCell id="n_chk_perm" value="&lt;b&gt;2. Permission Harmonization&lt;/b&gt;&lt;br&gt;chmod 644 (Allow www-data Read)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dcfce7;strokeColor=#86efac;fontColor=#166534;fontSize=11;fontFamily=Helvetica;" vertex="1" parent="c_engine">
      <mxGeometry x="340" y="170" width="240" height="60" as="geometry"/>
    </mxCell>
    <mxCell id="n_chk_syntax" value="&lt;b&gt;3. Nginx Syntax Probe&lt;/b&gt;&lt;br&gt;sudo nginx -t (Atomic Validation)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dcfce7;strokeColor=#86efac;fontColor=#166534;fontSize=11;fontFamily=Helvetica;" vertex="1" parent="c_engine">
      <mxGeometry x="40" y="280" width="240" height="60" as="geometry"/>
    </mxCell>
    <mxCell id="n_reload" value="&lt;b&gt;4. Zero-Downtime Reload&lt;/b&gt;&lt;br&gt;sudo systemctl reload nginx" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#22c55e;strokeColor=#16a34a;fontColor=#ffffff;fontSize=12;fontFamily=Helvetica;" vertex="1" parent="c_engine">
      <mxGeometry x="340" y="280" width="240" height="60" as="geometry"/>
    </mxCell>
    <mxCell id="n_health" value="&lt;b&gt;5. Automated HTTP Health Probe&lt;/b&gt;&lt;br&gt;curl -s -o /dev/null -w &#39;%{http_code}&#39; :80" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#0284c7;strokeColor=#0369a1;fontColor=#ffffff;fontSize=12;fontFamily=Helvetica;" vertex="1" parent="c_engine">
      <mxGeometry x="40" y="390" width="540" height="60" as="geometry"/>
    </mxCell>
    <mxCell id="n_decision" value="&lt;b&gt;HTTP == 200 OK?&lt;/b&gt;" style="rhombus;whiteSpace=wrap;html=1;fillColor=#fef08a;strokeColor=#eab308;fontColor=#854d0e;fontSize=12;fontStyle=1;" vertex="1" parent="c_engine">
      <mxGeometry x="220" y="480" width="180" height="80" as="geometry"/>
    </mxCell>

    <mxCell id="c_obs" value="&lt;b&gt;Runtime Observability Tier&lt;/b&gt;" style="swimlane;startSize=28;fillColor=#fefce8;strokeColor=#fef08a;fontColor=#713f12;fontStyle=1;fontSize=12;rounded=1;html=1;" vertex="1" parent="1">
      <mxGeometry x="990" y="40" width="320" height="580" as="geometry"/>
    </mxCell>
    <mxCell id="n_audit" value="&lt;b&gt;deployment.log&lt;/b&gt;&lt;br&gt;Audit Trail Timestamp &amp;amp; SHA" style="shape=cylinder3;whiteSpace=wrap;html=1;fillColor=#fef9c3;strokeColor=#fde047;fontColor=#713f12;fontSize=11;fontFamily=Helvetica;" vertex="1" parent="c_obs">
      <mxGeometry x="50" y="160" width="220" height="90" as="geometry"/>
    </mxCell>
    <mxCell id="n_alert" value="&lt;b&gt;Rollback &amp;amp; Alerting&lt;/b&gt;&lt;br&gt;Exit Code 1 (Abort Deployment)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fee2e2;strokeColor=#ef4444;fontColor=#991b1b;fontSize=12;fontFamily=Helvetica;" vertex="1" parent="c_obs">
      <mxGeometry x="50" y="485" width="220" height="70" as="geometry"/>
    </mxCell>

    <mxCell id="e_dev_commit" edge="1" parent="1" source="n_dev" target="n_commit" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=2;strokeColor=#3b82f6;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_commit_engine" edge="1" parent="1" source="n_commit" target="n_flags" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=2;strokeColor=#16a34a;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_flags_int" edge="1" parent="1" source="n_flags" target="n_chk_integrity" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=2;strokeColor=#16a34a;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_int_perm" edge="1" parent="1" source="n_chk_integrity" target="n_chk_perm" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=2;strokeColor=#16a34a;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_perm_syntax" edge="1" parent="1" source="n_chk_perm" target="n_chk_syntax" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=2;strokeColor=#16a34a;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_syntax_reload" edge="1" parent="1" source="n_chk_syntax" target="n_reload" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=2;strokeColor=#16a34a;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_reload_health" edge="1" parent="1" source="n_reload" target="n_health" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=2;strokeColor=#0284c7;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_health_dec" edge="1" parent="1" source="n_health" target="n_decision" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=2;strokeColor=#0284c7;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_dec_yes" edge="1" parent="1" source="n_decision" target="n_audit" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=3;strokeColor=#16a34a;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_dec_no" edge="1" parent="1" source="n_decision" target="n_alert" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;dashed=1;strokeWidth=2;strokeColor=#ef4444;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_rev_audit" edge="1" parent="1" source="n_rev" target="n_audit" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;dashed=1;strokeWidth=2;strokeColor=#64748b;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
  </root>
</mxGraphModel>"""

# ==============================================================================
# 3. MODUL 09 - VIRTUAL MACHINE VS DOCKER CONTAINER ARCHITECTURE
# ==============================================================================
xml_modul_09 = """<mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1350" pageHeight="720" background="#ffffff">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>

    <mxCell id="c_vm" value="&lt;b&gt;Traditional Virtual Machine Architecture (Type-2 Hypervisor)&lt;/b&gt;" style="swimlane;startSize=28;fillColor=#f8fafc;strokeColor=#cbd5e1;fontColor=#334155;fontStyle=1;fontSize=12;rounded=1;html=1;" vertex="1" parent="1">
      <mxGeometry x="40" y="40" width="580" height="580" as="geometry"/>
    </mxCell>
    <mxCell id="vm_app1" value="&lt;b&gt;App A&lt;/b&gt;&lt;br&gt;Port 80" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fed7aa;strokeColor=#f97316;fontColor=#9a3412;fontSize=12;fontFamily=Helvetica;" vertex="1" parent="c_vm">
      <mxGeometry x="40" y="60" width="220" height="60" as="geometry"/>
    </mxCell>
    <mxCell id="vm_app2" value="&lt;b&gt;App B&lt;/b&gt;&lt;br&gt;Port 8080" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fed7aa;strokeColor=#f97316;fontColor=#9a3412;fontSize=12;fontFamily=Helvetica;" vertex="1" parent="c_vm">
      <mxGeometry x="320" y="60" width="220" height="60" as="geometry"/>
    </mxCell>
    <mxCell id="vm_bins1" value="&lt;b&gt;Bins &amp;amp; Libs A&lt;/b&gt;&lt;br&gt;Full OS Libraries" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffedd5;strokeColor=#fdba74;fontColor=#c2410c;fontSize=11;fontFamily=Helvetica;" vertex="1" parent="c_vm">
      <mxGeometry x="40" y="140" width="220" height="50" as="geometry"/>
    </mxCell>
    <mxCell id="vm_bins2" value="&lt;b&gt;Bins &amp;amp; Libs B&lt;/b&gt;&lt;br&gt;Full OS Libraries" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffedd5;strokeColor=#fdba74;fontColor=#c2410c;fontSize=11;fontFamily=Helvetica;" vertex="1" parent="c_vm">
      <mxGeometry x="320" y="140" width="220" height="50" as="geometry"/>
    </mxCell>
    <mxCell id="vm_guest1" value="&lt;b&gt;Guest OS 1 (Ubuntu / Windows)&lt;/b&gt;&lt;br&gt;Dedicated Kernel &amp;amp; RAM (Heavyweight ~2-20 GB)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fee2e2;strokeColor=#ef4444;fontColor=#991b1b;fontSize=11;fontFamily=Helvetica;" vertex="1" parent="c_vm">
      <mxGeometry x="40" y="210" width="220" height="70" as="geometry"/>
    </mxCell>
    <mxCell id="vm_guest2" value="&lt;b&gt;Guest OS 2 (Debian / CentOS)&lt;/b&gt;&lt;br&gt;Dedicated Kernel &amp;amp; RAM (Heavyweight ~2-20 GB)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fee2e2;strokeColor=#ef4444;fontColor=#991b1b;fontSize=11;fontFamily=Helvetica;" vertex="1" parent="c_vm">
      <mxGeometry x="320" y="210" width="220" height="70" as="geometry"/>
    </mxCell>
    <mxCell id="vm_hypervisor" value="&lt;b&gt;Hypervisor (VirtualBox / VMware / KVM)&lt;/b&gt;&lt;br&gt;Hardware Virtualization Layer" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e2e8f0;strokeColor=#94a3b8;fontColor=#1e293b;fontSize=12;fontFamily=Helvetica;" vertex="1" parent="c_vm">
      <mxGeometry x="40" y="310" width="500" height="60" as="geometry"/>
    </mxCell>
    <mxCell id="vm_host_os" value="&lt;b&gt;Host Operating System&lt;/b&gt;&lt;br&gt;Windows 11 / macOS / Linux" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f1f5f9;strokeColor=#cbd5e1;fontColor=#334155;fontSize=12;fontFamily=Helvetica;" vertex="1" parent="c_vm">
      <mxGeometry x="40" y="395" width="500" height="60" as="geometry"/>
    </mxCell>
    <mxCell id="vm_infra" value="&lt;b&gt;Physical Infrastructure (Server Hardware)&lt;/b&gt;&lt;br&gt;CPU, RAM, Storage (SSD/NVMe), Network Cards" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#0f172a;strokeColor=#020617;fontColor=#ffffff;fontSize=12;fontFamily=Helvetica;" vertex="1" parent="c_vm">
      <mxGeometry x="40" y="480" width="500" height="60" as="geometry"/>
    </mxCell>

    <mxCell id="c_docker" value="&lt;b&gt;Modern Docker Containerization (Shared Kernel Engine)&lt;/b&gt;" style="swimlane;startSize=28;fillColor=#f0fdf4;strokeColor=#86efac;fontColor=#065f46;fontStyle=1;fontSize=12;rounded=1;html=1;" vertex="1" parent="1">
      <mxGeometry x="680" y="40" width="620" height="580" as="geometry"/>
    </mxCell>
    <mxCell id="doc_app1" value="&lt;b&gt;Container A: Web App&lt;/b&gt;&lt;br&gt;Nginx Alpine (:80)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#38bdf8;strokeColor=#0284c7;fontColor=#0f172a;fontSize=12;fontFamily=Helvetica;" vertex="1" parent="c_docker">
      <mxGeometry x="40" y="60" width="240" height="60" as="geometry"/>
    </mxCell>
    <mxCell id="doc_app2" value="&lt;b&gt;Container B: API App&lt;/b&gt;&lt;br&gt;Node.js / Python (:3000)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#38bdf8;strokeColor=#0284c7;fontColor=#0f172a;fontSize=12;fontFamily=Helvetica;" vertex="1" parent="c_docker">
      <mxGeometry x="340" y="60" width="240" height="60" as="geometry"/>
    </mxCell>
    <mxCell id="doc_bins1" value="&lt;b&gt;Minimal Bin/Libs A&lt;/b&gt;&lt;br&gt;Alpine Base Layer (~5 MB)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e0f2fe;strokeColor=#bae6fd;fontColor=#0369a1;fontSize=11;fontFamily=Helvetica;" vertex="1" parent="c_docker">
      <mxGeometry x="40" y="140" width="240" height="50" as="geometry"/>
    </mxCell>
    <mxCell id="doc_bins2" value="&lt;b&gt;Minimal Bin/Libs B&lt;/b&gt;&lt;br&gt;Alpine Base Layer (~5 MB)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e0f2fe;strokeColor=#bae6fd;fontColor=#0369a1;fontSize=11;fontFamily=Helvetica;" vertex="1" parent="c_docker">
      <mxGeometry x="340" y="140" width="240" height="50" as="geometry"/>
    </mxCell>
    <mxCell id="doc_engine" value="&lt;b&gt;Docker Engine (containerd / runc)&lt;/b&gt;&lt;br&gt;Namespaces (PID, NET, MNT, IPC) &amp;amp; Cgroups Isolation" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#0284c7;strokeColor=#0369a1;fontColor=#ffffff;fontSize=12;fontFamily=Helvetica;" vertex="1" parent="c_docker">
      <mxGeometry x="40" y="215" width="540" height="65" as="geometry"/>
    </mxCell>
    <mxCell id="doc_kernel" value="&lt;b&gt;Host Operating System &amp;amp; Shared Linux Kernel&lt;/b&gt;&lt;br&gt;WSL2 Ubuntu Kernel (Direct Kernel Sharing without Hypervisor Overhead)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#10b981;strokeColor=#059669;fontColor=#ffffff;fontSize=12;fontFamily=Helvetica;" vertex="1" parent="c_docker">
      <mxGeometry x="40" y="325" width="540" height="70" as="geometry"/>
    </mxCell>
    <mxCell id="doc_infra" value="&lt;b&gt;Physical Infrastructure (Server Hardware)&lt;/b&gt;&lt;br&gt;CPU, RAM, Storage (SSD/NVMe), Network Cards" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#0f172a;strokeColor=#020617;fontColor=#ffffff;fontSize=12;fontFamily=Helvetica;" vertex="1" parent="c_docker">
      <mxGeometry x="40" y="480" width="540" height="60" as="geometry"/>
    </mxCell>
  </root>
</mxGraphModel>"""

# ==============================================================================
# 4. MODUL 10 - GITHUB ACTIONS AUTOMATED CI/CD WORKFLOW PIPELINE
# ==============================================================================
xml_modul_10 = """<mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1350" pageHeight="680" background="#ffffff">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>

    <mxCell id="c_source" value="&lt;b&gt;Source &amp;amp; Event Ingestion&lt;/b&gt;" style="swimlane;startSize=28;fillColor=#f8fafc;strokeColor=#cbd5e1;fontColor=#0f172a;fontStyle=1;fontSize=12;rounded=1;html=1;" vertex="1" parent="1">
      <mxGeometry x="40" y="40" width="240" height="540" as="geometry"/>
    </mxCell>
    <mxCell id="n_dev_push" value="&lt;b&gt;Developer Terminal&lt;/b&gt;&lt;br&gt;git push origin main" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#3b82f6;strokeColor=#2563eb;fontColor=#ffffff;fontSize=12;fontFamily=Helvetica;" vertex="1" parent="c_source">
      <mxGeometry x="25" y="80" width="190" height="70" as="geometry"/>
    </mxCell>
    <mxCell id="n_gh_repo" value="&lt;b&gt;GitHub Repository&lt;/b&gt;&lt;br&gt;Webhook Event Trigger (:push)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1e293b;strokeColor=#0f172a;fontColor=#ffffff;fontSize=12;fontFamily=Helvetica;" vertex="1" parent="c_source">
      <mxGeometry x="25" y="320" width="190" height="70" as="geometry"/>
    </mxCell>

    <mxCell id="c_pipeline" value="&lt;b&gt;GitHub Actions Automation Runner (ubuntu-latest)&lt;/b&gt;" style="swimlane;startSize=28;fillColor=#f0fdf4;strokeColor=#86efac;fontColor=#065f46;fontStyle=1;fontSize=12;rounded=1;html=1;" vertex="1" parent="1">
      <mxGeometry x="320" y="40" width="640" height="540" as="geometry"/>
    </mxCell>
    <mxCell id="c_ci" value="&lt;b&gt;Job 1: code-quality (Continuous Integration)&lt;/b&gt;" style="swimlane;startSize=24;fillColor=#dcfce7;strokeColor=#86efac;fontColor=#166534;fontSize=11;rounded=1;html=1;" vertex="1" parent="c_pipeline">
      <mxGeometry x="30" y="50" width="580" height="190" as="geometry"/>
    </mxCell>
    <mxCell id="n_checkout" value="&lt;b&gt;actions/checkout@v4&lt;/b&gt;&lt;br&gt;Workspace Git Clone" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#86efac;fontColor=#166534;fontSize=11;fontFamily=Helvetica;" vertex="1" parent="c_ci">
      <mxGeometry x="30" y="45" width="150" height="60" as="geometry"/>
    </mxCell>
    <mxCell id="n_integrity" value="&lt;b&gt;File Integrity Check&lt;/b&gt;&lt;br&gt;test -f index.html &amp;amp; Dockerfile" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#86efac;fontColor=#166534;fontSize=11;fontFamily=Helvetica;" vertex="1" parent="c_ci">
      <mxGeometry x="210" y="45" width="160" height="60" as="geometry"/>
    </mxCell>
    <mxCell id="n_lint" value="&lt;b&gt;HTML Syntax Linter&lt;/b&gt;&lt;br&gt;grep -q &#39;&amp;lt;/html&amp;gt;&#39; index.html" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#86efac;fontColor=#166534;fontSize=11;fontFamily=Helvetica;" vertex="1" parent="c_ci">
      <mxGeometry x="390" y="45" width="160" height="60" as="geometry"/>
    </mxCell>
    <mxCell id="n_ci_status" value="&lt;b&gt;CI Quality Gate: PASSED (Fail-Fast Evaluator)&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#22c55e;strokeColor=#16a34a;fontColor=#ffffff;fontSize=11;fontFamily=Helvetica;fontStyle=1;" vertex="1" parent="c_ci">
      <mxGeometry x="30" y="125" width="520" height="40" as="geometry"/>
    </mxCell>

    <mxCell id="c_cd" value="&lt;b&gt;Job 2: build-and-push (Continuous Delivery / GHCR Publish)&lt;/b&gt;" style="swimlane;startSize=24;fillColor=#e0f2fe;strokeColor=#7dd3fc;fontColor=#0369a1;fontSize=11;rounded=1;html=1;" vertex="1" parent="c_pipeline">
      <mxGeometry x="30" y="270" width="580" height="235" as="geometry"/>
    </mxCell>
    <mxCell id="n_buildx" value="&lt;b&gt;docker/setup-buildx@v3&lt;/b&gt;&lt;br&gt;Moby BuildKit Engine" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#7dd3fc;fontColor=#0369a1;fontSize=11;fontFamily=Helvetica;" vertex="1" parent="c_cd">
      <mxGeometry x="30" y="45" width="150" height="65" as="geometry"/>
    </mxCell>
    <mxCell id="n_auth" value="&lt;b&gt;docker/login-action@v3&lt;/b&gt;&lt;br&gt;GITHUB_TOKEN Auth" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#7dd3fc;fontColor=#0369a1;fontSize=11;fontFamily=Helvetica;" vertex="1" parent="c_cd">
      <mxGeometry x="210" y="45" width="160" height="65" as="geometry"/>
    </mxCell>
    <mxCell id="n_meta" value="&lt;b&gt;metadata-action@v5&lt;/b&gt;&lt;br&gt;Tags: :latest, :sha-xxxx" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#7dd3fc;fontColor=#0369a1;fontSize=11;fontFamily=Helvetica;" vertex="1" parent="c_cd">
      <mxGeometry x="390" y="45" width="160" height="65" as="geometry"/>
    </mxCell>
    <mxCell id="n_push" value="&lt;b&gt;docker/build-push-action@v5&lt;/b&gt;&lt;br&gt;Build Container Image &amp;amp; Publish Layer Artifacts" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#0284c7;strokeColor=#0369a1;fontColor=#ffffff;fontSize=12;fontFamily=Helvetica;" vertex="1" parent="c_cd">
      <mxGeometry x="30" y="140" width="520" height="65" as="geometry"/>
    </mxCell>

    <mxCell id="c_dist" value="&lt;b&gt;Distribution &amp;amp; Production Target&lt;/b&gt;" style="swimlane;startSize=28;fillColor=#fefce8;strokeColor=#fef08a;fontColor=#713f12;fontStyle=1;fontSize=12;rounded=1;html=1;" vertex="1" parent="1">
      <mxGeometry x="1000" y="40" width="280" height="540" as="geometry"/>
    </mxCell>
    <mxCell id="n_ghcr" value="&lt;b&gt;GitHub Packages (GHCR)&lt;/b&gt;&lt;br&gt;ghcr.io/username/devops-cicd" style="shape=cylinder3;whiteSpace=wrap;html=1;fillColor=#fef08a;strokeColor=#eab308;fontColor=#854d0e;fontSize=12;fontFamily=Helvetica;" vertex="1" parent="c_dist">
      <mxGeometry x="35" y="160" width="210" height="100" as="geometry"/>
    </mxCell>
    <mxCell id="n_deploy" value="&lt;b&gt;Target Server / Host WSL2&lt;/b&gt;&lt;br&gt;docker pull &amp;amp; run -d" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#10b981;strokeColor=#059669;fontColor=#ffffff;fontSize=12;fontFamily=Helvetica;" vertex="1" parent="c_dist">
      <mxGeometry x="35" y="380" width="210" height="75" as="geometry"/>
    </mxCell>

    <mxCell id="e_push_repo" edge="1" parent="1" source="n_dev_push" target="n_gh_repo" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=2;strokeColor=#3b82f6;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_repo_ci" edge="1" parent="1" source="n_gh_repo" target="n_checkout" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=2;strokeColor=#16a34a;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_chk_int" edge="1" parent="1" source="n_checkout" target="n_integrity" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=2;strokeColor=#86efac;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_int_lint" edge="1" parent="1" source="n_integrity" target="n_lint" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=2;strokeColor=#86efac;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_lint_gate" edge="1" parent="1" source="n_lint" target="n_ci_status" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=2;strokeColor=#16a34a;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_gate_cd" edge="1" parent="1" source="n_ci_status" target="n_buildx" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=3;strokeColor=#0284c7;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_buildx_auth" edge="1" parent="1" source="n_buildx" target="n_auth" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=2;strokeColor=#7dd3fc;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_auth_meta" edge="1" parent="1" source="n_auth" target="n_meta" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=2;strokeColor=#7dd3fc;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_meta_push" edge="1" parent="1" source="n_meta" target="n_push" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=2;strokeColor=#0284c7;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_push_ghcr" edge="1" parent="1" source="n_push" target="n_ghcr" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=3;strokeColor=#0284c7;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_ghcr_deploy" edge="1" parent="1" source="n_ghcr" target="n_deploy" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=2;strokeColor=#10b981;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
  </root>
</mxGraphModel>"""

# ==============================================================================
# 5. MODUL 11 - NGINX REVERSE PROXY, SSL & OBSERVABILITY TOPOLOGY
# ==============================================================================
xml_modul_11 = """<mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1350" pageHeight="720" background="#ffffff">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>

    <mxCell id="c_ingress" value="&lt;b&gt;Client / Public Ingress Zone&lt;/b&gt;" style="swimlane;startSize=28;fillColor=#f8fafc;strokeColor=#cbd5e1;fontColor=#0f172a;fontStyle=1;fontSize=12;rounded=1;html=1;" vertex="1" parent="1">
      <mxGeometry x="40" y="40" width="260" height="600" as="geometry"/>
    </mxCell>
    <mxCell id="n_user" value="&lt;b&gt;Internet User / Browser&lt;/b&gt;&lt;br&gt;TLSv1.3 HTTPS Client" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#0284c7;strokeColor=#0369a1;fontColor=#ffffff;fontSize=12;fontFamily=Helvetica;" vertex="1" parent="c_ingress">
      <mxGeometry x="30" y="80" width="200" height="70" as="geometry"/>
    </mxCell>
    <mxCell id="n_plain_http" value="&lt;b&gt;Insecure HTTP Request&lt;/b&gt;&lt;br&gt;http://localhost:80" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fee2e2;strokeColor=#fca5a5;fontColor=#991b1b;fontSize=11;fontFamily=Helvetica;" vertex="1" parent="c_ingress">
      <mxGeometry x="30" y="240" width="200" height="60" as="geometry"/>
    </mxCell>
    <mxCell id="n_secure_https" value="&lt;b&gt;Encrypted HTTPS Request&lt;/b&gt;&lt;br&gt;https://localhost:443" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dcfce7;strokeColor=#86efac;fontColor=#166534;fontSize=11;fontFamily=Helvetica;" vertex="1" parent="c_ingress">
      <mxGeometry x="30" y="420" width="200" height="60" as="geometry"/>
    </mxCell>

    <mxCell id="c_proxy" value="&lt;b&gt;Nginx Edge Gateway &amp;amp; SSL Termination (nginx-gateway)&lt;/b&gt;" style="swimlane;startSize=28;fillColor=#f0fdf4;strokeColor=#86efac;fontColor=#065f46;fontStyle=1;fontSize=12;rounded=1;html=1;" vertex="1" parent="1">
      <mxGeometry x="350" y="40" width="460" height="600" as="geometry"/>
    </mxCell>
    <mxCell id="n_redirect_srv" value="&lt;b&gt;HTTP 301 Redirect Server&lt;/b&gt;&lt;br&gt;listen 80; return 301 https://$host$uri;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fef08a;strokeColor=#eab308;fontColor=#854d0e;fontSize=11;fontFamily=Helvetica;" vertex="1" parent="c_proxy">
      <mxGeometry x="40" y="80" width="380" height="60" as="geometry"/>
    </mxCell>
    <mxCell id="n_ssl_engine" value="&lt;b&gt;SSL/TLS Termination Engine&lt;/b&gt;&lt;br&gt;OpenSSL x509 (server.crt &amp;amp; server.key)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#10b981;strokeColor=#059669;fontColor=#ffffff;fontSize=12;fontFamily=Helvetica;" vertex="1" parent="c_proxy">
      <mxGeometry x="40" y="200" width="380" height="70" as="geometry"/>
    </mxCell>
    <mxCell id="n_hdr_fwd" value="&lt;b&gt;Client Identity Forwarder&lt;/b&gt;&lt;br&gt;X-Real-IP &amp;amp; X-Forwarded-Proto $scheme" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ecfdf5;strokeColor=#a7f3d0;fontColor=#065f46;fontSize=11;fontFamily=Helvetica;" vertex="1" parent="c_proxy">
      <mxGeometry x="40" y="320" width="380" height="60" as="geometry"/>
    </mxCell>
    <mxCell id="n_lb_core" value="&lt;b&gt;Round-Robin Load Balancer&lt;/b&gt;&lt;br&gt;upstream my_cluster { app1:80; app2:80; }" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#059669;strokeColor=#047857;fontColor=#ffffff;fontSize=12;fontFamily=Helvetica;" vertex="1" parent="c_proxy">
      <mxGeometry x="40" y="440" width="380" height="70" as="geometry"/>
    </mxCell>

    <mxCell id="c_cluster" value="&lt;b&gt;Isolated Docker Network (internal-net bridge)&lt;/b&gt;" style="swimlane;startSize=28;fillColor=#eff6ff;strokeColor=#93c5fd;fontColor=#1e3a8a;fontStyle=1;fontSize=12;rounded=1;html=1;" vertex="1" parent="1">
      <mxGeometry x="850" y="40" width="460" height="380" as="geometry"/>
    </mxCell>
    <mxCell id="n_app1" value="&lt;b&gt;backend-alpha (App Instance 1)&lt;/b&gt;&lt;br&gt;Nginx Alpine Container (172.19.0.2:80)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1e3a8a;strokeColor=#172554;fontColor=#ffffff;fontSize=12;fontFamily=Helvetica;" vertex="1" parent="c_cluster">
      <mxGeometry x="50" y="70" width="360" height="80" as="geometry"/>
    </mxCell>
    <mxCell id="n_app2" value="&lt;b&gt;backend-beta (App Instance 2)&lt;/b&gt;&lt;br&gt;Nginx Alpine Container (172.19.0.3:80)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#065f46;strokeColor=#022c22;fontColor=#ffffff;fontSize=12;fontFamily=Helvetica;" vertex="1" parent="c_cluster">
      <mxGeometry x="50" y="210" width="360" height="80" as="geometry"/>
    </mxCell>

    <mxCell id="c_obs_tier" value="&lt;b&gt;Observability &amp;amp; Telemetry Subsystem&lt;/b&gt;" style="swimlane;startSize=28;fillColor=#fefce8;strokeColor=#fef08a;fontColor=#713f12;fontStyle=1;fontSize=12;rounded=1;html=1;" vertex="1" parent="1">
      <mxGeometry x="850" y="440" width="460" height="200" as="geometry"/>
    </mxCell>
    <mxCell id="n_access_log" value="&lt;b&gt;custom_devops Format Log Stream&lt;/b&gt;&lt;br&gt;Upstream: $upstream_addr | Status: $status | Latency: ${upstream_response_time}s" style="shape=cylinder3;whiteSpace=wrap;html=1;fillColor=#fef9c3;strokeColor=#fde047;fontColor=#713f12;fontSize=11;fontFamily=Helvetica;" vertex="1" parent="c_obs_tier">
      <mxGeometry x="40" y="50" width="380" height="100" as="geometry"/>
    </mxCell>

    <mxCell id="e_u_plain" edge="1" parent="1" source="n_user" target="n_plain_http" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=2;strokeColor=#ef4444;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_plain_red" edge="1" parent="1" source="n_plain_http" target="n_redirect_srv" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=2;strokeColor=#f59e0b;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_red_sec" edge="1" parent="1" source="n_redirect_srv" target="n_secure_https" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;dashed=1;strokeWidth=2;strokeColor=#10b981;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_sec_ssl" edge="1" parent="1" source="n_secure_https" target="n_ssl_engine" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=2;strokeColor=#10b981;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_ssl_fwd" edge="1" parent="1" source="n_ssl_engine" target="n_hdr_fwd" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=2;strokeColor=#10b981;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_fwd_lb" edge="1" parent="1" source="n_hdr_fwd" target="n_lb_core" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=2;strokeColor=#059669;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_lb_app1" edge="1" parent="1" source="n_lb_core" target="n_app1" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=2;strokeColor=#1e3a8a;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_lb_app2" edge="1" parent="1" source="n_lb_core" target="n_app2" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=2;strokeColor=#065f46;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_lb_log" edge="1" parent="1" source="n_lb_core" target="n_access_log" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;dashed=1;strokeWidth=2;strokeColor=#eab308;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
  </root>
</mxGraphModel>"""

# ==============================================================================
# 6. README.MD - BASIC DEVOPS CURRICULUM ROADMAP
# ==============================================================================
xml_curriculum = """<mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1350" pageHeight="450" background="#ffffff">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>

    <mxCell id="m7" value="&lt;b&gt;MODUL 07&lt;/b&gt;&lt;br&gt;Linux &amp;amp; Web Server Foundations&lt;br&gt;&lt;font color=&#39;#64748b&#39;&gt;WSL2, Nginx Core, VHosts&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dbeafe;strokeColor=#3b82f6;fontColor=#1e3a8a;fontSize=12;fontFamily=Helvetica;strokeWidth=2;" vertex="1" parent="1">
      <mxGeometry x="40" y="140" width="220" height="110" as="geometry"/>
    </mxCell>
    <mxCell id="m8" value="&lt;b&gt;MODUL 08&lt;/b&gt;&lt;br&gt;Git &amp;amp; Shell Automation&lt;br&gt;&lt;font color=&#39;#64748b&#39;&gt;Defensive Bash, Zero-Downtime&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dcfce7;strokeColor=#22c55e;fontColor=#14532d;fontSize=12;fontFamily=Helvetica;strokeWidth=2;" vertex="1" parent="1">
      <mxGeometry x="300" y="140" width="220" height="110" as="geometry"/>
    </mxCell>
    <mxCell id="m9" value="&lt;b&gt;MODUL 09&lt;/b&gt;&lt;br&gt;Docker Containerization&lt;br&gt;&lt;font color=&#39;#64748b&#39;&gt;Alpine Image, Compose Cluster&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e0f2fe;strokeColor=#0284c7;fontColor=#0369a1;fontSize=12;fontFamily=Helvetica;strokeWidth=2;" vertex="1" parent="1">
      <mxGeometry x="560" y="140" width="220" height="110" as="geometry"/>
    </mxCell>
    <mxCell id="m10" value="&lt;b&gt;MODUL 10&lt;/b&gt;&lt;br&gt;CI/CD Pipeline Automation&lt;br&gt;&lt;font color=&#39;#64748b&#39;&gt;GitHub Actions &amp;amp; GHCR Publish&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f3e8ff;strokeColor=#a855f7;fontColor=#581c87;fontSize=12;fontFamily=Helvetica;strokeWidth=2;" vertex="1" parent="1">
      <mxGeometry x="820" y="140" width="220" height="110" as="geometry"/>
    </mxCell>
    <mxCell id="m11" value="&lt;b&gt;MODUL 11&lt;/b&gt;&lt;br&gt;Gateway, SSL &amp;amp; Observability&lt;br&gt;&lt;font color=&#39;#64748b&#39;&gt;Reverse Proxy, LB, TLS 1.3&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fef08a;strokeColor=#eab308;fontColor=#713f12;fontSize=12;fontFamily=Helvetica;strokeWidth=2;" vertex="1" parent="1">
      <mxGeometry x="1080" y="140" width="230" height="110" as="geometry"/>
    </mxCell>

    <mxCell id="e_7_8" edge="1" parent="1" source="m7" target="m8" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=3;strokeColor=#3b82f6;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_8_9" edge="1" parent="1" source="m8" target="m9" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=3;strokeColor=#22c55e;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_9_10" edge="1" parent="1" source="m9" target="m10" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=3;strokeColor=#0284c7;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="e_10_11" edge="1" parent="1" source="m10" target="m11" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeWidth=3;strokeColor=#a855f7;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
  </root>
</mxGraphModel>"""

if __name__ == '__main__':
    print("=== EXPORTING PRODUCTION DRAW.IO DIAGRAMS ===")
    
    # 1. Modul 7
    export_drawio(
        xml_modul_07,
        'docs/diagrams/modul_07_nginx_architecture.drawio',
        'assets/modul-07/00_arsitektur_nginx.png',
        'assets/modul-07/00_arsitektur_nginx.svg'
    )

    # 2. Modul 8
    export_drawio(
        xml_modul_08,
        'docs/diagrams/modul_08_deployment_pipeline.drawio',
        'assets/modul-08/00_arsitektur_deployment.png',
        'assets/modul-08/00_arsitektur_deployment.svg'
    )

    # 3. Modul 9
    export_drawio(
        xml_modul_09,
        'docs/diagrams/modul_09_docker_architecture.drawio',
        'assets/modul-09/00_arsitektur_docker.png',
        'assets/modul-09/00_arsitektur_docker.svg'
    )

    # 4. Modul 10
    export_drawio(
        xml_modul_10,
        'docs/diagrams/modul_10_cicd_pipeline.drawio',
        'assets/modul-10/00_arsitektur_cicd.png',
        'assets/modul-10/00_arsitektur_cicd.svg'
    )

    # 5. Modul 11
    export_drawio(
        xml_modul_11,
        'docs/diagrams/modul_11_reverse_proxy_topology.drawio',
        'assets/modul-11/00_arsitektur_reverse_proxy.png',
        'assets/modul-11/00_arsitektur_reverse_proxy.svg'
    )

    # 6. Roadmap Curriculum
    export_drawio(
        xml_curriculum,
        'docs/diagrams/curriculum_roadmap.drawio',
        'assets/kurikulum_devops_roadmap.png',
        'assets/kurikulum_devops_roadmap.svg',
        viewport=(1500, 600)
    )

    print("ALL DRAW.IO DIAGRAMS EXPORTED AND PLACED IN ASSETS SUCCESSFULLY!")
