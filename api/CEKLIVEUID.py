import json
import asyncio
import aiohttp
from io import BytesIO
from PIL import Image
import re
from http.server import BaseHTTPRequestHandler

# ==========================================
# FUNGSI ASYNC (Sama seperti sebelumnya)
# ==========================================
async def check_uid(session, baris_data):
    match = re.search(r'^(\d+)', baris_data.strip())
    if not match:
        return baris_data, "FORMAT_SALAH"
    
    uid = match.group(1)
    url = f"https://graph.facebook.com/{uid}/picture?type=normal"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        async with session.get(url, headers=headers, allow_redirects=True, timeout=10) as response:
            if response.status == 200:
                image_bytes = await response.read()
                try:
                    img = Image.open(BytesIO(image_bytes))
                    width, height = img.size
                    if width == 100 and height == 100:
                        return baris_data, "LIVE"
                    elif width == 100 and height == 63:
                        return baris_data, "DEAD"
                    else:
                        return baris_data, f"UNKNOWN_{width}x{height}"
                except:
                    return baris_data, "ERROR_BACA_GAMBAR"
            else:
                return baris_data, f"HTTP_ERROR_{response.status}"
    except:
        return baris_data, "ERROR_KONEKSI"

async def process_all_uids(list_baris):
    hasil_live = []
    hasil_dead = []
    
    async with aiohttp.ClientSession() as session:
        batch_size = 25 
        for i in range(0, len(list_baris), batch_size):
            batch = list_baris[i : i + batch_size]
            tasks = [check_uid(session, baris) for baris in batch]
            results = await asyncio.gather(*tasks)
            
            for baris_asli, status in results:
                if status == "LIVE":
                    hasil_live.append(baris_asli)
                else:
                    hasil_dead.append(f"{baris_asli} [{status}]")
                    
    return hasil_live, hasil_dead


# ==========================================
# VERCEL HTTP HANDLER (WAJIB ADA UNTUK VERCEL)
# ==========================================
class handler(BaseHTTPRequestHandler):
    # Menerima request POST dari Frontend
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data)
            uids = data.get('uids', [])
        except:
            uids = []
            
        if not uids:
            self._send_response(400, {"error": "Tidak ada data UID yang dikirim"})
            return
            
        # Jalankan pengecekan Python secara Asynchronous
        live, dead = asyncio.run(process_all_uids(uids))
        
        # Kirim hasil kembali ke Frontend
        self._send_response(200, {"live": live, "dead": dead})

    # Menerima request GET (Hanya untuk tes apakah API online)
    def do_GET(self):
        self._send_response(200, {"status": "API UID Checker berjalan normal."})

    # Format pengiriman balasan JSON
    def _send_response(self, status_code, payload):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*') # Izinkan akses silang
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode('utf-8'))
