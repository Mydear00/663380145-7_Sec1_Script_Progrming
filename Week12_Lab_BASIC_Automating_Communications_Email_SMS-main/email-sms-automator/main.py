
"""
email-sms-automator/main.py

Main orchestration script executing automated communication workflows:
1. Sending plaintext emails
2. Sending emails with file attachments
3. Sending SMS via carrier email gateways
4. Receiving, parsing, and processing incoming emails with attachment downloads
"""

import os
import sys
import time

# Ensure 'src' package directory is discoverable in Python path
sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
)

from email_receiver import EmailReceiver
from email_sender import EmailSender
from sms_gateway import SMSGateway
from utils import ensure_directory_exists, get_env_variable, setup_logging

logger = setup_logging(__name__)


def main():
    """
    Main entrypoint function to orchestrate email and SMS automation tasks.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    attachments_dir = os.path.join(data_dir, "attachments")

    ensure_directory_exists(data_dir)
    ensure_directory_exists(attachments_dir)

    # --- Load Credentials and Student Information ---
    try:
        sender_email = get_env_variable("SENDER_EMAIL")
        sender_app_password = get_env_variable("SENDER_APP_PASSWORD")
        smtp_server = get_env_variable("SMTP_SERVER")
        smtp_port = int(get_env_variable("SMTP_PORT"))
        imap_server = get_env_variable("IMAP_SERVER")

        test_recipient_email = get_env_variable("TEST_RECIPIENT_EMAIL")
        test_sms_phone_number = get_env_variable("TEST_SMS_PHONE_NUMBER")
        test_sms_carrier = get_env_variable("TEST_SMS_CARRIER")

        # Student information
        student_first_name = get_env_variable("STUDENT_FIRST_NAME")
        student_last_name = get_env_variable("STUDENT_LAST_NAME")
        student_id = get_env_variable("STUDENT_ID")

    except ValueError as e:
        logger.critical(
            f"Configuration error: {e}. "
            "Please check the required variables in your .env file."
        )
        sys.exit(1)

    # --- Prepare Student Notification Email ---
    student_email_body = f"""

ชื่อ: {student_first_name}
นามสกุล: {student_last_name}
รหัสนักศึกษา: {student_id}

"""

    # --- Initialize Handlers ---
    email_sender = EmailSender(
        smtp_server,
        smtp_port,
        sender_email,
        sender_app_password
    )
    email_receiver = EmailReceiver(
        imap_server,
        sender_email,
        sender_app_password
    )
    sms_gateway = SMSGateway(email_sender)

    # --- Task 1: Send a Student Notification Email ---
    logger.info("\n--- Task 1: Sending student notification email ---")

    email_sender.send_email(
        recipient_email=test_recipient_email,
        subject="แจ้งเตือนการรันโปรแกรม Python",
        body=student_email_body
    )

    time.sleep(2)

    # --- Task 2: Send an Email with an Attachment ---
    logger.info("\n--- Task 2: Sending an email with an attachment ---")

    attachment_file_path = os.path.join(data_dir, "dummy_report.pdf")

    if os.path.exists(attachment_file_path):
        email_sender.send_email(
            recipient_email=test_recipient_email,
            subject="รายงานการทดสอบระบบ Python พร้อมไฟล์แนบ",
            body=student_email_body,
            attachment_path=attachment_file_path
        )
    else:
        logger.warning(
            f"Attachment file not found at '{attachment_file_path}'. "
            "Skipping attachment email."
        )

    time.sleep(2)

    # --- Task 3: Send an SMS via Email Gateway ---
    logger.info("\n--- Task 3: Sending an SMS via email gateway ---")

    sms_message = (
        f"แจ้งเตือนจาก Python: {student_first_name} "
        f"{student_last_name} รหัสนักศึกษา {student_id}"
    )

    sms_gateway.send_sms(
        phone_number=test_sms_phone_number,
        message=sms_message,
        carrier_name=test_sms_carrier
    )

    time.sleep(5)

    # --- Task 4: Receive and Process Emails ---
    logger.info("\n--- Task 4: Receiving and processing emails ---")

    # Send a demo email to self for the receiving demonstration
    receiving_subject = "Python Test: Email for Receiving Demo"

    email_sender.send_email(
        recipient_email=sender_email,
        subject=receiving_subject,
        body=student_email_body,
        attachment_path=(
            attachment_file_path
            if os.path.exists(attachment_file_path)
            else None
        )
    )

    logger.info(
        "Sent a demo email to self. Waiting for email delivery..."
    )
    time.sleep(10)

    # Search for unread emails from self with the expected subject
    uids = email_receiver.search_emails(
        criteria="UNSEEN",
        from_sender=sender_email,
        subject_contains=receiving_subject
    )

    if uids:
        logger.info(
            f"Found {len(uids)} matching unread email(s) "
            "for receiving demo."
        )

        for uid in uids:
            uid_str = (
                uid.decode("utf-8")
                if isinstance(uid, bytes)
                else str(uid)
            )

            logger.info(f"Processing email UID: {uid_str}")

            email_details = email_receiver.fetch_email_content(
                uid=uid,
                mark_as_read=True,
                download_attachments_dir=attachments_dir
            )

            if email_details:
                logger.info(f"  Sender: {email_details['sender']}")
                logger.info(f"  Subject: {email_details['subject']}")
                logger.info(
                    f"  Body Snippet: {email_details['body_snippet']}"
                )

                if email_details["attachments_downloaded"]:
                    logger.info(
                        "  Attachments downloaded: "
                        + ", ".join(
                            email_details["attachments_downloaded"]
                        )
                    )
                else:
                    logger.info("  No attachments downloaded.")
            else:
                logger.error(
                    f"Could not retrieve email UID: {uid_str}"
                )
    else:
        logger.info(
            "No matching unread emails found for receiving demo."
        )

    logger.info("\n--- All communication automation tasks completed ---")


if __name__ == "__main__":
    main()
