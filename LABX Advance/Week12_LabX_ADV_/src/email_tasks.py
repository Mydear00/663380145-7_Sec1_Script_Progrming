import email
import imaplib
import smtplib
from email import policy
from email.header import decode_header
from email.message import EmailMessage
from pathlib import Path

from .utils import setup_logging, ensure_directory_exists

logger = setup_logging(__name__)


class EmailTasks:
    """SMTP/IMAP helper. Network actions are only invoked when DRY_RUN is false."""

    def __init__(
        self,
        smtp_server,
        smtp_port,
        imap_server,
        sender_email,
        sender_password,
        dry_run=True,
    ):
        self.smtp_server = smtp_server
        self.smtp_port = int(smtp_port)
        self.imap_server = imap_server
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.dry_run = dry_run

    # ---------------------------------------------------------
    # Send email with optional attachments
    # ---------------------------------------------------------
    def send_email(
        self,
        recipients,
        subject,
        body,
        attachments=None,
        is_html=False,
    ):
        recipients = recipients or {}

        to = recipients.get("to", []) or []
        cc = recipients.get("cc", []) or []
        bcc = recipients.get("bcc", []) or []

        all_recipients = to + cc + bcc

        if not all_recipients:
            logger.error("Email skipped: no recipients configured.")
            return False

        # Validate attachment paths
        existing_files = []

        for raw_path in attachments or []:
            path = Path(raw_path)

            if path.is_file():
                existing_files.append(path)
            else:
                logger.error("Attachment not found: %s", path)
                return False

        # Preview only; do not connect to SMTP
        if self.dry_run:
            logger.info(
                "[DRY RUN] Email preview | To=%s | CC=%s | BCC=%s",
                to,
                cc,
                bcc,
            )
            logger.info("[DRY RUN] Subject: %s", subject)
            logger.info(
                "[DRY RUN] Attachments: %s",
                [path.name for path in existing_files],
            )
            logger.info("[DRY RUN] Body preview: %s", body[:300])
            return True

        try:
            message = EmailMessage()
            message["From"] = self.sender_email

            if to:
                message["To"] = ", ".join(to)

            if cc:
                message["Cc"] = ", ".join(cc)

            message["Subject"] = subject

            if is_html:
                message.set_content(
                    "This email contains HTML content. "
                    "Please use an HTML-capable email client."
                )
                message.add_alternative(body, subtype="html")
            else:
                message.set_content(body)

            # Attach PDF, XLSX, and other files
            for path in existing_files:
                file_data = path.read_bytes()
                suffix = path.suffix.lower()

                if suffix == ".pdf":
                    maintype = "application"
                    subtype = "pdf"
                elif suffix == ".xlsx":
                    maintype = "application"
                    subtype = (
                        "vnd.openxmlformats-officedocument."
                        "spreadsheetml.sheet"
                    )
                elif suffix == ".csv":
                    maintype = "text"
                    subtype = "csv"
                else:
                    maintype = "application"
                    subtype = "octet-stream"

                message.add_attachment(
                    file_data,
                    maintype=maintype,
                    subtype=subtype,
                    filename=path.name,
                )

            # Connect to SMTP and send
            with smtplib.SMTP(
                self.smtp_server,
                self.smtp_port,
                timeout=30,
            ) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()

                server.login(
                    self.sender_email,
                    self.sender_password,
                )

                server.send_message(
                    message,
                    from_addr=self.sender_email,
                    to_addrs=all_recipients,
                )

            logger.info("Email sent successfully to %s", all_recipients)
            return True

        except Exception as exc:
            logger.exception("Email send failed: %s", exc)
            return False

    # ---------------------------------------------------------
    # Decode email headers
    # ---------------------------------------------------------
    @staticmethod
    def _decode_header(value):
        if not value:
            return ""

        decoded_parts = []

        for part, charset in decode_header(value):
            if isinstance(part, bytes):
                decoded_parts.append(
                    part.decode(
                        charset or "utf-8",
                        errors="replace",
                    )
                )
            else:
                decoded_parts.append(part)

        return "".join(decoded_parts).strip()

    # ---------------------------------------------------------
    # Connect to IMAP
    # ---------------------------------------------------------
    def _connect_imap(self, mailbox="INBOX"):
        """Connect and authenticate to IMAP; caller must close the connection."""
        mail = imaplib.IMAP4_SSL(self.imap_server)
        try:
            mail.login(self.sender_email, self.sender_password)

            status, _ = mail.select(mailbox)

            if status != "OK":
                raise RuntimeError(
                    f"Could not select mailbox: {mailbox}"
                )

            return mail

        except Exception:
            try:
                mail.logout()
            except Exception:
                pass
            raise

    # ---------------------------------------------------------
    # Search inbox
    # ---------------------------------------------------------
    def search_emails(
        self,
        mailbox="INBOX",
        criteria="UNSEEN",
        from_sender=None,
        subject_contains=None,
    ):
        if self.dry_run:
            logger.info(
                "[DRY RUN] Inbox search skipped; IMAP was not connected."
            )
            return []

        mail = None

        try:
            mail = self._connect_imap(mailbox)

            allowed_criteria = {
                "ALL",
                "UNSEEN",
                "SEEN",
                "ANSWERED",
                "FLAGGED",
            }

            if criteria not in allowed_criteria:
                logger.warning(
                    "Unsupported IMAP criteria %r; using UNSEEN.",
                    criteria,
                )
                criteria = "UNSEEN"

            # IMAP search uses separate search arguments.
            query = [criteria]

            if from_sender:
                query.extend(["FROM", f'"{from_sender}"'])

            if subject_contains:
                query.extend(["SUBJECT", f'"{subject_contains}"'])

            status, data = mail.uid("search", None, *query)

            if status != "OK" or not data or not data[0]:
                logger.info("No matching emails found.")
                return []

            uids = data[0].split()

            logger.info(
                "Found %s matching email(s) in %s.",
                len(uids),
                mailbox,
            )

            return uids

        except Exception as exc:
            logger.exception("Inbox search failed: %s", exc)
            return []

        finally:
            if mail is not None:
                try:
                    mail.logout()
                except Exception:
                    pass

    # ---------------------------------------------------------
    # Fetch email content and optionally download attachments
    # ---------------------------------------------------------
    def fetch_email_content(
        self,
        uid,
        mark_as_read=True,
        download_attachments_dir=None,
        allowed_extensions=None,
        mailbox="INBOX",
    ):
        if self.dry_run:
            logger.info(
                "[DRY RUN] Fetch skipped; IMAP was not connected."
            )
            return None

        mail = None

        try:
            mail = self._connect_imap(mailbox)

            if isinstance(uid, str):
                uid = uid.encode("ascii")

            status, data = mail.uid(
                "fetch",
                uid,
                "(RFC822)",
            )

            if (
                status != "OK"
                or not data
                or not isinstance(data[0], tuple)
            ):
                logger.warning("Could not fetch email UID %s.", uid)
                return None

            message = email.message_from_bytes(
                data[0][1],
                policy=policy.default,
            )

            text_parts = []
            html_parts = []
            attachments_meta = []

            if message.is_multipart():
                parts = message.walk()
            else:
                parts = [message]

            for part in parts:
                filename = part.get_filename()
                disposition = part.get_content_disposition()

                # Process attachments
                if filename and disposition in {"attachment", "inline"}:
                    safe_name = Path(filename).name
                    extension = Path(safe_name).suffix.lower()

                    if (
                        allowed_extensions
                        and extension not in {
                            ext.lower()
                            for ext in allowed_extensions
                        }
                    ):
                        logger.info(
                            "Attachment skipped by extension filter: %s",
                            safe_name,
                        )

                        attachments_meta.append(
                            {
                                "filename": safe_name,
                                "filepath": None,
                                "skipped": True,
                            }
                        )
                        continue

                    filepath = None

                    if download_attachments_dir:
                        folder = Path(download_attachments_dir)
                        ensure_directory_exists(folder)

                        destination = folder / safe_name

                        # Prevent overwriting a previous download.
                        if destination.exists():
                            uid_text = (
                                uid.decode(errors="ignore")
                                if isinstance(uid, bytes)
                                else str(uid)
                            )
                            destination = folder / (
                                f"{destination.stem}_{uid_text}"
                                f"{destination.suffix}"
                            )

                        file_data = part.get_payload(decode=True) or b""
                        destination.write_bytes(file_data)

                        filepath = str(destination)

                        logger.info(
                            "Attachment downloaded: %s",
                            filepath,
                        )

                    attachments_meta.append(
                        {
                            "filename": safe_name,
                            "filepath": filepath,
                            "skipped": False,
                        }
                    )

                # Process email body
                elif part.get_content_type() == "text/plain":
                    try:
                        content = part.get_content()
                        if isinstance(content, str):
                            text_parts.append(content)
                    except Exception as exc:
                        logger.warning(
                            "Could not decode plain-text body: %s",
                            exc,
                        )

                elif part.get_content_type() == "text/html":
                    try:
                        content = part.get_content()
                        if isinstance(content, str):
                            html_parts.append(content)
                    except Exception as exc:
                        logger.warning(
                            "Could not decode HTML body: %s",
                            exc,
                        )

            # Mark the message as read if requested.
            if mark_as_read:
                status, _ = mail.uid(
                    "store",
                    uid,
                    "+FLAGS",
                    r"(\Seen)",
                )

                if status != "OK":
                    logger.warning(
                        "Could not mark email UID %s as read.",
                        uid,
                    )

            uid_text = (
                uid.decode(errors="replace")
                if isinstance(uid, bytes)
                else str(uid)
            )

            result = {
                "uid": uid_text,
                "sender": self._decode_header(message.get("From")),
                "subject": self._decode_header(message.get("Subject")),
                "text_body": "\n".join(text_parts),
                "html_body": "\n".join(html_parts),
                "has_attachments": bool(attachments_meta),
                "attachments_meta": attachments_meta,
            }

            logger.info(
                "Email fetched: UID=%s | Subject=%s",
                uid_text,
                result["subject"],
            )

            return result

        except Exception as exc:
            logger.exception(
                "Could not fetch email %s: %s",
                uid,
                exc,
            )
            return None

        finally:
            if mail is not None:
                try:
                    mail.logout()
                except Exception:
                    pass