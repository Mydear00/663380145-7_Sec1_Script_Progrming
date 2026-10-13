
"""
SMS Gateway for Lab testing.

Modes:
- mock: simulate SMS without sending anything
- twilio: send a real SMS using the Twilio API

Real SMS requires explicit opt-in in .env.
"""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    from .email_sender import EmailSender
    from .utils import setup_logging
except ImportError:
    from email_sender import EmailSender
    from utils import setup_logging

logger = setup_logging(__name__)


class SMSGateway:
    def __init__(self, email_sender_instance: EmailSender):
        if not isinstance(email_sender_instance, EmailSender):
            raise TypeError(
                "SMSGateway requires an instance of EmailSender."
            )

        # Kept for compatibility with existing main.py.
        # EmailSender is never used to transmit SMS.
        self.email_sender = email_sender_instance

        self.mode = os.getenv("SMS_MODE", "mock").strip().lower()
        self.real_sms_enabled = (
            os.getenv("ENABLE_REAL_SMS", "false").strip().lower()
            == "true"
        )

        project_root = Path(__file__).resolve().parent.parent
        self.log_dir = project_root / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.sms_log_file = self.log_dir / "sms_simulation.log"

        if self.mode not in {"mock", "twilio"}:
            raise ValueError(
                "SMS_MODE must be 'mock' or 'twilio'."
            )

        if self.mode == "twilio" and not self.real_sms_enabled:
            logger.warning(
                "Twilio mode requested, but real SMS is disabled. "
                "No SMS will be sent."
            )

        logger.info("SMSGateway initialized. Mode=%s", self.mode)

    @staticmethod
    def _normalize_phone(phone_number: str) -> Optional[str]:
        """Normalize a Thai mobile number or international number."""
        if not isinstance(phone_number, str):
            return None

        phone = re.sub(r"[\s\-()]", "", phone_number.strip())

        # Convert Thai domestic format 0xxxxxxxxx to +66xxxxxxxxx.
        if re.fullmatch(r"0[0-9]{9}", phone):
            phone = "+66" + phone[1:]

        # Accept international E.164-style numbers.
        if not re.fullmatch(r"\+[1-9][0-9]{7,14}", phone):
            return None

        return phone

    def _write_log(
        self,
        phone_number: str,
        status: str,
        detail: str = "",
    ) -> None:
        timestamp = datetime.now().astimezone().isoformat(
            timespec="seconds"
        )
        entry = (
            f"[{timestamp}] status={status} "
            f"| phone={phone_number} | {detail}\n"
        )

        with self.sms_log_file.open("a", encoding="utf-8") as file:
            file.write(entry)

    def send_sms(
        self,
        phone_number: str,
        message: str,
        carrier_name: Optional[str] = None,
    ) -> bool:
        """
        Send a mock SMS or a real Twilio SMS, depending on .env.
        Returns True when the provider accepts the message request.
        This does not guarantee delivery to the recipient.
        """
        recipient = self._normalize_phone(phone_number)

        if recipient is None:
            logger.error("SMS failed: invalid phone number format.")
            return False

        if not isinstance(message, str) or not message.strip():
            logger.error("SMS failed: message cannot be empty.")
            return False

        message = message.strip()

        # Default mode: simulate only.
        if self.mode == "mock":
            try:
                self._write_log(
                    recipient,
                    "SIMULATED_SUCCESS",
                    "No real SMS sent",
                )
                logger.info(
                    "[MOCK SMS] Simulation successful for %s. "
                    "No real SMS was sent.",
                    recipient,
                )
                return True
            except OSError:
                logger.exception("Could not write SMS simulation log.")
                return False

        # Real sending requires two explicit settings.
        if not self.real_sms_enabled:
            logger.warning(
                "Real SMS blocked: set ENABLE_REAL_SMS=true "
                "only when ready to send."
            )
            return False

        account_sid = os.getenv("TWILIO_ACCOUNT_SID", "").strip()
        auth_token = os.getenv("TWILIO_AUTH_TOKEN", "").strip()
        from_number = os.getenv("TWILIO_FROM_NUMBER", "").strip()

        if not account_sid or not auth_token or not from_number:
            logger.error(
                "Real SMS blocked: Twilio credentials or sender "
                "number are missing from .env."
            )
            return False

        normalized_sender = self._normalize_phone(from_number)
        if normalized_sender is None:
            logger.error(
                "Real SMS blocked: TWILIO_FROM_NUMBER must be "
                "a valid international phone number."
            )
            return False

        try:
            from twilio.rest import Client

            client = Client(account_sid, auth_token)
            sms = client.messages.create(
                to=recipient,
                from_=normalized_sender,
                body=message,
            )

            logger.info(
                "Twilio accepted SMS request. SID=%s Status=%s",
                sms.sid,
                sms.status,
            )

            try:
                self._write_log(
                    recipient,
                    "PROVIDER_ACCEPTED",
                    f"sid={sms.sid} status={sms.status}",
                )
            except OSError:
                logger.warning("Could not write SMS log file.")

            return True

        except ImportError:
            logger.error(
                "Twilio SDK is missing. Run: "
                "python -m pip install twilio"
            )
            return False
        except Exception:
            # Do not print credentials or message contents.
            logger.exception("Twilio SMS request failed.")
            return False
