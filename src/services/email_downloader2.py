import imaplib

imap_server = "imap.gmail.com"  # Replace with your public IMAP server
email_address = "metcfo@gmail.com"
email_password = "WFORECASTS!"

try:
    mail = imaplib.IMAP4(imap_server)
    mail.login(email_address, email_password)
    print("Login successful!")
except imaplib.IMAP4.error as e:
    print("Login failed:", e)
