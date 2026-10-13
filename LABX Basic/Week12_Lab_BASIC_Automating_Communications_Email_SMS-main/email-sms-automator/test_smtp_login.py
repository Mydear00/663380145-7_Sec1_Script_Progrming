import os
import smtplib
import ssl
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path, override=True)

email = os.getenv("SENDER_EMAIL", "").strip()
password = os.getenv("SENDER_APP_PASSWORD", "").strip().replace(" ", "")

if not email or not password:
    print("ERROR: Missing SENDER_EMAIL or SENDER_APP_PASSWORD in .env")
    raise SystemExit(1)

server = None

try:
    print("Connecting to Gmail SMTP over SSL (port 465)...")

    server = smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465,
        timeout=20,
        context=ssl.create_default_context()
    )

    print("SSL connection: OK")

    print("\nStep 1: Sending EHLO...")
    ehlo_code, ehlo_response = server.ehlo()
    print(f"EHLO response code: {ehlo_code}")

    if ehlo_code != 250:
        print("ERROR: Gmail did not accept EHLO.")
        raise RuntimeError("EHLO failed")

    print("Supported SMTP features:", sorted(server.esmtp_features.keys()))
    print(
        "Supported authentication methods:",
        server.esmtp_features.get("auth", "Not advertised")
    )

    print("\nStep 2: Testing authentication...")
    server.login(email, password)

    print("SMTP LOGIN: SUCCESS")

except smtplib.SMTPAuthenticationError as e:
    print(f"Authentication rejected: SMTP code {e.smtp_code}")
    print("Check the Google App Password and Google account.")

except smtplib.SMTPServerDisconnected as e:
    print(f"Connection closed by server: {e}")

except (OSError, ssl.SSLError) as e:
    print(f"Network/SSL error: {type(e).__name__}: {e}")

except smtplib.SMTPException as e:
    print(f"SMTP error: {type(e).__name__}: {e}")

except RuntimeError as e:
    print(f"Test stopped: {e}")

finally:
    if server is not None:
        try:
            server.quit()
        except Exception:
            server.close()

    print("\nSMTP test finished.")
