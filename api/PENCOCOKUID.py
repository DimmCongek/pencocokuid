from http.server import BaseHTTPRequestHandler
import json
import re

def get_uid_from_cookie(cookie_str):
    """Mengekstrak UID (c_user) dari string cookie."""
    match = re.search(r'c_user=(\d+)', cookie_str)
    return match.group(1) if match else None

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
            <title>PENCOCOK UID & COOKIES</title>
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
                }
                
                body {
                    font-family: 'Inter', sans-serif;
                    background-color: var(--bg-dark);
                    background-image: 
                        radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.15) 0px, transparent 50%),
                        radial-gradient(at 100% 100%, rgba(16, 185, 129, 0.1) 0px, transparent 50%);
                    color: var(--text-main);
                    margin: 0;
                    padding: 30px 15px;
                    min-height: 100vh;
                    box-sizing: border-box;
                }

                /* Mengubah max-width agar lebih kecil / compact */
                .container {
                    max-width: 850px; 
                    margin: 0 auto;
                }

                .header-title {
                    text-align: center;
                    font-size: 2rem; /* Ukuran font diperkecil sedikit */
                    font-weight: 800;
                    margin-bottom: 5px;
                    background: linear-gradient(to right, #60a5fa, #34d399);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                }
                
                .header-subtitle {
                    text-align: center;
                    color: var(--text-muted);
                    margin-bottom: 30px;
                    font-size: 0.9rem;
                }

                .glass-panel {
                    background: var(--panel-bg);
                    backdrop-filter: blur(12px);
                    -webkit-backdrop-filter: blur(12px);
                    border: 1px solid var(--border);
                    border-radius: 12px;
                    padding: 20px;
                    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
                    margin-bottom: 20px;
                }

                .grid-2col {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 15px; /* Jarak antar kolom diperkecil */
                    margin-bottom: 15px;
                }

                @media (max-width: 768px) {
                    .grid-2col {
                        grid-template-columns: 1fr;
                    }
                }

                label {
                    display: block;
                    font-weight: 600;
                    margin-bottom: 6px;
                    font-size: 0.9rem;
                }

                textarea, input {
                    width: 100%;
                    background: rgba(15, 23, 42, 0.6);
                    border: 1px solid var(--border);
                    color: var(--text-main);
                    border-radius: 6px;
                    padding: 10px;
                    font-family: monospace;
                    font-size: 0.85rem;
                    box-sizing: border-box;
                    transition: border-color 0.3s ease;
                    /* KUNCI UKURAN TEXTAREA */
                    resize: none; 
                }
                
                textarea::placeholder, input::placeholder {
                    color: rgba(148, 163, 184, 0.5);
                }

                textarea:focus, input:focus {
                    outline: none;
                    border-color: var(--accent);
                }

                /* Tinggi textarea diperkecil sedikit */
                textarea {
                    height: 180px;
                }

                .action-btn {
                    width: 100%;
                    background: var(--accent);
                    color: white;
                    border: none;
                    padding: 12px;
                    font-size: 1rem;
                    font-weight: 600;
                    border-radius: 6px;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 14px rgba(59, 130, 246, 0.4);
                }

                .action-btn:hover {
                    background: var(--accent-hover);
                    transform: translateY(-2px);
                }

                .action-btn:disabled {
                    background: var(--text-muted);
                    cursor: not-allowed;
                    transform: none;
                    box-shadow: none;
                }
                
                .result-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 10px;
                }
                
                .status-badge {
                    background: rgba(16, 185, 129, 0.2);
                    color: var(--success);
                    padding: 4px 10px;
                    border-radius: 12px;
                    font-size: 0.8rem;
                    font-weight: 600;
                    border: 1px solid rgba(16, 185, 129, 0.3);
                }

                .copy-btn {
                    background: rgba(255,255,255,0.1);
                    color: var(--text-main);
                    border: 1px solid var(--border);
                    padding: 6px 12px;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 0.85rem;
                    font-weight: 600;
                    transition: all 0.2s ease;
                }

                .copy-btn:hover {
                    background: rgba(255,255,255,0.2);
                }
                
                .copy-btn.copied {
                    background: var(--success);
                    border-color: var(--success);
                }
                
                /* Textarea hasil dibuat lebih pendek */
                #resultText {
                    height: 150px;
                    background: rgba(0, 0, 0, 0.3);
                    border-color: rgba(16, 185, 129, 0.3);
                }

            </style>
        </head>
        <body>
            <div class="container">
                <h1 class="header-title">PENCOCOK UID & COOKIES</h1>
                <p class="header-subtitle">Alat pemrosesan cepat dan aman</p>

                <div class="glass-panel">
                    <form id="matchForm">
                        <div class="grid-2col">
                            <!-- Kolom Kiri: Cookies (Sesuai Permintaan) -->
                            <div>
                                <label>🍪 Cookies</label>
                                <textarea id="cookiesInput" placeholder="Tempel raw cookies di sini...&#10;Satu cookie per baris" required></textarea>
                            </div>
                            
                            <!-- Kolom Kanan: UID (Sesuai Permintaan) -->
                            <div>
                                <label>👤 UID</label>
                                <textarea id="uidsInput" placeholder="Contoh:&#10;10008xxxx&#10;10009xxxx|password123&#10;&#10;Satu per baris" required></textarea>
                            </div>
                        </div>

                        <div style="margin-bottom: 15px;">
                            <label>🔑 Password (Opsional)</label>
                            <input type="text" id="globalPassword" placeholder="Akan digunakan jika UID tidak memiliki password">
                        </div>

                        <button type="submit" id="submitBtn" class="action-btn">🚀 Cocokkan Sekarang</button>
                    </form>
                </div>

                <!-- Bagian Hasil (Selalu Ditampilkan dari awal) -->
                <div id="resultSection" class="glass-panel">
                    <div class="result-header">
                        <div>
                            <span style="font-size: 1.1rem; font-weight: 600; margin-right: 10px;">Hasil Pencocokan</span>
                            <span id="matchCount" class="status-badge">0 Akun</span>
                        </div>
                        <button id="copyBtn" class="copy-btn">📋 Salin Hasil</button>
                    </div>
                    <textarea id="resultText" readonly placeholder="Menunggu proses pencocokan..."></textarea>
                </div>
            </div>

            <script>
                document.getElementById('matchForm').addEventListener('submit', async (e) => {
                    e.preventDefault();
                    
                    const btn = document.getElementById('submitBtn');
                    const originalText = btn.innerHTML;
                    btn.innerHTML = '⏳ Memproses...';
                    btn.disabled = true;
                    
                    const payload = {
                        uids: document.getElementById('uidsInput').value,
                        cookies: document.getElementById('cookiesInput').value,
                        global_password: document.getElementById('globalPassword').value
                    };

                    try {
                        const response = await fetch('/api/PENCOCOKUID', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(payload)
                        });
                        
                        const data = await response.json();
                        
                        document.getElementById('resultText').value = data.hasil;
                        document.getElementById('matchCount').innerText = `${data.jumlah} Akun`;
                        
                        // Scroll pelan ke hasil
                        document.getElementById('resultSection').scrollIntoView({ behavior: 'smooth' });

                    } catch (error) {
                        alert('Terjadi kesalahan saat memproses data.');
                        console.error(error);
                    } finally {
                        btn.innerHTML = originalText;
                        btn.disabled = false;
                    }
                });

                // Fungsi Tombol Copy
                document.getElementById('copyBtn').addEventListener('click', function() {
                    const resultText = document.getElementById('resultText');
                    if (!resultText.value) return;
                    
                    resultText.select();
                    document.execCommand('copy');
                    
                    const btn = this;
                    const originalText = btn.innerHTML;
                    btn.innerHTML = '✅ Disalin!';
                    btn.classList.add('copied');
                    
                    setTimeout(() => {
                        btn.innerHTML = originalText;
                        btn.classList.remove('copied');
                    }, 2000);
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
        raw_cookies = parsed_data.get('cookies', '')
        global_password = parsed_data.get('global_password', '').strip()

        cookie_dict = {}
        for c_str in raw_cookies.splitlines():
            c_str = c_str.strip()
            if c_str:
                uid_dari_cookie = get_uid_from_cookie(c_str)
                if uid_dari_cookie:
                    cookie_dict[uid_dari_cookie] = c_str
        
        hasil_match = []
        matched_count = 0
        
        for line in raw_uids.splitlines():
            line_clean = line.strip()
            if not line_clean:
                continue
                
            parts = line_clean.split('|')
            uid_target = parts[0].strip()
            
            if len(parts) > 1 and parts[1].strip() != "":
                password_to_use = parts[1].strip()
            else:
                password_to_use = global_password
                
            if uid_target in cookie_dict:
                matched_cookie = cookie_dict[uid_target]
                hasil_line = f"{uid_target}|{password_to_use}|{matched_cookie}"
                hasil_match.append(hasil_line)
                matched_count += 1
        
        self.send_response(200)
        self._send_cors_headers()
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response_data = {
            "status": "success",
            "jumlah": matched_count,
            "hasil": "\n".join(hasil_match)
        }
        self.wfile.write(json.dumps(response_data).encode('utf-8'))
