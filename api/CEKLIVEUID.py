from http.server import BaseHTTPRequestHandler

# Simpan seluruh kode HTML, CSS, dan JS ke dalam variabel string Python
HTML_PAGE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cek Live UID - Dimmskuy Tools</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #090d16;
            --sidebar-bg: #0f172a;
            --panel-bg: rgba(30, 41, 59, 0.6);
            --accent: #3b82f6;
            --accent-hover: #2563eb;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border: rgba(255, 255, 255, 0.08);
            --badge-bg: rgba(59, 130, 246, 0.15);
            --badge-color: #60a5fa;
            --green-live: #10b981;
            --red-dead: #ef4444;
        }
        body { font-family: 'Inter', sans-serif; background-color: var(--bg-dark); color: var(--text-main); margin: 0; padding: 0; padding-top: 60px; min-height: 100vh; display: flex; overflow-x: hidden; }
        .topbar { position: fixed; top: 0; left: 0; width: 100%; height: 60px; background: var(--sidebar-bg); border-bottom: 1px solid var(--border); display: flex; align-items: center; padding: 0 20px; box-sizing: border-box; z-index: 1000; justify-content: flex-start; gap: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.3); }
        .menu-toggle { background: none; border: none; cursor: pointer; display: flex; flex-direction: column; justify-content: space-around; width: 26px; height: 22px; padding: 0; z-index: 1001; order: 1; }
        .menu-toggle span { display: block; width: 100%; height: 3px; background-color: var(--text-main); border-radius: 3px; transition: all 0.3s ease; }
        .menu-toggle:hover span { background-color: var(--accent); }
        .topbar-brand { order: 2; font-size: 1.25rem; font-weight: 700; background: linear-gradient(to right, #60a5fa, #34d399); -webkit-background-clip: text; -webkit-text-fill-color: transparent; display: flex; align-items: center; }
        @media (max-width: 768px) { .topbar { justify-content: space-between; } .menu-toggle { order: 2; } .topbar-brand { order: 1; } }
        .sidebar { width: 280px; background-color: var(--sidebar-bg); border-right: 1px solid var(--border); padding: 24px 16px; box-sizing: border-box; height: calc(100vh - 60px); position: fixed; top: 60px; left: -320px; transition: left 0.3s ease; overflow-y: auto; z-index: 999; box-shadow: 4px 0 20px rgba(0,0,0,0.4); }
        .sidebar.active { left: 0; }
        .overlay { position: fixed; top: 60px; left: 0; width: 100%; height: calc(100vh - 60px); background: rgba(0,0,0,0.5); backdrop-filter: blur(2px); z-index: 998; visibility: hidden; opacity: 0; transition: opacity 0.3s ease, visibility 0.3s ease; }
        .overlay.active { visibility: visible; opacity: 1; }
        .category-group { margin-bottom: 16px; background: rgba(15, 23, 42, 0.4); border: 1px solid var(--border); border-radius: 10px; overflow: hidden; }
        .category-title { display: flex; align-items: center; justify-content: space-between; padding: 12px 14px; font-weight: 600; font-size: 0.95rem; color: var(--text-main); background: rgba(30, 41, 59, 0.6); border-bottom: 1px solid rgba(255,255,255,0.05); }
        .category-title-left { display: flex; align-items: center; gap: 10px; }
        .badge { background: var(--badge-bg); color: var(--badge-color); padding: 2px 8px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }
        .submenu { padding: 8px 14px; display: flex; flex-direction: column; gap: 6px; }
        .submenu-item { display: flex; align-items: center; justify-content: flex-start; padding: 8px; color: var(--text-muted); text-decoration: none; border-radius: 6px; font-size: 0.9rem; transition: all 0.2s ease; gap: 10px; }
        .submenu-item:hover, .submenu-item.active { background: rgba(59, 130, 246, 0.1); color: var(--text-main); }
        .main-content { padding: 40px; width: 100%; box-sizing: border-box; transition: padding-left 0.3s ease; display: flex; flex-direction: column; gap: 20px; }
        @media (min-width: 769px) { .sidebar.active ~ .main-content { padding-left: 320px; } }
        @media (max-width: 768px) { .main-content { padding: 20px; } }
        
        /* Tool Khusus */
        .tool-header { background: var(--panel-bg); border: 1px solid var(--border); border-radius: 12px; padding: 20px; }
        .tool-header h2 { margin: 0 0 10px 0; color: #fff; display: flex; align-items: center; gap: 10px; }
        .tool-header p { margin: 0; color: var(--text-muted); font-size: 0.95rem; }
        .tool-card { background: var(--sidebar-bg); border: 1px solid var(--border); border-radius: 12px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        label { display: block; font-weight: 600; margin-bottom: 10px; font-size: 15px; color: var(--text-main);}
        textarea { width: 100%; background-color: var(--bg-dark); color: var(--text-main); border: 1px solid var(--border); border-radius: 8px; padding: 12px; font-family: monospace; font-size: 14px; resize: vertical; outline: none; box-sizing: border-box; }
        textarea:focus { border-color: var(--accent); }
        #inputList { height: 160px; margin-bottom: 15px; }
        .btn-primary { width: 100%; background-color: var(--accent); color: white; border: none; padding: 12px; border-radius: 8px; font-size: 16px; font-weight: 600; cursor: pointer; transition: 0.2s; }
        .btn-primary:hover { background-color: var(--accent-hover); }
        .btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
        .status-text { text-align: center; font-weight: bold; margin-bottom: 15px; color: var(--accent); font-size: 15px; }
        .results-container { display: flex; gap: 20px; }
        @media (max-width: 768px) { .results-container { flex-direction: column; } }
        .result-box { flex: 1; display: flex; flex-direction: column; }
        .result-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; font-weight: bold; font-size: 14px; }
        .result-badge { padding: 3px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; color: white; background-color: #374151;}
        .live-text { color: var(--green-live); }
        .dead-text { color: var(--red-dead); }
        .bg-live { background-color: var(--green-live); color: #000; }
        .bg-dead { background-color: var(--red-dead); }
        .btn-copy { background-color: transparent; border: 1px solid var(--border); color: var(--text-main); padding: 5px 12px; border-radius: 6px; cursor: pointer; font-size: 12px; transition: 0.2s; }
        .btn-copy:hover { background-color: rgba(255,255,255,0.1); }
        .out-area { height: 350px; }
        .out-live { border-color: rgba(16, 185, 129, 0.3); }
        .out-dead { border-color: rgba(239, 68, 68, 0.3); }
    </style>
</head>
<body>
    <header class="topbar">
        <button class="menu-toggle" id="menuToggle"><span></span><span></span><span></span></button>
        <div class="topbar-brand">⚡ Dimmskuy Tools</div>
    </header>

    <div class="overlay" id="overlay"></div>

    <nav class="sidebar" id="sidebar">
        <div class="category-group">
            <div class="category-title">
                <div class="category-title-left">
                    <svg style="width:18px;height:18px" viewBox="0 0 24 24"><path fill="#1877F2" d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.469h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.469h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
                    Facebook Tools
                </div>
                <span class="badge">3</span>
            </div>
            <div class="submenu">
                <a href="/api/PENCOCOKUID" class="submenu-item"><span style="font-size: 14px; color: #3b82f6;">◆</span> Pencocok UID</a>
                <a href="/api/EKSTRAKUID" class="submenu-item"><span style="font-size: 14px; color: #3b82f6;">◆</span> Ekstrak UID</a>
                <a href="/api/CEKLIVEUID" class="submenu-item active"><span style="font-size: 14px; color: #3b82f6;">◆</span> Cek Live UID</a>
            </div>
        </div>
        <div class="category-group">
            <div class="category-title">
                <div class="category-title-left">
                    <svg style="width:18px;height:18px" viewBox="0 0 448 512"><path fill="#ffffff" d="M448 209.91a210.06 210.06 0 0 1-122.77-39.25V349.38A162.55 162.55 0 1 1 185 188.31V278.2a74.62 74.62 0 1 0 52.23 71.18V0l88 0a121.18 121.18 0 0 0 1.86 22.17h0A122.18 122.18 0 0 0 381 102.39a121.43 121.43 0 0 0 67 20.14Z"/></svg>
                    TikTok Tools
                </div>
                <span class="badge">2</span>
            </div>
        </div>
    </nav>

    <main class="main-content" id="mainContent">
        <div class="tool-header">
            <h2>
                <svg style="width:24px;height:24px" viewBox="0 0 24 24"><path fill="#1877F2" d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.469h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.469h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
                Cek Live UID
            </h2>
            <p>Alat pemeriksa status aktif atau mati dari daftar UID Facebook (Client-Side Rendering untuk Bypass Vercel Timeout).</p>
        </div>

        <div class="tool-card">
            <label>🕵️ Daftar UID (Format bebas: UID saja atau UID|Pass|dll)</label>
            <textarea id="inputList" placeholder="Tempel daftar UID di sini..."></textarea>
            <button id="btnStart" class="btn-primary">⚡ Mulai Cek Status UID</button>
        </div>

        <div class="tool-card">
            <div id="statusInfo" class="status-text" style="display: none;">✅ Selesai memproses 0 data.</div>
            <div class="results-container">
                <div class="result-box">
                    <div class="result-header">
                        <span class="live-text">✅ HASIL LIVE <span class="result-badge bg-live" id="countLive">0</span></span>
                        <button class="btn-copy" onclick="copyText('outLive')">📋 Salin</button>
                    </div>
                    <textarea id="outLive" class="out-area out-live" readonly></textarea>
                </div>
                <div class="result-box">
                    <div class="result-header">
                        <span class="dead-text">❌ HASIL DEAD <span class="result-badge bg-dead" id="countDead">0</span></span>
                        <button class="btn-copy" onclick="copyText('outDead')">📋 Salin</button>
                    </div>
                    <textarea id="outDead" class="out-area out-dead" readonly></textarea>
                </div>
            </div>
        </div>
    </main>

    <script>
        const menuToggle = document.getElementById('menuToggle');
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('overlay');
        function toggleMenu() { sidebar.classList.toggle('active'); overlay.classList.toggle('active'); }
        menuToggle.addEventListener('click', toggleMenu);
        overlay.addEventListener('click', toggleMenu);

        const inputList = document.getElementById('inputList');
        const btnStart = document.getElementById('btnStart');
        const outLive = document.getElementById('outLive');
        const outDead = document.getElementById('outDead');
        const countLiveEl = document.getElementById('countLive');
        const countDeadEl = document.getElementById('countDead');
        const statusInfo = document.getElementById('statusInfo');

        function checkUID(uid) {
            return new Promise((resolve) => {
                let img = new Image();
                img.onload = function() {
                    if (img.width === 100 && img.height === 100) resolve("LIVE");
                    else if (img.width === 100 && img.height === 63) resolve("DEAD");
                    else resolve("UNKNOWN_DIMENSION"); 
                };
                img.onerror = function() { resolve("UNKNOWN_400"); };
                img.src = "https://graph.facebook.com/" + uid + "/picture?type=normal&_=" + new Date().getTime();
            });
        }

        btnStart.addEventListener('click', async function() {
            let lines = inputList.value.split('\\n').map(line => line.trim()).filter(line => line.length > 0);
            if (lines.length === 0) { alert("Harap masukkan minimal 1 baris data!"); return; }

            btnStart.disabled = true;
            btnStart.innerText = "⏳ Sedang Memproses...";
            outLive.value = ""; outDead.value = "";
            let liveCount = 0; let deadCount = 0;
            countLiveEl.innerText = liveCount; countDeadEl.innerText = deadCount;
            statusInfo.style.display = "block";
            
            const batchSize = 25; 
            for (let i = 0; i < lines.length; i += batchSize) {
                let batch = lines.slice(i, i + batchSize);
                let batchPromises = batch.map(async (currentLine) => {
                    let uidMatch = currentLine.match(/^(\\d+)/); 
                    if (uidMatch) {
                        let uid = uidMatch[1];
                        let status = await checkUID(uid);
                        if (status === "LIVE") {
                            outLive.value += currentLine + "\\n";
                            liveCount++; countLiveEl.innerText = liveCount;
                        } else {
                            let failReason = status !== "DEAD" ? ` [${status}]` : "";
                            outDead.value += currentLine + failReason + "\\n";
                            deadCount++; countDeadEl.innerText = deadCount;
                        }
                    } else {
                        outDead.value += currentLine + " [FORMAT_SALAH]\\n";
                        deadCount++; countDeadEl.innerText = deadCount;
                    }
                });

                await Promise.all(batchPromises);
                let processed = Math.min(i + batchSize, lines.length);
                statusInfo.innerHTML = `⏳ Sedang memproses ${processed} dari ${lines.length} data...`;
                outLive.scrollTop = outLive.scrollHeight; outDead.scrollTop = outDead.scrollHeight;
            }
            btnStart.disabled = false;
            btnStart.innerText = "⚡ Mulai Cek Status UID";
            statusInfo.innerHTML = `✅ Selesai memproses ${lines.length} data.`;
        });

        function copyText(elementId) {
            let textarea = document.getElementById(elementId);
            textarea.select();
            document.execCommand("copy");
            alert("Berhasil disalin!");
        }
    </script>
</body>
</html>
"""

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Saat browser mengakses /api/CEKLIVEUID, Python akan memberikan halaman HTML ini
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(HTML_PAGE.encode('utf-8'))
