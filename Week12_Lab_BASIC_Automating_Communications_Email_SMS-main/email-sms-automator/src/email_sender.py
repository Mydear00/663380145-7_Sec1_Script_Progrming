
"""
email-sms-automator/src/email_sender.py

Handles sending emails via SMTP with SSL/STARTTLS encryption,
UTF-8 content, attachments, and error handling.
"""

import os
import smtplib
import ssl
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

try:
    from .utils import setup_logging
except ImportError:
    from utils import setup_logging


logger = setup_logging(__name__)


class EmailSender:
    """Send UTF-8 emails and attachments securely via SMTP."""

    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        sender_email: str,
        sender_password: str
    ):
        self.smtp_server = smtp_server.strip()
        self.smtp_port = int(smtp_port)
        self.sender_email = sender_email.strip()
        # Remove accidental spaces from a copied Google App Password.
        self.sender_password = sender_password.strip().replace(" ", "")
        self.server = None

        logger.info(
            "EmailSender initialized for %s via %s:%s.",
            self.sender_email,
            self.smtp_server,
            self.smtp_port
        )

    def _connect(self) -> bool:
        """Connect to SMTP and authenticate securely."""

        self._disconnect()

        try:
            logger.info(
                "Connecting to SMTP server %s:%s...",
                self.smtp_server,
                self.smtp_port
            )

            context = ssl.create_default_context()

            if self.smtp_port == 465:
                # Implicit SSL: encryption starts immediately.
                self.server = smtplib.SMTP_SSL(
                    self.smtp_server,
                    self.smtp_port,
                    timeout=20,
                    context=context
                )

                logger.info("SMTP SSL connection established.")

            elif self.smtp_port == 587:
                # STARTTLS: upgrade the connection to TLS.
                self.server = smtplib.SMTP(
                    self.smtp_server,
                    self.smtp_port,
                    timeout=20
                )

                code, _ = self.server.ehlo()
                if code != 250:
                    raise smtplib.SMTPHeloError(
                        code, b"Initial EHLO failed"
                    )

                self.server.starttls(context=context)

                code, _ = self.server.ehlo()
                if code != 250:
                    raise smtplib.SMTPHeloError(
                        code, b"EHLO after STARTTLS failed"
                    )

                logger.info("SMTP STARTTLS connection established.")

            else:
                raise ValueError(
                    f"Unsupported SMTP port: {self.smtp_port}. "
                    "Use port 465 (SSL) or 587 (STARTTLS)."
                )

            logger.info("Authenticating with SMTP server...")
            self.server.login(
                self.sender_email,
                self.sender_password
            )

            logger.info("SMTP connection and authentication successful.")
            return True

        except smtplib.SMTPAuthenticationError as e:
            logger.error(
                "SMTP authentication failed (code %s). "
                "Check the email and Google App Password.",
                e.smtp_code
            )

        except smtplib.SMTPNotSupportedError as e:
            logger.error("SMTP feature not supported: %s", e)

        except smtplib.SMTPConnectError as e:
            logger.error("SMTP connection failed: %s", e)

        except (TimeoutError, OSError, ssl.SSLError) as e:
            logger.error(
                "SMTP network/TLS error (%s): %s",
                type(e).__name__,
                e
            )

        except (smtplib.SMTPException, ValueError) as e:
            logger.error(
                "SMTP configuration/protocol error (%s): %s",
                type(e).__name__,
                e
            )

        except Exception as e:
            logger.error(
                "Unexpected SMTP error (%s): %s",
                type(e).__name__,
                e
            )

        self._disconnect()
        return False

    def _disconnect(self) -> None:
        """Safely close the SMTP connection."""

        server = self.server
        self.server = None

        if server is not None:
            try:
                server.quit()
                logger.info("Disconnected from SMTP server.")
            except Exception:
                try:
                    server.close()
                except Exception:
                    pass

    def send_email(
        self,
        recipient_email: str,
        subject: str,
        body: str,
        attachment_path: str = None,
        is_html: bool = False
    ) -> bool:
        """Send a UTF-8 email, optionally including an attachment."""

        if not recipient_email or not recipient_email.strip():
            logger.error("Recipient email must not be empty.")
            return False

        if not self._connect():
            logger.error("Email not sent because SMTP connection failed.")
            return False

        try:
            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = recipient_email.strip()
            msg["Subject"] = subject

            content_type = "html" if is_html else "plain"
            msg.attach(MIMEText(body, content_type, "utf-8"))

            if attachment_path:
                if os.path.isfile(attachment_path):
                    filename = os.path.basename(attachment_path)

                    with open(attachment_path, "rb") as file:
                        part = MIMEApplication(
                            file.read(),
                            Name=filename
                        )

                    part.add_header(
                        "Content-Disposition",
                        "attachment",
                        filename=filename
                    )
                    msg.attach(part)

                    logger.info("Attached file: %s", attachment_path)

                else:
                    logger.error(
                        "Attachment not found: %s. "
                        "Email will not be sent.",
                        attachment_path
                    )
                    return False

            refused = self.server.send_message(
                msg,
                from_addr=self.sender_email,
                to_addrs=[recipient_email.strip()]
            )

            if refused:
                logger.error(
                    "Email was refused by the SMTP server for: %s",
                    ", ".join(refused.keys())
                )
                return False

            logger.info(
                "Email sent successfully to %s with subject: %s",
                recipient_email,
                subject
            )
            return True

        except (smtplib.SMTPException, OSError, TimeoutError) as e:
            logger.error(
                "Failed to send email (%s): %s",
                type(e).__name__,
                e
            )
            return False

        except Exception as e:
            logger.error(
                "Unexpected email error (%s): %s",
                type(e).__name__,
                e
            )
            return False

        finally:
            self._disconnect()
