"""
Bilibili QR Code Login Script
Generates QR code, saves to assets/, polls for scan, saves credentials.

Usage: python bilibili_qr_login.py
"""

import asyncio
import json
import sys
from pathlib import Path

import qrcode
from bilibili_api.login_v2 import QrCodeLogin, QrCodeLoginEvents


def p(text=""):
    print(text.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding))


# Paths
VAULT_ROOT = Path(__file__).resolve().parents[5]  # obsidian-vault/
ASSETS_DIR = VAULT_ROOT / "assets"
CREDENTIALS_FILE = Path(__file__).resolve().parent / "bilibili_credentials.json"


async def main():
    p("=" * 55)
    p(" Bilibili QR Code Login")
    p("=" * 55)

    # Step 1: Generate QR code
    p("\n[1/3] Generating QR code...")
    qr = QrCodeLogin()
    await qr.generate_qrcode()

    # Get QR code URL and create image
    qr_url = qr._QrCodeLogin__qr_link
    qr_img = qrcode.make(qr_url)
    dst_qr = ASSETS_DIR / "bilibili_qr_login.png"
    qr_img.save(dst_qr)
    p("  [OK] QR code saved to: " + str(dst_qr))
    p("")
    p("  >>> Scan with Bilibili App on your phone <<<")
    p("  File: " + str(dst_qr))
    p("")

    # Step 2: Poll for scan (120s timeout)
    p("[2/3] Waiting for scan (max 120s)...")
    credential = None
    for i in range(120):
        state = await qr.check_state()
        if state == QrCodeLoginEvents.DONE:
            credential = qr.get_credential()
            p("  [OK] Login successful!")
            break
        elif state == QrCodeLoginEvents.TIMEOUT:
            p("  [FAIL] QR code expired. Run again.")
            return
        else:
            if state == QrCodeLoginEvents.SCAN and i % 10 == 0:
                p("  [WAIT] Waiting for scan... (" + str(i) + "s)")
            elif state == QrCodeLoginEvents.CONF and i % 3 == 0:
                p("  [OK] Scanned, confirming login...")
            await asyncio.sleep(1)

    if not credential:
        p("  [FAIL] Timeout (120s). Try again.")
        return

    # Step 3: Validate and save credentials
    p("\n[3/3] Validating credentials...")
    try:
        is_valid = await credential.check_valid()
        if is_valid:
            p("  [OK] Credentials valid!")

            cred_data = {
                "sessdata": credential.sessdata,
                "bili_jct": credential.bili_jct,
                "buvid3": credential.buvid3,
                "dedeuserid": credential.dedeuserid,
                "ac_time_value": credential.ac_time_value,
            }
            with open(CREDENTIALS_FILE, "w", encoding="utf-8") as f:
                json.dump(cred_data, f, ensure_ascii=False, indent=2)
            p("  [OK] Credentials saved to: " + str(CREDENTIALS_FILE))
            p("  [INFO] Other scripts will read from this file.")
        else:
            p("  [FAIL] Credentials invalid. Try again.")
    except Exception as e:
        p("  [ERROR] " + str(e))


if __name__ == "__main__":
    asyncio.run(main())
