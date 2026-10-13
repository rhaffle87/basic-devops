import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO_ROOT)

def create_drawio_xml():
    xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="drawio" version="26.0.0">
  <diagram name="Arsitektur-Webserver-Modul-7" id="modul-7-light-arch">
    <mxGraphModel dx="1200" dy="1000" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1160" pageHeight="920" background="#ffffff" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- Title Header (Minimalist Modern) -->
        <mxCell id="title_header" value="&lt;font color=&quot;#0f172a&quot; style=&quot;font-size: 16px; font-weight: bold;&quot;&gt;Arsitektur Web Server Nginx &amp;amp; Siklus Komunikasi HTTP (Modul 7)&lt;/font&gt;&lt;br&gt;&lt;font color=&quot;#64748b&quot; style=&quot;font-size: 11px;&quot;&gt;Production Architecture with Official Service Components &amp;amp; Lightweight Isolation&lt;/font&gt;" style="text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;" vertex="1" parent="1">
          <mxGeometry x="340" y="20" width="480" height="40" as="geometry" />
        </mxCell>

        <!-- ================= LAYER 1: CLIENT LAYER ================= -->
        <!-- Card 1: Google Chrome -->
        <mxCell id="card_chrome" value="&lt;b style=&quot;font-size: 13px; color: #0f172a;&quot;&gt;Google Chrome&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size: 11px; color: #64748b;&quot;&gt;Host Web Browser (Port 80)&lt;/span&gt;" style="rounded=1;arcSize=12;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#2563eb;strokeWidth=2.5;align=left;spacingLeft=68;shadow=0;" vertex="1" parent="1">
          <mxGeometry x="310" y="85" width="240" height="72" as="geometry" />
        </mxCell>
        <mxCell id="icon_chrome" value="" style="shape=image;html=1;verticalAlign=top;verticalLabelPosition=bottom;imageAspect=0;aspect=fixed;image=https://cdn.jsdelivr.net/gh/devicons/devicon/icons/chrome/chrome-original.svg;" vertex="1" parent="card_chrome">
          <mxGeometry x="16" y="16" width="38" height="38" as="geometry" />
        </mxCell>

        <!-- Card 2: Terminal / cURL Client -->
        <mxCell id="card_curl" value="&lt;b style=&quot;font-size: 13px; color: #0f172a;&quot;&gt;Terminal / curl&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size: 11px; color: #64748b;&quot;&gt;HTTP CLI Test Client&lt;/span&gt;" style="rounded=1;arcSize=12;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#0284c7;strokeWidth=2.5;align=left;spacingLeft=68;shadow=0;" vertex="1" parent="1">
          <mxGeometry x="610" y="85" width="240" height="72" as="geometry" />
        </mxCell>
        <mxCell id="icon_curl" value="" style="shape=image;html=1;verticalAlign=top;verticalLabelPosition=bottom;imageAspect=0;aspect=fixed;image=https://cdn.jsdelivr.net/gh/devicons/devicon/icons/bash/bash-original.svg;" vertex="1" parent="card_curl">
          <mxGeometry x="16" y="16" width="38" height="38" as="geometry" />
        </mxCell>

        <!-- ================= LAYER 2: HOST OS GATEWAY ================= -->
        <!-- Card 3: Windows 10/11 Host Winsock -->
        <mxCell id="card_winsock" value="&lt;b style=&quot;font-size: 13px; color: #0f172a;&quot;&gt;Windows 10/11 OS&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size: 11px; color: #64748b;&quot;&gt;Winsock TCP Stack (127.0.0.1)&lt;/span&gt;" style="rounded=1;arcSize=12;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#0078d7;strokeWidth=2.5;align=left;spacingLeft=68;shadow=0;" vertex="1" parent="1">
          <mxGeometry x="460" y="210" width="240" height="72" as="geometry" />
        </mxCell>
        <mxCell id="icon_winsock" value="" style="shape=image;html=1;verticalAlign=top;verticalLabelPosition=bottom;imageAspect=0;aspect=fixed;image=https://cdn.jsdelivr.net/gh/devicons/devicon/icons/windows8/windows8-original.svg;" vertex="1" parent="card_winsock">
          <mxGeometry x="16" y="16" width="38" height="38" as="geometry" />
        </mxCell>

        <!-- ================= LAYER 3: WSL2 LINUX ENVIRONMENT CONTAINER ================= -->
        <mxCell id="container_wsl" value="Windows Subsystem for Linux (WSL2) &amp;mdash; Ubuntu 22.04 LTS Environment" style="swimlane;startSize=36;rounded=1;arcSize=6;fillColor=#f8fafc;strokeColor=#cbd5e1;strokeWidth=1.5;fontStyle=1;fontSize=12;fontColor=#1e293b;swimlaneFillColor=#f8fafc;swimlaneHeadFillColor=#e2e8f0;html=1;align=left;spacingLeft=20;" vertex="1" parent="1">
          <mxGeometry x="130" y="330" width="900" height="530" as="geometry" />
        </mxCell>

        <!-- Ubuntu Logo in Header -->
        <mxCell id="icon_ubuntu" value="" style="shape=image;html=1;verticalAlign=top;verticalLabelPosition=bottom;imageAspect=0;aspect=fixed;image=https://cdn.jsdelivr.net/gh/devicons/devicon/icons/ubuntu/ubuntu-plain.svg;" vertex="1" parent="container_wsl">
          <mxGeometry x="830" y="7" width="22" height="22" as="geometry" />
        </mxCell>
        <!-- Linux Tux Logo in Header -->
        <mxCell id="icon_linux" value="" style="shape=image;html=1;verticalAlign=top;verticalLabelPosition=bottom;imageAspect=0;aspect=fixed;image=https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linux/linux-original.svg;" vertex="1" parent="container_wsl">
          <mxGeometry x="860" y="7" width="22" height="22" as="geometry" />
        </mxCell>

        <!-- Card 4: Nginx Master Process (Gateway / Supervisor) -->
        <mxCell id="card_master" value="&lt;b style=&quot;font-size: 13px; color: #0f172a;&quot;&gt;Nginx Master&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size: 11px; color: #64748b;&quot;&gt;Privileged Daemon • Root PID 1240&lt;/span&gt;" style="rounded=1;arcSize=12;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#059669;strokeWidth=2.5;align=left;spacingLeft=68;shadow=0;" vertex="1" parent="container_wsl">
          <mxGeometry x="330" y="70" width="240" height="72" as="geometry" />
        </mxCell>
        <mxCell id="icon_master" value="" style="shape=image;html=1;verticalAlign=top;verticalLabelPosition=bottom;imageAspect=0;aspect=fixed;image=https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nginx/nginx-original.svg;" vertex="1" parent="card_master">
          <mxGeometry x="16" y="16" width="38" height="38" as="geometry" />
        </mxCell>

        <!-- Card 5: Nginx Worker Process (Event-Driven Engine) -->
        <mxCell id="card_worker" value="&lt;b style=&quot;font-size: 13px; color: #0f172a;&quot;&gt;Nginx Worker&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size: 11px; color: #64748b;&quot;&gt;epoll Event Loop • www-data&lt;/span&gt;" style="rounded=1;arcSize=12;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#10b981;strokeWidth=2.5;align=left;spacingLeft=68;shadow=0;" vertex="1" parent="container_wsl">
          <mxGeometry x="330" y="200" width="240" height="72" as="geometry" />
        </mxCell>
        <mxCell id="icon_worker" value="" style="shape=image;html=1;verticalAlign=top;verticalLabelPosition=bottom;imageAspect=0;aspect=fixed;image=https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nginx/nginx-original.svg;" vertex="1" parent="card_worker">
          <mxGeometry x="16" y="16" width="38" height="38" as="geometry" />
        </mxCell>

        <!-- Card 6: Virtual Host Config -->
        <mxCell id="card_vhost" value="&lt;b style=&quot;font-size: 13px; color: #0f172a;&quot;&gt;Virtual Host Config&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size: 11px; color: #64748b;&quot;&gt;/etc/nginx/sites-available&lt;/span&gt;" style="rounded=1;arcSize=12;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#8b5cf6;strokeWidth=2.5;align=left;spacingLeft=68;shadow=0;" vertex="1" parent="container_wsl">
          <mxGeometry x="40" y="350" width="240" height="72" as="geometry" />
        </mxCell>
        <mxCell id="icon_vhost" value="" style="shape=image;html=1;verticalAlign=top;verticalLabelPosition=bottom;imageAspect=0;aspect=fixed;image=https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/sliders-horizontal.svg;" vertex="1" parent="card_vhost">
          <mxGeometry x="16" y="18" width="36" height="36" as="geometry" />
        </mxCell>

        <!-- Card 7: Document Root Storage (HTML5 Portfolio) -->
        <mxCell id="card_storage" value="&lt;b style=&quot;font-size: 13px; color: #0f172a;&quot;&gt;Document Root (HTML5)&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size: 11px; color: #64748b;&quot;&gt;/var/www/html/Portfolio&lt;/span&gt;" style="rounded=1;arcSize=12;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#ea580c;strokeWidth=2.5;align=left;spacingLeft=68;shadow=0;" vertex="1" parent="container_wsl">
          <mxGeometry x="330" y="350" width="240" height="72" as="geometry" />
        </mxCell>
        <mxCell id="icon_storage" value="" style="shape=image;html=1;verticalAlign=top;verticalLabelPosition=bottom;imageAspect=0;aspect=fixed;image=https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg;" vertex="1" parent="card_storage">
          <mxGeometry x="16" y="16" width="38" height="38" as="geometry" />
        </mxCell>

        <!-- Card 8: Access Logs -->
        <mxCell id="card_logs" value="&lt;b style=&quot;font-size: 13px; color: #0f172a;&quot;&gt;Access &amp;amp; Error Logs&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size: 11px; color: #64748b;&quot;&gt;/var/log/nginx/access.log&lt;/span&gt;" style="rounded=1;arcSize=12;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#64748b;strokeWidth=2.5;align=left;spacingLeft=68;shadow=0;" vertex="1" parent="container_wsl">
          <mxGeometry x="620" y="350" width="240" height="72" as="geometry" />
        </mxCell>
        <mxCell id="icon_logs" value="" style="shape=image;html=1;verticalAlign=top;verticalLabelPosition=bottom;imageAspect=0;aspect=fixed;image=https://cdn.jsdelivr.net/gh/devicons/devicon/icons/bash/bash-original.svg;" vertex="1" parent="card_logs">
          <mxGeometry x="16" y="18" width="36" height="36" as="geometry" />
        </mxCell>

        <!-- ================= EDGES & CONNECTORS ================= -->
        <!-- Edge 1: Chrome -> Winsock -->
        <mxCell id="edge_chrome_sock" value="HTTP GET" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#2563eb;strokeWidth=2;fontSize=10;fontColor=#0f172a;labelBackgroundColor=#ffffff;labelBorderColor=#cbd5e1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.25;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="card_chrome" target="card_winsock">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Edge 2: Curl -> Winsock -->
        <mxCell id="edge_curl_sock" value="CLI GET" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#0284c7;strokeWidth=2;fontSize=10;fontColor=#0f172a;labelBackgroundColor=#ffffff;labelBorderColor=#cbd5e1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.75;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="card_curl" target="card_winsock">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Edge 3: Winsock -> Nginx Master (Direct Vertical Down) -->
        <mxCell id="edge_sock_master" value="Port 80 TCP" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#0078d7;strokeWidth=2.5;fontSize=10;fontColor=#0f172a;labelBackgroundColor=#ffffff;labelBorderColor=#cbd5e1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="card_winsock" target="card_master">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Edge 4: Master -> Worker (Direct Vertical Down) -->
        <mxCell id="edge_master_worker" value="IPC Spawn" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#059669;strokeWidth=2.5;fontSize=10;fontColor=#0f172a;labelBackgroundColor=#ffffff;labelBorderColor=#cbd5e1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="container_wsl" source="card_master" target="card_worker">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Edge 5: Master -> Virtual Host Config (Load Config) -->
        <mxCell id="edge_master_vhost" value="Read Config" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#8b5cf6;strokeWidth=2;dashed=1;fontSize=10;fontColor=#0f172a;labelBackgroundColor=#ffffff;labelBorderColor=#cbd5e1;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="container_wsl" source="card_master" target="card_vhost">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Edge 6: Worker -> Storage (sendfile read) -->
        <mxCell id="edge_worker_storage" value="sendfile()" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#ea580c;strokeWidth=2.5;fontSize=10;fontColor=#0f172a;labelBackgroundColor=#ffffff;labelBorderColor=#cbd5e1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="container_wsl" source="card_worker" target="card_storage">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Edge 7: Worker -> Logs (Log Entry) -->
        <mxCell id="edge_worker_logs" value="Write Log" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#64748b;strokeWidth=2;dashed=1;fontSize=10;fontColor=#0f172a;labelBackgroundColor=#ffffff;labelBorderColor=#cbd5e1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="container_wsl" source="card_worker" target="card_logs">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Edge 8: Worker -> Chrome (HTTP 200 Response via Clean Outer Channel) -->
        <mxCell id="edge_worker_chrome" value="HTTP 200 OK" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#10b981;strokeWidth=2.5;fontSize=10;fontColor=#0f172a;labelBackgroundColor=#ffffff;labelBorderColor=#cbd5e1;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="card_worker" target="card_chrome">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="60" y="566" />
              <mxPoint x="60" y="121" />
            </Array>
          </mxGeometry>
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
'''
    target_path = 'assets/modul-07/00_arsitektur_webserver_nginx.drawio'
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(xml_content.strip())
    print(f'Wrote XML to {target_path}')

if __name__ == '__main__':
    create_drawio_xml()
