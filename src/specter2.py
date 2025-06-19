#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import requests
from pathlib import Path

# ── Konfiguration ───────────────────────────────────────────────────────────────
REPO_API_URL   = "https://api.github.com/repos/allenai/SPECTER2/releases/latest"
EMBEDDINGS_DIR = Path(__file__).parent.parent / "embeddings"
TIMEOUT        = 10  # Sekunden für HTTP-Requests
# ────────────────────────────────────────────────────────────────────────────────

def get_latest_release_info():
    resp = requests.get(REPO_API_URL, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()

def find_embedding_asset(release_json):
    # Wir suchen nach einem Asset, dessen Name auf .bin oder .kv endet
    for asset in release_json.get("assets", []):
        name = asset.get("name", "")
        if name.endswith(".bin") or name.endswith(".kv"):
            return asset["name"], asset["browser_download_url"]
    return None, None

def download_file(url, dest_path):
    with requests.get(url, stream=True, timeout=TIMEOUT) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dest_path, "wb") as f:
            downloaded = 0
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                if total:
                    pct = downloaded * 100 // total
                    print(f"\rDownloading... {pct:3d}% ", end="", flush=True)
    print("\rDownload complete.      ")

def main():
    print("📡 Fetching latest SPECTER2 release info from GitHub…")
    info = get_latest_release_info()
    name, url = find_embedding_asset(info)
    if not url:
        print("❌ Kein .bin/.kv Asset im Release gefunden.", file=sys.stderr)
        sys.exit(1)

    dest = EMBEDDINGS_DIR / name
    if dest.exists():
        print(f"⚠️  Datei '{dest.name}' existiert bereits, überspringe Download.")
    else:
        print(f"⬇️  Lade Embeddings '{name}' herunter …")
        download_file(url, dest)
    print(f"\n✅ SPECTER2-Embeddings sind verfügbar unter:\n   {dest}")

if __name__ == "__main__":
    main()
