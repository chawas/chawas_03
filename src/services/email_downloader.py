import imaplib
import email
from email.header import decode_header
import csv
import getpass

# Function to clean and decode headers
def clean_header(header):
    if header:
        decoded_header = decode_headeri(header)[0]
        if isinstance(decoded_header[0], bytes):
            return decoded_header[0].decode(decoded_header[1] or 'utf-8')
        return decoded_header[0]
    return None

# Function to read emails with specific headers
def fetch_emails(imap_server, email_address, email_password, folder="INBOX", search_criteria='ALL'):
    # Log in to the email server
    with imaplib.IMAP4_SSL(imap_server) as mail:
        mail.login(email_address, email_password)
        mail.select(folder)  # Select the folder to search in (default is INBOX)

        # Search for all messages that match the criteria
        status, messages = mail.search(None, search_criteria)
        email_ids = messages[0].split()

        emails_data = []

        for e_id in email_ids:
            # Fetch the email by ID
            status, msg_data = mail.fetch(e_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    # Parse the email content
                    msg = email.message_from_bytes(response_part[1])

                    # Get specific headers: From, To, Subject, Date
                    from_ = clean_header(msg.get("From"))
                    to_ = clean_header(msg.get("To"))
                    subject_ = clean_header(msg.get("Subject"))
                    date_ = clean_header(msg.get("Date"))

                    emails_data.append([from_, to_, subject_, date_])

        return emails_data

# Function to save emails to a CSV file
def save_to_csv(emails_data, csv_filename):
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write headers
        writer.writerow(["From", "To", "Subject", "Date"])
        # Write email data
        writer.writerows(emails_data)

def main():
    # Input email credentials
    imap_server = input("Enter your IMAP server (e.g., imap.gmail.com): ")
    email_address = input("Enter your email address: ")
    email_password = getpass.getpass("Enter your email password: ")

    # Fetch emails with specific headers
    emails_data = fetch_emails(imap_server, email_address, email_password, search_criteria='ALL')

    # Save to CSV
    csv_filename = "emails.csv"
    save_to_csv(emails_data, csv_filename)

    print(f"Emails saved to {csv_filename}")

if __name__ == "__main__":
    main()
