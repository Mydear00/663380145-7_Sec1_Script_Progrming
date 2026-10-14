import datetime
import os
from pathlib import Path

from .config_parser import ConfigParser
from .email_tasks import EmailTasks
from .sms_tasks import SMSTasks
from .template_renderer import TemplateRenderer
from .utils import (
    ensure_directory_exists,
    get_env_variable,
    log_audit_entry,
    setup_logging,
    write_json,
)

logger = setup_logging(__name__)


class CommunicationAgent:
    """Runs email/SMS workflows and records audit logs."""

    def __init__(self, config, base_dir):
        self.config = config
        self.base_dir = Path(base_dir).resolve()
        self.context = {}
        self.audit_log = []
        self.start_time = datetime.datetime.now()
        self.renderer = TemplateRenderer()

        # Keep safe default: real sending requires explicit DRY_RUN=false.
        self.dry_run = (
            get_env_variable("DRY_RUN", "true")
            .strip()
            .lower()
            not in {"0", "false", "no"}
        )

        self.sender_email = get_env_variable("SENDER_EMAIL", "").strip()
        self.sender_password = get_env_variable(
            "SENDER_APP_PASSWORD", ""
        ).replace(" ", "")

        smtp_server = get_env_variable(
            "SMTP_SERVER", "smtp.gmail.com"
        )
        smtp_port = int(get_env_variable("SMTP_PORT", "587"))
        imap_server = get_env_variable(
            "IMAP_SERVER", "imap.gmail.com"
        )

        self.email_tasks = EmailTasks(
            smtp_server=smtp_server,
            smtp_port=smtp_port,
            imap_server=imap_server,
            sender_email=self.sender_email,
            sender_password=self.sender_password,
            dry_run=self.dry_run,
        )

        self.sms_tasks = SMSTasks(
            self.email_tasks,
            self.dry_run,
        )

        logger.info(
            "CommunicationAgent ready (DRY_RUN=%s).",
            self.dry_run,
        )

        if not self.dry_run:
            if not self.sender_email or not self.sender_password:
                raise ValueError(
                    "Real email sending requires SENDER_EMAIL and "
                    "SENDER_APP_PASSWORD in the .env file."
                )

            logger.info("Real communication mode enabled.")

    def _render(self, value, context=None):
        return self.renderer.render(
            value,
            context if context is not None else self.context,
        )

    def _path(self, raw_path):
        path = Path(self._render(str(raw_path)))

        if path.is_absolute():
            return path

        return self.base_dir / path

    def _record(self, level, message, task_type, details=None):
        log_audit_entry(
            self.audit_log,
            level,
            message,
            task_type,
            details or {},
        )

    def _process_task(self, task):
        task_type = task.get("type", "")
        name = task.get("name", "Unnamed task")
        params = task.get("parameters", {})
        output_key = task.get("output_context_key")

        # Skip disabled tasks instead of executing them.
        if task.get("enabled", True) is False:
            logger.info("Skipping disabled task: %s", name)
            self._record(
                "INFO",
                f"Task skipped because it is disabled: {name}",
                task_type,
                {"name": name},
            )
            return

        self._record(
            "INFO",
            f"Starting task: {name}",
            task_type,
            {"name": name},
        )

        try:
            result = True
            output = None

            # -----------------------------------------------
            # Send email
            # -----------------------------------------------
            if task_type == "send_email":
                raw_recipients = params.get(
                    "recipients",
                    {"to": params.get("to", [])},
                )

                recipients = {
                    kind: [
                        self._render(item)
                        for item in (values or [])
                    ]
                    for kind, values in raw_recipients.items()
                }

                subject = self._render(
                    params.get("subject_template", "")
                )
                body = self._render(
                    params.get("body_template", "")
                )

                attachments = [
                    str(self._path(path))
                    for path in params.get("attachments", [])
                ]

                # Do not send if any configured attachment is missing.
                missing_files = [
                    path for path in attachments
                    if not Path(path).is_file()
                ]

                if missing_files:
                    raise FileNotFoundError(
                        "Required email attachment(s) not found: "
                        + ", ".join(missing_files)
                    )

                result = self.email_tasks.send_email(
                    recipients=recipients,
                    subject=subject,
                    body=body,
                    attachments=attachments,
                    is_html=params.get("is_html", False),
                )

                output = {
                    "recipients": recipients,
                    "subject": subject,
                    "attachments": attachments,
                    "sent": bool(result),
                }

            # -----------------------------------------------
            # Send SMS
            # -----------------------------------------------
            elif task_type == "send_sms":
                numbers = [
                    self._render(number)
                    for number in params.get("phone_numbers", [])
                ]

                message = self._render(
                    params.get("message_template", "")
                )

                carrier = self._render(
                    params.get("carrier_name", "")
                ) or None

                result = self.sms_tasks.send_sms(
                    numbers,
                    message,
                    carrier,
                )

                output = {
                    "phone_numbers": numbers,
                    "message": message,
                    "result": result,
                }

            # -----------------------------------------------
            # Process inbox and apply If-Then rules
            # -----------------------------------------------
            elif task_type == "process_inbox":
                criteria = params.get("search_criteria", {})

                sender_filter = (
                    self._render(criteria["from_sender"])
                    if criteria.get("from_sender")
                    else None
                )

                subject_filter = (
                    self._render(criteria["subject_contains"])
                    if criteria.get("subject_contains")
                    else None
                )

                mailbox = params.get("mailbox", "INBOX")

                uids = self.email_tasks.search_emails(
                    mailbox=mailbox,
                    criteria=criteria.get("status", "UNSEEN"),
                    from_sender=sender_filter,
                    subject_contains=subject_filter,
                )

                processed = []
                rule_results = []

                download_dir = self._path(
                    params.get(
                        "download_attachments_base_dir",
                        "data/incoming_attachments",
                    )
                )

                for uid in uids:
                    info = self.email_tasks.fetch_email_content(
                        uid,
                        mark_as_read=False,
                        download_attachments_dir=download_dir,
                        allowed_extensions=params.get(
                            "allowed_extensions"
                        ),
                        mailbox=mailbox,
                    )

                    if not info:
                        rule_results.append({
                            "uid": str(uid),
                            "status": "fetch_failed",
                        })
                        continue

                    processed.append(info)

                    combined_body = (
                        info.get("text_body", "")
                        + " "
                        + info.get("html_body", "")
                    )

                    for rule in params.get("rules", []):
                        conditions = rule.get("if", {})
                        matched = True

                        if "subject_contains" in conditions:
                            expected = self._render(
                                conditions["subject_contains"]
                            ).lower()

                            if expected not in info.get(
                                "subject", ""
                            ).lower():
                                matched = False

                        if "body_contains" in conditions:
                            expected = self._render(
                                conditions["body_contains"]
                            ).lower()

                            if expected not in combined_body.lower():
                                matched = False

                        if "has_attachments" in conditions:
                            expected = bool(
                                conditions["has_attachments"]
                            )

                            if expected != info.get(
                                "has_attachments", False
                            ):
                                matched = False

                        if "sender_contains" in conditions:
                            expected = self._render(
                                conditions["sender_contains"]
                            ).lower()

                            if expected not in info.get(
                                "sender", ""
                            ).lower():
                                matched = False

                        if not matched:
                            continue

                        actions = rule.get("then", {})

                        logger.info(
                            "Inbox rule matched: %s | Subject: %s",
                            rule.get("name", "unnamed"),
                            info.get("subject", ""),
                        )

                        self._record(
                            "INFO",
                            "Inbox rule matched",
                            "inbox_rule",
                            {
                                "uid": info["uid"],
                                "rule": rule.get("name", "unnamed"),
                            },
                        )

                        rule_result = {
                            "uid": info["uid"],
                            "rule": rule.get("name", "unnamed"),
                        }

                        # Send alert only when explicitly enabled.
                        if actions.get("send_sms_alert", False):
                            alert_context = {
                                **self.context,
                                **info,
                            }

                            alert_message = self._render(
                                actions.get(
                                    "alert_message_template",
                                    "Urgent email from {sender}: {subject}",
                                ),
                                alert_context,
                            )

                            alert_numbers = [
                                self._render(number)
                                for number in actions.get(
                                    "alert_phone_numbers", []
                                )
                            ]

                            alert_carrier = self._render(
                                actions.get("alert_carrier", "")
                            ) or None

                            sms_result = self.sms_tasks.send_sms(
                                alert_numbers,
                                alert_message,
                                alert_carrier,
                            )

                            rule_result["sms_result"] = sms_result

                        # Reply to the sender when the rule matches.
                        if actions.get("reply_with_template"):
                            reply_context = {
                                **self.context,
                                **info,
                            }

                            reply_body = self._render(
                                actions["reply_with_template"],
                                reply_context,
                            )

                            reply_subject = self._render(
                                actions.get(
                                    "reply_subject_template",
                                    "Re: {subject}",
                                ),
                                reply_context,
                            )

                            reply_address = self._extract_email_address(
                                info.get("sender", "")
                            )

                            if not reply_address:
                                logger.warning(
                                    "Cannot reply: sender email address "
                                    "could not be extracted."
                                )
                                rule_result["reply_sent"] = False
                            else:
                                reply_sent = self.email_tasks.send_email(
                                    recipients={
                                        "to": [reply_address]
                                    },
                                    subject=reply_subject,
                                    body=reply_body,
                                )

                                rule_result["reply_sent"] = bool(
                                    reply_sent
                                )

                        rule_results.append(rule_result)

                    # Mark as read after processing.
                    # Fetch again with mark_as_read=True.
                    self.email_tasks.fetch_email_content(
                        uid,
                        mark_as_read=True,
                        download_attachments_dir=None,
                        allowed_extensions=params.get(
                            "allowed_extensions"
                        ),
                        mailbox=mailbox,
                    )

                output = {
                    "processed_emails": processed,
                    "found_count": len(uids),
                    "rule_results": rule_results,
                }

            # -----------------------------------------------
            # Log message
            # -----------------------------------------------
            elif task_type == "log_message":
                message = self._render(
                    params.get("message_template", "")
                )

                logger.info("WORKFLOW MESSAGE: %s", message)
                output = {"message": message}

            else:
                logger.warning(
                    "Unsupported task type: %s",
                    task_type,
                )
                result = False

            if result and output_key and output is not None:
                self.context[output_key] = output

            self._record(
                "SUCCESS" if result else "ERROR",
                f"Task {'completed' if result else 'failed'}: {name}",
                task_type,
                {
                    "output_context_key": output_key,
                    "result": bool(result),
                },
            )

        except Exception as exc:
            logger.exception("Task failed: %s", name)

            self._record(
                "ERROR",
                f"Task failed: {name}: {exc}",
                task_type,
                {"error": str(exc)},
            )

    @staticmethod
    def _extract_email_address(sender):
        """Extract an address from a From header."""
        from email.utils import parseaddr

        _, address = parseaddr(sender or "")
        return address.strip()

    def run(self):
        today = datetime.date.today().isoformat()

        self.context.update({
            "report_name": "DailySalesSummary",
            "report_date": today,
            "sales_figure": 12345.67,
            "total_customers": 500,
            "attachment_path_1": "data/reports/sales_report.pdf",
            "attachment_path_2": "data/reports/summary_data.xlsx",
        })

        self._record(
            "INFO",
            "Communication Agent started",
            "agent_run",
            {"dry_run": self.dry_run},
        )

        for task in self.config.get("tasks", []):
            self._process_task(task)

        elapsed = (
            datetime.datetime.now() - self.start_time
        ).total_seconds()

        self._record(
            "INFO",
            "Communication Agent finished",
            "agent_run",
            {
                "duration_seconds": round(elapsed, 2),
                "dry_run": self.dry_run,
                "context_keys": sorted(self.context.keys()),
            },
        )

        report_dir = self.base_dir / "reports"
        ensure_directory_exists(report_dir)

        report_path = report_dir / (
            "audit_report_comm_"
            + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            + ".json"
        )

        write_json(report_path, self.audit_log)

        logger.info("Audit log saved to %s", report_path)

        return report_path