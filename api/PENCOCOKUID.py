from http.server import BaseHTTPRequestHandler
import json
import re
from urllib.parse import parse_qs

def get_uid_from_cookie(cookie_str):
    """Mengekstrak UID (c_user) dari string cookie."""
    match = re.search(r'c_user=(\d+)', cookie_str)
    return match.group(1) if match else None

class handler(BaseHTTPRequestHandler):
    
    # Mengizinkan akses dari website manapun (CORS)
    def _send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    # Menangani pre-flight request untuk CORS
    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    # Menangani tampilan GET (saat orang baru membuka URL web)
    def do_GET(self):
        self.send_response(200)
        self._send_cors_headers()
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        # Tampilan Form Sederhana HTML
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Tool Pencocok UID & Cookies Facebook</title>
            <style>
                body { font-family: sans-serif; padding: 20px; max-width: 800px; margin: 0 auto;}
                textarea { width: 100%; height: 150px; margin-bottom: 10px; }
                button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
                button:hover { background: #0056b3; }
            </style>
        </head>
        <body>
            <h2>Tool Pencocok UID & Cookies Facebook</h2>
            <form method="POST" action="/api/PENCOCOKUID">
                <label><b>Daftar UID (satu per baris, format: UID atau UID|PASS):</b></label><br>
                <textarea name="uids" placeholder="Contoh:\n10008xxxx\n10009xxxx|password123"></textarea><br>
                
                <label><b>Daftar Cookies Mentahan (satu per baris):</b></label><br>
                <textarea name="cookies" placeholder="Tempel semua raw cookies di sini..."></textarea><br>
                
                <label><b>Password Default (Opsional):</b></label><br>
                <input type="text" name="global_password" placeholder="Masukkan password" style="width: 100%; padding: 8px; margin-bottom: 10px;"><br>
                
                <button type="submit">Cocokkan Sekarang</button>
            </form>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode('utf-8'))

    # Menangani saat tombol "Cocokkan Sekarang" ditekan (POST)
    def do_POST(self):
        # Ambil panjang data yang dikirim
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        # Parsing data yang dikirim dari form
        parsed_data = parse_qs(post_data)
        
        raw_uids = parsed_data.get('uids', [''])[0]
        raw_cookies = parsed_data.get('cookies', [''])[0]
        global_password = parsed_data.get('global_password', [''])[0].strip()

        # --- LOGIKA PENCOCOKAN ---
        cookie_dict = {}
        # Proses setiap baris cookie
        for c_str in raw_cookies.splitlines():
            c_str = c_str.strip()
            if c_str:
                uid_dari_cookie = get_uid_from_cookie(c_str)
                if uid_dari_cookie:
                    cookie_dict[uid_dari_cookie] = c_str
        
        hasil_match = []
        matched_count = 0
        
        # Proses setiap baris UID
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
        
        # --- TAMPILKAN HASILNYA KE LAYAR ---
        self.send_response(200)
        self._send_cors_headers()
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        hasil_text = "\n".join(hasil_match)
        
        html_result = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Hasil Pencocokan</title>
            <style>
                body {{ font-family: sans-serif; padding: 20px; max-width: 800px; margin: 0 auto;}}
                textarea {{ width: 100%; height: 300px; }}
                a {{ display: inline-block; margin-top: 10px; padding: 10px 20px; background: #28a745; color: white; text-decoration: none; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <h2>Proses Selesai!</h2>
            <p>Berhasil mencocokkan: <b>{matched_count} Akun</b></p>
            <textarea readonly>{hasil_text}</textarea><br>
            <a href="/api/PENCOCOKUID">Kembali ke Awal</a>
        </body>
        </html>
        """
        self.wfile.write(html_result.encode('utf-8'))
