import re
from .utils import setup_logging

logger = setup_logging(__name__)

class SMSTasks:
    """Send SMS through an email-to-SMS gateway (carrier support varies by country)."""
    GATEWAYS = {"att": "txt.att.net", "verizon": "vtext.com", "tmobile": "tmomail.net", "sprint": "messaging.sprintpcs.com", "boost": "sms.boostmobile.com", "cricket": "mms.cricketwireless.net", "us_cellular": "email.uscc.net"}
    def __init__(self, email_tasks_instance, dry_run=True):
        self.email_tasks = email_tasks_instance
        self.dry_run = dry_run
    def send_sms(self, phone_numbers, message, carrier_name=None):
        if isinstance(phone_numbers, str): phone_numbers = [phone_numbers]
        if not phone_numbers: logger.warning("No SMS recipients configured."); return False
        results = []
        for number in phone_numbers:
            if "@" in number:
                address = number
            elif carrier_name and carrier_name.lower() in self.GATEWAYS:
                digits = re.sub(r"\D", "", number)
                address = f"{digits}@{self.GATEWAYS[carrier_name.lower()]}"
            else:
                logger.warning("Cannot send SMS to %s: provide a supported carrier or full gateway address.", number)
                results.append(False); continue
            if self.dry_run:
                logger.info("[DRY RUN] SMS preview to %s: %s", address, message)
                results.append(True)
            else:
                results.append(self.email_tasks.send_email({"to": [address]}, "", message))
        return bool(results) and all(results)
