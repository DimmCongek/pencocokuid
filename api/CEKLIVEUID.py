import asyncio
import aiohttp
from io import BytesIO
from PIL import Image
import re

# ==========================================
# FUNGSI UTAMA PENGECEKAN UID (ASYNCHRONOUS)
# ==========================================
async def check_uid(session, baris_data):
    # Ekstrak UID menggunakan Regex (mengambil angka di depan)
    match = re.search(r'^(\d+)', baris_data.strip())
    if not match:
        return baris_data, "FORMAT_SALAH"
    
    uid = match.group(1)
    url = f"https://graph.facebook.com/{uid}/picture?type=normal"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }

    try:
        # Melakukan request HTTP secara async
        async with session.get(url, headers=headers, allow_redirects=True, timeout=10) as response:
            if response.status == 200:
                # Baca byte gambar yang dikembalikan Facebook
                image_bytes = await response.read()
                
                try:
                    # Buka gambar menggunakan Pillow untuk mengecek ukuran Pixel-nya
                    img = Image.open(BytesIO(image_bytes))
                    width, height = img.size
                    
                    # Logika Pencocokan Dimensi
                    if width == 100 and height == 100:
                        return baris_data, "LIVE"
                    elif width == 100 and height == 63:
                        return baris_data, "DEAD"
                    else:
                        return baris_data, f"UNKNOWN_{width}x{height}"
                        
                except Exception:
                    return baris_data, "ERROR_BACA_GAMBAR"
            else:
                return baris_data, f"HTTP_ERROR_{response.status}"
                
    except asyncio.TimeoutError:
        return baris_data, "TIMEOUT"
    except Exception as e:
        return baris_data, "ERROR_KONEKSI"


# ==========================================
# FUNGSI BATCHING (MEMPROSES BANYAK SEKALIGUS)
# ==========================================
async def process_all_uids(list_baris):
    print(f"🚀 Memulai pengecekan {len(list_baris)} data secara paralel...")
    
    hasil_live = []
    hasil_dead = []
    
    # Membuka satu sesi HTTP untuk semua request agar lebih hemat memori & cepat
    async with aiohttp.ClientSession() as session:
        batch_size = 25 # Proses 25 UID sekaligus (sama seperti JS sebelumnya)
        
        for i in range(0, len(list_baris), batch_size):
            batch = list_baris[i : i + batch_size]
            
            # Membuat list tugas (tasks) untuk dikerjakan bersamaan
            tasks = [check_uid(session, baris) for baris in batch]
            
            # Menunggu 25 tugas ini selesai bersamaan (Promise.all versi Python)
            results = await asyncio.gather(*tasks)
            
            # Memisahkan hasil
            for baris_asli, status in results:
                if status == "LIVE":
                    hasil_live.append(baris_asli)
                else:
                    hasil_dead.append(f"{baris_asli} [{status}]")
                    
            print(f"⏳ Progress: {min(i + batch_size, len(list_baris))} / {len(list_baris)} selesai.")
            
    return hasil_live, hasil_dead


# ==========================================
# CONTOH CARA MENJALANKAN (ENTRY POINT)
# ==========================================
if __name__ == "__main__":
    # Contoh data (Bisa format murni atau pakai pemisah | )
    data_input = """
    61592326942341|akunsakti99|datr=...
    61592294788365|akunsakti99|datr=...
    100039336012799
    61594629976460
    """
    
    # Bersihkan string input menjadi list
    list_data = [baris.strip() for baris in data_input.strip().split('\n') if baris.strip()]
    
    # Menjalankan loop asynchronous
    live, dead = asyncio.run(process_all_uids(list_data))
    
    print("\n==============================")
    print(f"✅ Total LIVE: {len(live)}")
    print(f"❌ Total DEAD: {len(dead)}")
    
    if live:
        print("\n📋 --- DAFTAR LIVE ---")
        for item in live:
            print(item)
            
    if dead:
        print("\n📋 --- DAFTAR DEAD ---")
        for item in dead:
            print(item)
