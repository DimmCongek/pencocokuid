from http.server import BaseHTTPRequestHandler
import json
import re
import requests

def check_facebook_uid(uid):
    url = f"https://www.facebook.com/profile.php?id={uid}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    try:
        # Timeout diatur cepat (3 detik) agar tidak memakan batas waktu Vercel
        response = requests.get(url, headers=headers, timeout=3)
        if response.status_code == 200:
            return "LIVE"
        elif response.status_code == 404:
            return "DEAD"
        else:
            return "UNKNOWN"
    except requests.exceptions.RequestException:
        return "ERROR"

class handler(BaseHTTPRequestHandler):
    
    def _send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self._send_cors_headers()
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html_content = """
        <!DOCTYPE html>
        <html lang="id">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>CEK LIVE UID FACEBOOK</title>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
            <style>
                :root {
                    --bg-dark: #0f172a;
                    --panel-bg: rgba(30, 41, 59, 0.7);
                    --accent: #3b82f6;
                    --accent-hover: #2563eb;
                    --text-main: #f8fafc;
                    --text-muted: #94a3b8;
                    --border: rgba(255, 255, 255, 0.1);
                    --success: #10b981;
                    --danger: #ef4444;
                }
                
                body { font-family: 'Inter', sans-serif; background-color: var(--bg-dark); color: var(--text-main); margin: 0; padding: 30px 15px; min-height: 100vh; box-sizing: border-box; }
                .container { max-width: 850px; margin: 0 auto; }
                .header-title { text-align: center; font-size: 2rem; font-weight: 800; margin-bottom: 5px; background: linear-gradient(to right, #60a5fa, #34d399); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
                .header-subtitle { text-align: center; color: var(--text-muted); margin-bottom: 30px; font-size: 0.9rem; }
                .glass-panel { background: var(--panel-bg); backdrop-filter: blur(12px); border: 1px solid var(--border); border-radius: 12px; padding: 20px; margin-bottom: 20px; }
                label { display: block; font-weight: 600; margin-bottom: 6px; font-size: 0.9rem; }
                textarea { width: 100%; background: rgba(15, 23, 42, 0.6); border: 1px solid var(--border); color: var(--text-main); border-radius: 6px; padding: 10px; font-family: monospace; font-size: 0.85rem; box-sizing: border-box; transition: border-color 0.3s ease; resize: none; margin-bottom: 15px; }
                textarea:focus { outline: none; border-color: var(--accent); }
                .action-btn { width: 100%; background: var(--accent); color: white; border: none; padding: 12px; font-size: 1rem; font-weight: 600; border-radius: 6px; cursor: pointer; transition: all 0.3s ease; }
                .action-btn:hover { background: var(--accent-hover); }
                .action-btn:disabled { background: var(--text-muted); cursor: not-allowed; }
                .nav-back { display: inline-block; margin-bottom: 20px; color: var(--accent); text-decoration: none; font-weight: 600; font-size: 0.9rem; }
                .nav-back:hover { text-decoration: underline; }
                .grid-2col { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
                .badge-live { background: rgba(16, 185, 129, 0.2); color: var(--success); padding: 4px 10px; border-radius: 12px; font-size: 0.8rem; font-weight: 600; border: 1px solid rgba(16, 185, 129, 0.3); }
                .badge-dead { background: rgba(239, 68, 68, 0.2); color: var(--danger); padding: 4px 10px; border-radius: 12px; font-size: 0.8rem; font-weight: 600; border: 1px solid rgba(239, 68, 68, 0.3); }
                .warning-box { background: rgba(234, 179, 8, 0.1); border: 1px solid rgba(234, 179, 8, 0.3); color: #facc15; padding: 10px; border-radius: 8px; font-size: 0.85rem; margin-bottom: 15px; }
                @media (max-width: 768px) { .grid-2col { grid-template-columns: 1fr; } }
            </style>
        </head>
        <body>
            <div class="container">
                <a href="/" class="nav-back">← Kembali ke Dashboard</a>
                <h1 class="header-title">CEK LIVE UID</h1>
                <p class="header-subtitle">Verifikasi status profil secara real-time</p>

                <div class="glass-panel">
                    <div class="warning-box">
                        ⚠️ <b>Perhatian:</b> Karena server Vercel memiliki batas waktu maksimal 10 detik, <b>jangan memasukkan lebih dari 10-15 UID sekaligus</b> agar sistem tidak mengalami timeout.
                    </div>
                    <form id="checkForm">
                        <label>👤 Daftar UID (Bisa format UID saja atau UID|PASS)</label>
                        <textarea id="uidsInput" style="height: 150px;" placeholder="10008xxxx&#10;10009xxxx|password123" required></textarea>
                        <button type="submit" id="submitBtn" class="action-btn">⚡ Cek Status UID</button>
                    </form>
                </div>

                <div id="resultSection" class="glass-panel" style="display: none;">
                    <div class="grid-2col">
                        <div>
                            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                                <label>✅ HASIL LIVE</label>
                                <span id="countLive" class="badge-live">0</span>
                            </div>
                            <textarea id="resultLive" style="height: 200px; border-color: rgba(16, 185, 129, 0.3);" readonly></textarea>
                        </div>
                        <div>
                            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                                <label>❌ HASIL DEAD</label>
                                <span id="countDead" class="badge-dead">0</span>
                            </div>
                            <textarea id="resultDead" style="height: 200px; border-color: rgba(239, 68, 68, 0.3);" readonly></textarea>
                        </div>
                    </div>
                </div>
            </div>

            <script>
                document.getElementById('checkForm').addEventListener('submit', async (e) => {
                    e.preventDefault();
                    const btn = document.getElementById('submitBtn');
                    btn.innerHTML = '⏳ Mengecek Status Server...';
                    btn.disabled = true;
                    document.getElementById('resultSection').style.display = 'block';
                    document.getElementById('resultLive').value = "Memproses...";
                    document.getElementById('resultDead').value = "Memproses...";
                    
                    const payload = { uids: document.getElementById('uidsInput').value };

                    try {
                        const response = await fetch('/api/CEKLIVEUID', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(payload)
                        });
                        const data = await response.json();
                        
                        document.getElementById('resultLive').value = data.hasil_live;
                        document.getElementById('resultDead').value = data.hasil_dead;
                        document.getElementById('countLive').innerText = data.live_count;
                        document.getElementById('countDead').innerText = data.dead_count;
                        
                    } catch (error) {
                        alert('Terjadi kesalahan atau Time Out! Coba kurangi jumlah baris UID.');
                    } finally {
                        btn.innerHTML = '⚡ Cek Status UID';
                        btn.disabled = false;
                    }
                });
            </script>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        try:
            parsed_data = json.loads(post_data)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            return
            
        raw_uids = parsed_data.get('uids', '')

        hasil_live = []
        hasil_dead = []
        
        # Proses Pengecekan
        for line in raw_uids.splitlines():
            clean_line = line.strip()
            if not clean_line:
                continue
                
            # Ambil hanya angka UID dari depan (mendukung input "UID|PASS" atau hanya "UID")
            match = re.match(r'^(\d+)', clean_line)
            if match:
                uid = match.group(1)
                status = check_facebook_uid(uid)
                
                if status == "LIVE":
                    hasil_live.append(clean_line) # Menyimpan kembali beserta passwordnya jika ada
                else:
                    hasil_dead.append(clean_line)
        
        self.send_response(200)
        self._send_cors_headers()
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response_data = {
            "status": "success",
            "live_count": len(hasil_live),
            "dead_count": len(hasil_dead),
            "hasil_live": "\n".join(hasil_live),
            "hasil_dead": "\n".join(hasil_dead)
        }
        self.wfile.write(json.dumps(response_data).encode('utf-8'))
