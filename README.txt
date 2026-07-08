====================================================
  NETFLIX COOKIE CHECKER BOT - Setup PC
====================================================

REQUIREMENTS
------------
- Python 3.10+  →  https://www.python.org/downloads/
  (centang "Add Python to PATH" saat install)

INSTALL & JALANKAN
------------------

1. Install dependencies (sekali saja):
   Buka Command Prompt di folder ini, ketik:

      pip install -r requirements.txt

2. Jalankan bot:
   Klik dua kali  start.bat
   -- atau --
   Ketik di Command Prompt:  python run.py

3. Masukkan Bot Token saat diminta.
   (Buat token lewat @BotFather di Telegram)

   Tips: buka start.bat dengan Notepad, isi token di baris
   yang sudah disediakan agar tidak perlu ketik tiap kali.

====================================================
JIKA MUNCUL ERROR "ProxyError" / "503" / "NetworkError"
====================================================

Artinya Telegram diblokir di jaringan Anda.
Solusi: gunakan proxy (VPN lokal, Clash, V2Ray, dll.)

CARA SETTING PROXY:

Buka file start.bat dengan Notepad, cari baris:
   REM set HTTPS_PROXY=socks5://127.0.0.1:7890

Hapus "REM " di depannya dan sesuaikan port:
   set HTTPS_PROXY=socks5://127.0.0.1:7890   ← Clash default
   set HTTPS_PROXY=socks5://127.0.0.1:1080   ← V2Ray/Xray default
   set HTTPS_PROXY=http://127.0.0.1:8080     ← HTTP proxy

Pastikan aplikasi proxy (Clash/V2Ray/dll.) sudah berjalan
di PC sebelum menjalankan bot.

Atau saat run.py meminta "Proxy:", langsung ketik:
   socks5://127.0.0.1:7890

====================================================

CARA PAKAI
----------
Di Telegram, kirim file ke bot Anda:
  - .txt / .json  →  file cookie langsung
  - .zip          →  kumpulan file cookie

Format yang didukung: Netscape, JSON array, pipe-combo,
CookieCheckerPro, ZIP bundle.

TROUBLESHOOTING
---------------
"No module named 'curl_cffi'"  →  pip install curl_cffi
"No module named 'telegram'"   →  pip install -r requirements.txt
Bot tidak merespons             →  pastikan hanya 1 instance berjalan
                                   dengan token yang sama

====================================================
