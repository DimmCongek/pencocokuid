from http.server import BaseHTTPRequestHandler
import json
import re

def extract_facebook_uid(cookie_string):
    """Mengekstrak UID (c_user) dari string cookie."""
    match = re.search(r'c_user=(\d+)', cookie_string)
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
            <title>EKSTRAKTOR UID FACEBOOK</title>
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

                .container {
                    max-width: 850px; 
                    margin: 0 auto;
                }

                .header-title {
                    text-align: center;
                    font-size: 2rem;
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

                label {
                    display: block;
                    font-weight: 600;
                    margin-bottom: 6px;
                    font-size: 0.9rem;
                }

                textarea {
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
                    resize: none; 
                    height: 200px;
                    margin-bottom: 15px;
                }
                
                textarea::placeholder {
                    color: rgba(148, 163, 184, 0.5);
                }

                textarea:focus {
                    outline: none;
                    border-color: var(--accent);
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
                
                #resultText {
                    height: 200px;
                    background: rgba(0, 0, 0, 0.3);
                    border-color: rgba(16, 185, 129, 0.3);
                    margin-bottom: 0;
                }

                .nav-back {
                    display: inline-block;
                    margin-bottom: 20px;
                    color: var(--accent);
                    text-decoration: none;
                    font-weight: 600;
                    font-size: 0.9rem;
                }
                .nav-back:hover {
                    text-decoration: underline;
                }

            </style>
        </head>
        <body>
            <div class="container">
                <a href="/" class="nav-back">← Kembali ke Dashboard</a>
                <h1 class="header-title">EKSTRAKTOR UID FACEBOOK</h1>
                <p class="header-subtitle">Ambil c_user dari raw cookies dalam hitungan detik</p>

                <div class="glass-panel">
                    <form id="extractForm">
                        <label>🍪 Cookies Mentahan (Raw)</label>
                        <textarea id="cookiesInput" placeholder="Tempel raw cookies di sini...&#10;Satu cookie per baris" required></textarea>
                        
                        <button type="submit" id="submitBtn" class="action-btn">🚀 Ekstrak UID Sekarang</button>
                    </form>
                </div>

                <!-- Bagian Hasil -->
                <div id="resultSection" class="glass-panel">
                    <div class="result-header">
                        <div>
                            <span style="font-size: 1.1rem; font-weight: 600; margin-right: 10px;">Hasil Ekstrak</span>
                            <span id="matchCount" class="status-badge">0 UID</span>
                        </div>
                        <button id="copyBtn" class="copy-btn">📋 Salin Hasil</button>
                    </div>
                    <textarea id="resultText" readonly placeholder="Menunggu proses ekstraksi..."></textarea>
                </div>
            </div>

            <script>
                document.getElementById('extractForm').addEventListener('submit', async (e) => {
                    e.preventDefault();
                    
                    const btn = document.getElementById('submitBtn');
                    const originalText = btn.innerHTML;
                    btn.innerHTML = '⏳ Mengekstrak...';
                    btn.disabled = true;
                    
                    const payload = {
                        cookies: document.getElementById('cookiesInput').value
                    };

                    try {
                        const response = await fetch('/api/EKSTRAKUID', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(payload)
                        });
                        
                        const data = await response.json();
                        
                        document.getElementById('resultText').value = data.hasil;
                        document.getElementById('matchCount').innerText = `${data.jumlah} UID`;
                        
                        document.getElementById('resultSection').scrollIntoView({ behavior: 'smooth' });

                    } catch (error) {
                        alert('Terjadi kesalahan saat memproses data.');
                        console.error(error);
                    } finally {
                        btn.innerHTML = originalText;
                        btn.disabled = false;
                    }
                });

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
            
        raw_cookies = parsed_data.get('cookies', '')

        # --- LOGIKA EKSTRAKSI SEPERTI CUSER.PY ---
        extracted_uids = [] 
        
        for line in raw_cookies.splitlines():
            clean_line = line.strip()
            if clean_line:
                uid = extract_facebook_uid(clean_line)
                if uid:
                    extracted_uids.append(uid)
        
        self.send_response(200)
        self._send_cors_headers()
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response_data = {
            "status": "success",
            "jumlah": len(extracted_uids),
            "hasil": "\n".join(extracted_uids)
        }
        self.wfile.write(json.dumps(response_data).encode('utf-8'))
