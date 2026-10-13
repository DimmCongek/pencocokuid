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
        # Timeout diset 5 detik, jika 1 profil tidak bisa diakses, langsung anggap gagal agar cepat
        response = requests.get(url, headers=headers, timeout=5)
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
                .glass-panel { background: var(--panel-bg); backdrop-filter: blur(12px); border: 1px solid var(--border); border-radius: 12px; padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1); }
                label { display: block; font-weight: 600; font-size: 0.9rem; }
                
                textarea { width: 100%; background: rgba(15, 23, 42, 0.6); border: 1px solid var(--border); color: var(--text-main); border-radius: 6px; padding: 10px; font-family: monospace; font-size: 0.85rem; box-sizing: border-box; transition: border-color 0.3s ease; resize: none; margin-bottom: 15px; margin-top: 10px; }
                textarea:focus { outline: none; border-color: var(--accent); }
                
                .action-btn { width: 100%; background: var(--accent); color: white; border: none; padding: 14px; font-size: 1rem; font-weight: 600; border-radius: 6px; cursor: pointer; transition: all 0.3s ease; box-shadow: 0 4px 14px rgba(59, 130, 246, 0.4); }
                .action-btn:hover { background: var(--accent-hover); transform: translateY(-2px); }
                .action-btn:disabled { background: var(--text-muted); cursor: not-allowed; transform: none; box-shadow: none; color: #fff; }
                
                .nav-back { display: inline-block; margin-bottom: 20px; color: var(--accent); text-decoration: none; font-weight: 600; font-size: 0.9rem; }
                .nav-back:hover { text-decoration: underline; }
                .grid-2col { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
                
                /* Badge Counters */
                .badge-live { background: rgba(16, 185, 129, 0.2); color: var(--success); padding: 4px 10px; border-radius: 12px; font-size: 0.85rem; font-weight: 700; border: 1px solid rgba(16, 185, 129, 0.3); }
                .badge-dead { background: rgba(239, 68, 68, 0.2); color: var(--danger); padding: 4px 10px; border-radius: 12px; font-size: 0.85rem; font-weight: 700; border: 1px solid rgba(239, 68, 68, 0.3); }
                
                /* Info Box */
                .info-box { background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.3); color: #60a5fa; padding: 12px; border-radius: 8px; font-size: 0.85rem; margin-bottom: 15px; line-height: 1.5; }
                
                /* Copy Buttons */
                .copy-btn { background: rgba(255,255,255,0.05); color: var(--text-main); border: 1px solid var(--border); padding: 4px 10px; border-radius: 4px; cursor: pointer; font-size: 0.75rem; font-weight: 600; transition: all 0.2s ease; margin-left: auto; }
                .copy-btn:hover { background: rgba(255,255,255,0.15); }
                .copy-btn.copied { background: var(--success); border-color: var(--success); color: white; }
                
                .result-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 5px; }
                
                @media (max-width: 768px) { .grid-2col { grid-template-columns: 1fr; } }
            </style>
        </head>
        <body>
            <div class="container">
                <a href="/" class="nav-back">← Kembali ke Dashboard</a>
                <h1 class="header-title">CEK LIVE UID</h1>
                <p class="header-subtitle">Verifikasi status profil secara real-time</p>

                <div class="glass-panel">
                    <div class="info-box">
                        🚀 <b>Sistem Cepat Terintegrasi:</b> Proses pengecekan dilakukan <b>satu per satu secara otomatis</b> agar tidak terjadi server <i>timeout</i>. Anda aman memasukkan ratusan data sekaligus.
                    </div>
                    <form id="checkForm">
                        <label>👤 Daftar UID (Bisa format UID saja atau UID|PASS)</label>
                        <textarea id="uidsInput" style="height: 150px;" placeholder="10008xxxx&#10;10009xxxx|password123&#10;&#10;Satu data per baris" required></textarea>
                        <button type="submit" id="submitBtn" class="action-btn">⚡ Mulai Cek Status UID</button>
                    </form>
                </div>

                <div id="resultSection" class="glass-panel" style="display: none;">
                    <!-- Area Progress Bar (Teks) -->
                    <div id="progressText" style="text-align: center; color: var(--accent); font-weight: 600; margin-bottom: 15px; font-size: 0.9rem;"></div>
                    
                    <div class="grid-2col">
                        <!-- Kolom Live -->
                        <div>
                            <div class="result-header">
                                <label style="margin: 0; color: var(--success);">✅ HASIL LIVE <span id="countLive" class="badge-live" style="margin-left: 8px;">0</span></label>
                                <button type="button" class="copy-btn" onclick="copyResult('resultLive', this)">📋 Salin</button>
                            </div>
                            <textarea id="resultLive" style="height: 250px; border-color: rgba(16, 185, 129, 0.3);" readonly></textarea>
                        </div>
                        
                        <!-- Kolom Dead -->
                        <div>
                            <div class="result-header">
                                <label style="margin: 0; color: var(--danger);">❌ HASIL DEAD <span id="countDead" class="badge-dead" style="margin-left: 8px;">0</span></label>
                                <button type="button" class="copy-btn" onclick="copyResult('resultDead', this)">📋 Salin</button>
                            </div>
                            <textarea id="resultDead" style="height: 250px; border-color: rgba(239, 68, 68, 0.3);" readonly></textarea>
                        </div>
                    </div>
                </div>
            </div>

            <script>
                document.getElementById('checkForm').addEventListener('submit', async (e) => {
                    e.preventDefault();
                    
                    // Ambil data dan saring baris kosong
                    const rawInput = document.getElementById('uidsInput').value;
                    const lines = rawInput.split('\\n').map(line => line.trim()).filter(line => line !== "");
                    
                    if(lines.length === 0) return;

                    const btn = document.getElementById('submitBtn');
                    const progressText = document.getElementById('progressText');
                    
                    btn.disabled = true;
                    document.getElementById('resultSection').style.display = 'block';
                    
                    // Reset UI
                    const liveArea = document.getElementById('resultLive');
                    const deadArea = document.getElementById('resultDead');
                    const countLive = document.getElementById('countLive');
                    const countDead = document.getElementById('countDead');
                    
                    liveArea.value = "";
                    deadArea.value = "";
                    let liveC = 0, deadC = 0;
                    
                    // PROSES SATU PER SATU SECARA ASYNCHRONOUS (Cepat & Anti Timeout)
                    for (let i = 0; i < lines.length; i++) {
                        const currentLine = lines[i];
                        
                        // Update Progress
                        btn.innerHTML = `⏳ Mengecek... (${i + 1} / ${lines.length})`;
                        progressText.innerHTML = `Sedang memproses baris ${i + 1} dari ${lines.length}...`;
                        
                        try {
                            const response = await fetch('/api/CEKLIVEUID', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ line: currentLine })
                            });
                            
                            const data = await response.json();
                            
                            // Distribusikan hasil langsung ke text area secara real-time
                            if (data.status === 'LIVE') {
                                liveArea.value += (liveArea.value ? '\\n' : '') + data.line;
                                liveC++;
                                countLive.innerText = liveC;
                                liveArea.scrollTop = liveArea.scrollHeight; // Auto scroll ke bawah
                            } else {
                                deadArea.value += (deadArea.value ? '\\n' : '') + data.line;
                                deadC++;
                                countDead.innerText = deadC;
                                deadArea.scrollTop = deadArea.scrollHeight;
                            }
                        } catch (error) {
                            // Jika ada error koneksi API, anggap dead atau lewati
                            deadArea.value += (deadArea.value ? '\\n' : '') + currentLine + " [ERROR_KONEKSI]";
                            deadC++;
                            countDead.innerText = deadC;
                        }
                    }

                    // Proses Selesai
                    btn.innerHTML = '⚡ Mulai Cek Status UID';
                    btn.disabled = false;
                    progressText.innerHTML = `✅ Selesai memproses ${lines.length} data.`;
                });

                // FUNGSI COPY
                function copyResult(textareaId, btnObj) {
                    const textarea = document.getElementById(textareaId);
                    if (!textarea.value) return; // Jangan copy jika kosong
                    
                    textarea.select();
                    document.execCommand('copy');
                    
                    // Animasi Tombol
                    const originalText = btnObj.innerHTML;
                    btnObj.innerHTML = '✅ Disalin!';
                    btnObj.classList.add('copied');
                    
                    setTimeout(() => {
                        btnObj.innerHTML = originalText;
                        btnObj.classList.remove('copied');
                    }, 2000);
                }
            </script>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode('utf-8'))

    def do_POST(self):
        """
        Sekarang backend HANYA memproses SATU BARIS per request.
        Ini sangat meringankan server dan menjamin 0% Timeout Vercel.
        """
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        try:
            parsed_data = json.loads(post_data)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            return
            
        line = parsed_data.get('line', '').strip()
        status = "UNKNOWN"
        
        if line:
            # Ambil UID (angka) dari depan string
            match = re.match(r'^(\d+)', line)
            if match:
                uid = match.group(1)
                status = check_facebook_uid(uid)
            else:
                status = "DEAD" # Jika tidak ada format UID di depan, anggap Invalid/Dead
                
        self.send_response(200)
        self._send_cors_headers()
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response_data = {
            "status": status,
            "line": line
        }
        self.wfile.write(json.dumps(response_data).encode('utf-8'))
