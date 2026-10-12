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
        
        # UI TEMA FUTURISTIK / CYBERPUNK
        html_content = """
        <!DOCTYPE html>
        <html lang="id">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>PENCOCOK UID & COOKIES</title>
            <!-- Menggunakan font bergaya teknologi -->
            <link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
            <style>
                :root {
                    --bg-dark: #030712;
                    --panel-bg: rgba(17, 24, 39, 0.85);
                    --accent: #0ea5e9;
                    --accent-hover: #38bdf8;
                    --neon-glow: 0 0 10px rgba(14, 165, 233, 0.5), 0 0 20px rgba(14, 165, 233, 0.3);
                    --text-main: #e2e8f0;
                    --text-muted: #64748b;
                    --border: rgba(14, 165, 233, 0.3);
                    --success: #10b981;
                    --success-glow: 0 0 10px rgba(16, 185, 129, 0.5);
                }
                
                body {
                    font-family: 'Rajdhani', sans-serif;
                    background-color: var(--bg-dark);
                    /* Background Grid Pattern */
                    background-image: 
                        linear-gradient(rgba(14, 165, 233, 0.05) 1px, transparent 1px),
                        linear-gradient(90deg, rgba(14, 165, 233, 0.05) 1px, transparent 1px);
                    background-size: 40px 40px;
                    color: var(--text-main);
                    margin: 0;
                    padding: 30px 15px;
                    min-height: 100vh;
                    box-sizing: border-box;
                    overflow-x: hidden;
                }

                /* Animasi Load Masuk */
                @keyframes fadeInUp {
                    from { opacity: 0; transform: translateY(30px); }
                    to { opacity: 1; transform: translateY(0); }
                }

                /* Animasi Memproses Data */
                @keyframes pulseBorder {
                    0% { border-color: rgba(14, 165, 233, 0.3); }
                    50% { border-color: rgba(14, 165, 233, 0.8); box-shadow: var(--neon-glow); }
                    100% { border-color: rgba(14, 165, 233, 0.3); }
                }

                .container {
                    max-width: 850px; 
                    margin: 0 auto;
                    animation: fadeInUp 0.8s ease-out forwards;
                }

                .header-title {
                    text-align: center;
                    font-size: 2.8rem;
                    font-weight: 700;
                    margin-bottom: 5px;
                    color: #fff;
                    text-shadow: var(--neon-glow);
                    letter-spacing: 2px;
                }
                
                .header-subtitle {
                    text-align: center;
                    color: var(--accent);
                    margin-bottom: 30px;
                    font-size: 1rem;
                    letter-spacing: 2px;
                    text-transform: uppercase;
                }

                .glass-panel {
                    background: var(--panel-bg);
                    backdrop-filter: blur(10px);
                    -webkit-backdrop-filter: blur(10px);
                    border: 1px solid var(--border);
                    border-radius: 12px;
                    padding: 20px;
                    margin-bottom: 20px;
                    position: relative;
                    overflow: hidden;
                    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
                    transition: all 0.3s ease;
                }
                
                .glass-panel:hover {
                    border-color: var(--accent);
                    box-shadow: var(--neon-glow);
                }

                /* Animasi Scanline (Garis Pemindai) di dalam kotak */
                .glass-panel::before {
                    content: "";
                    position: absolute;
                    top: -100%;
                    left: 0;
                    width: 100%;
                    height: 3px;
                    background: var(--accent);
                    box-shadow: 0 0 15px var(--accent);
                    opacity: 0.5;
                    animation: scan 4s linear infinite;
                    pointer-events: none;
                }

                @keyframes scan {
                    0% { top: -10px; opacity: 0; }
                    10% { opacity: 0.5; }
                    90% { opacity: 0.5; }
                    100% { top: 100%; opacity: 0; }
                }

                .grid-2col {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 15px;
                    margin-bottom: 15px;
                }

                @media (max-width: 768px) {
                    .grid-2col {
                        grid-template-columns: 1fr;
                    }
                }

                label {
                    display: block;
                    font-weight: 700;
                    margin-bottom: 6px;
                    font-size: 1.1rem;
                    color: var(--accent);
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }

                textarea, input {
                    width: 100%;
                    background: rgba(3, 7, 18, 0.8);
                    border: 1px solid var(--border);
                    color: var(--accent-hover);
                    border-radius: 6px;
                    padding: 10px;
                    font-family: 'Share Tech Mono', monospace;
                    font-size: 0.95rem;
                    box-sizing: border-box;
                    transition: all 0.3s ease;
                    resize: none; 
                }
                
                textarea::placeholder, input::placeholder {
                    color: rgba(100, 116, 139, 0.5);
                }

                textarea:focus, input:focus {
                    outline: none;
                    border-color: var(--accent);
                    box-shadow: inset 0 0 10px rgba(14, 165, 233, 0.2), var(--neon-glow);
                }

                textarea {
                    height: 180px;
                }

                /* Tombol Animasi Futuristik */
                .action-btn {
                    width: 100%;
                    background: transparent;
                    color: var(--accent);
                    border: 2px solid var(--accent);
                    padding: 14px;
                    font-size: 1.3rem;
                    font-weight: 700;
                    border-radius: 6px;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    text-transform: uppercase;
                    letter-spacing: 2px;
                    font-family: 'Rajdhani', sans-serif;
                    position: relative;
                    overflow: hidden;
                }

                .action-btn::before {
                    content: '';
                    position: absolute;
                    top: 0; left: -100%;
                    width: 100%; height: 100%;
                    background: linear-gradient(90deg, transparent, rgba(14, 165, 233, 0.4), transparent);
                    transition: all 0.4s ease;
                }

                .action-btn:hover::before {
                    left: 100%;
                }

                .action-btn:hover {
                    background: var(--accent);
                    color: #fff;
                    box-shadow: var(--neon-glow);
                }

                .action-btn:disabled {
                    border-color: var(--text-muted);
                    color: var(--text-muted);
                    cursor: not-allowed;
                    box-shadow: none;
                }
                .action-btn:disabled:hover {
                    background: transparent;
                }
                
                .result-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 10px;
                }
                
                .status-badge {
                    background: rgba(16, 185, 129, 0.1);
                    color: var(--success);
                    padding: 4px 12px;
                    border-radius: 4px;
                    font-size: 1rem;
                    font-weight: 700;
                    border: 1px solid var(--success);
                    box-shadow: var(--success-glow);
                    font-family: 'Share Tech Mono', monospace;
                }

                .copy-btn {
                    background: transparent;
                    color: var(--accent);
                    border: 1px solid var(--accent);
                    padding: 6px 15px;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 1rem;
                    font-weight: 700;
                    transition: all 0.2s ease;
                    text-transform: uppercase;
                    font-family: 'Rajdhani', sans-serif;
                }

                .copy-btn:hover {
                    background: var(--accent);
                    color: #fff;
                    box-shadow: var(--neon-glow);
                }
                
                .copy-btn.copied {
                    background: var(--success);
                    border-color: var(--success);
                    color: #fff;
                    box-shadow: var(--success-glow);
                }
                
                #resultText {
                    height: 150px;
                    background: rgba(3, 7, 18, 0.9);
                    border-color: rgba(16, 185, 129, 0.5);
                    color: var(--success);
                }
                
                /* Efek kedip saat hasil memproses */
                .typing-active {
                    animation: pulseBorder 1s infinite;
                }

            </style>
        </head>
        <body>
            <div class="container">
                <h1 class="header-title">PENCOCOK UID & COOKIES</h1>
                <p class="header-subtitle">/// TERMINAL PROTOCOL INITIATED ///</p>

                <div class="glass-panel">
                    <form id="matchForm">
                        <div class="grid-2col">
                            <!-- Kolom Kiri: UID (SESUAI PERMINTAAN) -->
                            <div>
                                <label>👤 UID</label>
                                <textarea id="uidsInput" placeholder="> Input UID array...&#10;> 10008xxxx&#10;> 10009xxxx|password123&#10;&#10;> 1 data per baris" required></textarea>
                            </div>
                            
                            <!-- Kolom Kanan: Cookies (SESUAI PERMINTAAN) -->
                            <div>
                                <label>🍪 Cookies</label>
                                <textarea id="cookiesInput" placeholder="> Input RAW cookies...&#10;> c_user=...&#10;&#10;> 1 data per baris" required></textarea>
                            </div>
                        </div>

                        <div style="margin-bottom: 15px;">
                            <label>🔑 Password (Opsional)</label>
                            <input type="text" id="globalPassword" placeholder="> Set default password override...">
                        </div>

                        <button type="submit" id="submitBtn" class="action-btn">EXECUTE_MATCH()</button>
                    </form>
                </div>

                <!-- Bagian Hasil -->
                <div id="resultSection" class="glass-panel">
                    <div class="result-header">
                        <div>
                            <span style="font-size: 1.2rem; font-weight: 700; margin-right: 10px; color: var(--accent); text-transform: uppercase;">[OUTPUT_LOG]</span>
                            <span id="matchCount" class="status-badge">0 MATCH</span>
                        </div>
                        <button id="copyBtn" class="copy-btn">COPY_DATA</button>
                    </div>
                    <textarea id="resultText" readonly placeholder="> Standby for execution..."></textarea>
                </div>
            </div>

            <script>
                document.getElementById('matchForm').addEventListener('submit', async (e) => {
                    e.preventDefault();
                    
                    const btn = document.getElementById('submitBtn');
                    const originalText = btn.innerHTML;
                    btn.innerHTML = 'PROCESSING...';
                    btn.disabled = true;
                    
                    // Efek proses di kolom result
                    const resultTextarea = document.getElementById('resultText');
                    resultTextarea.classList.add('typing-active');
                    resultTextarea.value = '> Executing matching algorithm...\n> Extracting UID from Cookies...\n> Please wait...';
                    
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
                        
                        // Sedikit delay agar efek animasi processing terlihat
                        setTimeout(() => {
                            resultTextarea.classList.remove('typing-active');
                            resultTextarea.value = data.hasil || '> No matches found in database.';
                            document.getElementById('matchCount').innerText = `${data.jumlah} MATCH`;
                        }, 800); 

                    } catch (error) {
                        alert('SYSTEM ERROR: Execution failed.');
                        console.error(error);
                        resultTextarea.classList.remove('typing-active');
                        resultTextarea.value = '> ERROR OCCURRED.';
                    } finally {
                        setTimeout(() => {
                            btn.innerHTML = originalText;
                            btn.disabled = false;
                        }, 800);
                    }
                });

                // Fungsi Tombol Copy
                document.getElementById('copyBtn').addEventListener('click', function() {
                    const resultText = document.getElementById('resultText');
                    if (!resultText.value || resultText.value.startsWith('>')) return;
                    
                    resultText.select();
                    document.execCommand('copy');
                    
                    const btn = this;
                    const originalText = btn.innerHTML;
                    btn.innerHTML = 'COPIED!';
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
