import base64
from pathlib import Path
from socket import *
import os
import ssl


def send_cmd(sock, cmd):
    sock.send(cmd.encode())
    rec = sock.recv(1024).decode()
    print(rec)

# Socket connection and greeting
def connect_greet(mailserver):
    print("Connecting to mail server...")
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(mailserver)
    recv = sock.recv(1024).decode()
    print(recv)
    return sock

# Send EHLO command
def ehlo(sock):
    print("Sending EHLO command...")
    ehlo_cmd = 'EHLO Alice\r\n'
    send_cmd(sock, ehlo_cmd)

# Start TLS and wrap socket with SSL
def start_tls(sock, server_host):
    print("Sending STARTTLS command...")
    starttls_cmd = 'STARTTLS\r\n'
    send_cmd(sock, starttls_cmd)

    print("Wrapping socket with SSL...")
    context = ssl.create_default_context()
    sock = context.wrap_socket(sock, server_hostname=server_host)
    
    return sock

# Load credentials from environment variables
def load_credentials():
    print("Loading credentials...")
    user = os.getenv("GMAIL_USER")
    pwd = os.getenv("GMAIL_APP_PASS")
    if not user or not pwd:
        raise RuntimeError("Missing GMAIL_USER or GMAIL_APP_PASS environment variables")
    return user, pwd

# Authenticate using AUTH LOGIN
def authenticate(sock, user, pwd):
    print("Sending AUTH LOGIN command...")
    send_cmd(sock, 'AUTH LOGIN\r\n')

    # user.encode(): alice@gmail.com -> utf-8 bytes
    # base64.b64encode: utf-8 bytes-> new bytes: b'YWxpY2VAZ21haWwuY29t'
    # decode(): new bytes -> utf-8 string: 'YWxpY2VAZ21haWwuY29t'
    b64_user = base64.b64encode(user.encode()).decode()
    send_cmd(sock, (b64_user + '\r\n'))

    b64_pass = base64.b64encode(pwd.encode()).decode()
    send_cmd(sock, (b64_pass + '\r\n'))

# Send email with attachments
def send_mail(sock, user, recipient, subject, text, attachments=None):
    print("Sending MAIL FROM command...")
    mail_from = f"MAIL FROM:<{user}>\r\n"
    send_cmd(sock, mail_from)

    print("Sending RCPT TO command...")
    rcpt_to = f"RCPT TO:<{recipient}>\r\n"
    send_cmd(sock, rcpt_to)

    print("Sending DATA command...")
    send_cmd(sock, 'DATA\r\n')

    if attachments:
        boundary = "====BOUNDARY===="
        # build headers and multipart
        parts = [
            f"From: {user}\r\n",
            f"To: {recipient}\r\n",
            f"Subject: {subject}\r\n"
            "MIME-Version: 1.0\r\n",
            f"Content-Type: multipart/mixed; boundary=\"{boundary}\"\r\n\r\n",
        ]
        # text part
        parts.extend([
            f"--{boundary}\r\n",
            "Content-Type: text/plain; charset=\"utf-8\"\r\n",
            "Content-Transfer-Encoding: 7bit\r\n\r\n",
            f"{text}\r\n"
        ])

        # attchment parts
        for img_path in attachments:
            if img_path.exists():
                parts.extend([
                    f"--{boundary}\r\n",
                    "Content-Type: image/jpeg\r\n",
                    "Content-Transfer-Encoding: base64\r\n",
                    f"Content-Disposition: attachment; filename=\"{img_path.name}\"\r\n\r\n"
                ])
                with open(img_path, 'rb') as img_file:
                    img_data = base64.b64encode(img_file.read()).decode()
                    parts.append(f"{img_data}\r\n")
            else:
                print(f"Attachment {img_path} does not exist, skipping...")
        
        # closing boundary
        parts.extend([
            f"--{boundary}--\r\n",
            ".\r\n"
        ])
        sock.send(''.join(parts).encode())
    else:
        print("Sending email with text only...")
        data = f"Subject: {subject}\r\nTo: {recipient}\r\n\r\n{text}\r\n.\r\n"
        send_cmd(sock, data)

# Send QUIT command and close socket
def quit(sock):
    send_cmd(sock, 'QUIT\r\n')
    sock.close()

def main():
    MAILSERVER = ('smtp.gmail.com', 587)    
    
    sock = connect_greet(MAILSERVER)

    ehlo(sock)
    sock = start_tls(sock, MAILSERVER[0])

    user, pwd = load_credentials()
    authenticate(sock, user, pwd)

    recipient = f"{user}" 
    subject = "Test Email from SMTP Client"
    text = "Hello!\r\nI love computer networks!"
    img = [Path(__file__).parent / 'cat.jpg']
    send_mail(sock, user, recipient, subject, text, img)

    quit(sock)

if __name__ == "__main__":
    main()