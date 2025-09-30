# scripts/ensure_build_files.py
import os

required_files = [
    "public/icon.ico",
    "public/icon.icns",
    "public/icon.png",
    "public/icon.svg",
    "public/icon.webp",
]

for f in required_files:
    if not os.path.exists(f):
        raise FileNotFoundError(f"Missing required file: {f}")

print("All required files are present.")