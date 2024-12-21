import imaplib

imap_server = "imap.gmail.com"  # Replace with your IMAP server address
email_address = "wilfred.chawaguta@gmail.com"
email_password = "Chawazi2023|"

# Attempt to connect with SSL (recommended for most services)
try:
    mail = imaplib.IMAP4_SSL(imap_server, 993)
    mail.login(email_address, email_password)
    print("Connected and logged in successfully!")
except imaplib.IMAP4.error as e:
    print("IMAP login failed:", e)
except Exception as e:
    print("Error:", e)