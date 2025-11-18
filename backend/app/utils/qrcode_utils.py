
from pathlib import Path

import qrcode

# On remonte jusqu'au dossier racine "maavnica-smartcard"
BASE_DIR = Path(__file__).resolve().parents[3]  # utils -> app -> backend -> maavnica-smartcard
QR_BASE_DIR = BASE_DIR / "static" / "qr"
QR_BASE_DIR.mkdir(parents=True, exist_ok=True)


def get_or_create_qr_for_slug(slug: str) -> str:
    """Crée un QR code pour l'URL publique d'une SmartCard, si besoin."""
    filename = QR_BASE_DIR / f"{slug}.png"
    if not filename.exists():
        url = f"http://127.0.0.1:8000/c/{slug}"
        img = qrcode.make(url)
        img.save(filename)

    # URL relative que FastAPI sert depuis /static
    return f"/static/qr/{slug}.png"
