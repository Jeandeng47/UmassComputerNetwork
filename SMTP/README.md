# Lab04: SMTP Client Lab
---
## Overview
A modular, Python-based SMTP client that supports:
- STARTTLS encryption
- AUTH LOGIN authentication with Gmail App Passwords
- Sending plain-text emails
- Sending emails with image attachments (MIME multipart)

---

## Requirements

- Python 3.x  

---

## Usage
1. Before running the program, export the credential information to current environment.
    ```bash
    # Example with gmail
    GMAIL_USER=your.username@gmail.com
    GMAIL_APP_PASS=your_app_password_here
    ```
2. Place any image attachments (e.g. `cat.jpg`) under the same folder of the program
3. Modify the mail content (e.g. recipient, subject, text, img) inside main()
    ```bash
    recipient = f"{user}"
    subject = "Test Email from SMTP Client"
    text = "Hello!\r\nI love computer networks!"
    img = [Path(__file__).parent / 'cat.jpg']
    ```
3. Run the SMTP client
    ```bash
    python3 smtp_client.py
    ```
4. The program will
    - Connect to `smtp.gmail.com:587`
    - Send `EHLO`, `STARTTLS`, wrap socket in SSL
    - Re-`EHLO` and authenticate via AUTH LOGIN
    - Send a test email (with or without attachments)
    - Quit the session

---

## 📄 License

This project is provided for educational purposes only.
