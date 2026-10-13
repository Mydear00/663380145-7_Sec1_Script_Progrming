
"""
test_sms_simulation.py
Large, clear SMS simulation notification.
No real SMS or email is sent.
"""

import os

# Always force simulation mode.
os.environ["SMS_MODE"] = "mock"
os.environ["ENABLE_REAL_SMS"] = "false"

import tkinter as tk
from tkinter import font as tkfont

from src.email_sender import EmailSender
from src.sms_gateway import SMSGateway


def center_window(window, width, height):
    """Center the window on the screen."""
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")


def main():
    phone = "0809744365"
    message = "Hello! This is a simulated SMS for Lab Week 12."

    # Dummy configuration: no email is sent.
    email_sender = EmailSender(
        smtp_server="localhost",
        smtp_port=465,
        sender_email="lab@example.com",
        sender_password="not-a-real-password",
    )

    sms_gateway = SMSGateway(email_sender)

    print("=" * 45)
    print("SMS SIMULATION TEST")
    print("Mode: MOCK - no real SMS will be sent")
    print("=" * 45)

    result = sms_gateway.send_sms(
        phone_number=phone,
        message=message,
        carrier_name="Lunarixz",
    )

    print(f"Phone number: {phone}")
    print(f"Message: {message}")
    print(f"Simulation result: {'SUCCESS' if result else 'FAILED'}")
    print("No real SMS or email was sent.")

    # Create a custom notification window.
    root = tk.Tk()
    root.title("SMS Notification")
    root.resizable(False, False)
    root.configure(bg="#F3F5F7")

    # Use a clear font that supports Thai and English.
    ui_font = "Tahoma"

    title_font = tkfont.Font(
        family=ui_font, size=19, weight="bold"
    )
    body_font = tkfont.Font(
        family=ui_font, size=12
    )
    small_font = tkfont.Font(
        family=ui_font, size=10
    )
    button_font = tkfont.Font(
        family=ui_font, size=12, weight="bold"
    )

    center_window(root, 620, 450)

    # Header
    header_color = "#168653" if result else "#C62828"

    header = tk.Frame(root, bg=header_color, height=105)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="SMS SIMULATION",
        font=title_font,
        fg="white",
        bg=header_color,
    ).pack(anchor="w", padx=28, pady=(22, 4))

    tk.Label(
        header,
        text=(
            "Operation completed successfully"
            if result
            else "Operation failed"
        ),
        font=body_font,
        fg="white",
        bg=header_color,
    ).pack(anchor="w", padx=29)

    # Main content
    content = tk.Frame(root, bg="white")
    content.pack(fill="both", expand=True, padx=22, pady=18)

    tk.Label(
        content,
        text=(
            "จำลองการส่ง SMS สำเร็จ"
            if result
            else "จำลองการส่ง SMS ไม่สำเร็จ"
        ),
        font=tkfont.Font(
            family=ui_font, size=17, weight="bold"
        ),
        fg="#168653" if result else "#C62828",
        bg="white",
    ).pack(anchor="w", padx=20, pady=(18, 14))

    # Recipient
    tk.Label(
        content,
        text="หมายเลขผู้รับ (Recipient)",
        font=small_font,
        fg="#596579",
        bg="white",
    ).pack(anchor="w", padx=20)

    tk.Label(
        content,
        text=phone,
        font=tkfont.Font(
            family=ui_font, size=15, weight="bold"
        ),
        fg="#172033",
        bg="white",
    ).pack(anchor="w", padx=20, pady=(3, 12))

    # Message
    tk.Label(
        content,
        text="ข้อความ (Message)",
        font=small_font,
        fg="#596579",
        bg="white",
    ).pack(anchor="w", padx=20)

    tk.Label(
        content,
        text=message,
        font=body_font,
        fg="#172033",
        bg="white",
        wraplength=520,
        justify="left",
    ).pack(anchor="w", padx=20, pady=(4, 14))

    # Simulation warning
    tk.Label(
        content,
        text="หมายเหตุ: เป็นการจำลองเท่านั้น ไม่มี SMS เข้ามือถือจริง",
        font=small_font,
        fg="#8A5700",
        bg="#FFF2CC",
        padx=12,
        pady=10,
        wraplength=520,
        justify="left",
    ).pack(fill="x", padx=20, pady=(0, 14))

    # Close button
    tk.Button(
        root,
        text="ตกลง  |  OK",
        command=root.destroy,
        font=button_font,
        fg="white",
        bg="#168653" if result else "#C62828",
        activeforeground="white",
        activebackground="#126B43" if result else "#9E1F1F",
        relief="flat",
        cursor="hand2",
        width=18,
        pady=10,
    ).pack(pady=(0, 18))

    root.bind("<Return>", lambda event: root.destroy())
    root.bind("<Escape>", lambda event: root.destroy())

    root.mainloop()

    print("=" * 45)

    if not result:
        raise SystemExit("SMS simulation failed.")


if __name__ == "__main__":
    main()
