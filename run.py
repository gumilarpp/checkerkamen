import os
import sys

_PROXY_KEYS = [
    "HTTPS_PROXY", "HTTP_PROXY", "ALL_PROXY",
    "https_proxy", "http_proxy", "all_proxy",
]

def _configure_proxy() -> None:
    # If user already set a proxy via env var, use it directly (no prompt)
    explicit = next((os.environ[k] for k in _PROXY_KEYS if os.environ.get(k)), "")
    if explicit:
        print(f"[*] Proxy: {explicit}")
        return

    # Non-interactive fallback: if stdin is not a TTY (e.g. background/headless),
    # just clear proxy env vars and move on — no prompt.
    if not sys.stdin.isatty():
        for k in _PROXY_KEYS:
            os.environ.pop(k, None)
        os.environ["NO_PROXY"] = "*"
        print("[*] Tanpa proxy — system proxy dinonaktifkan (non-interactive mode).")
        return

    proxy = ""

    if proxy:
        os.environ["HTTPS_PROXY"] = proxy
        print(f"[*] Proxy diset: {proxy}")
    else:
        # No proxy wanted — clear ALL proxy env vars (including Windows system proxy)
        # so httpx does not accidentally pick one up and get a 503 ProxyError.
        for k in _PROXY_KEYS:
            os.environ.pop(k, None)
        os.environ["NO_PROXY"] = "*"
        print("[*] Tanpa proxy — system proxy dinonaktifkan.")

def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        print("=" * 50)
        token = input("Masukkan Telegram Bot Token: ").strip()
        if not token:
            print("Token kosong. Keluar.")
            sys.exit(1)
        os.environ["TELEGRAM_BOT_TOKEN"] = token

    _configure_proxy()

    print("[*] Menjalankan Netflix Cookie Checker Bot...")
    import bot
    bot.main()

if __name__ == "__main__":
    main()
