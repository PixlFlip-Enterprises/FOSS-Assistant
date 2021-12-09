import base64
import imaplib
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from bs4 import BeautifulSoup as bs


def getAllInbox(username, password):
    M = imaplib.IMAP4_SSL('imap.gmail.com')
    M.login(username, password)

    M.select('INBOX')

    typ, message_numbers = M.search(None, 'ALL')  # change variable name, and use new name in for loop

    for num in message_numbers[0].split():
        typ, data = M.fetch(num, '(RFC822)')
        print(data)  # check what you've actually got. That will help with the next line
        data1 = base64.b64decode(data[0][1])
        print('Message %s\n%s\n' % (num, data1))

    M.close()
    M.logout()


# TODO make this return a uniform, concice array of strings, each string being a message or something similar.
def userViewGetInbox(username, password):
    import imaplib
    import email
    from email.header import decode_header
    import webbrowser
    import os

    def clean(text):
        # clean text for creating a folder
        return "".join(c if c.isalnum() else "_" for c in text)

    # create an IMAP4 class with SSL
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    imap.login(username, password)
    status, messages = imap.select("INBOX")
    # number of top emails to fetch
    N = 3
    # total number of emails
    messages = int(messages[0])

    for i in range(messages, messages - N, -1):
        # fetch the email message by ID
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                # decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # if it's a bytes, decode to str
                    subject = subject.decode(encoding)
                # decode email sender
                From, encoding = decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)
                print("Subject:", subject)
                print("From:", From)
                # if the email message is multipart
                if msg.is_multipart():
                    # iterate over email parts
                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            # print text/plain emails and skip attachments
                            print(body)
                        elif "attachment" in content_disposition:
                            # download attachment
                            filename = part.get_filename()
                            if filename:
                                folder_name = clean(subject)
                                if not os.path.isdir(folder_name):
                                    # make a folder for this email (named after the subject)
                                    os.mkdir(folder_name)
                                filepath = os.path.join(folder_name, filename)
                                # download attachment and save it
                                open(filepath, "wb").write(part.get_payload(decode=True))
                else:
                    # extract content type of email
                    content_type = msg.get_content_type()
                    # get the email body
                    body = msg.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        # print only text email parts
                        print(body)
                if content_type == "text/html":
                    # if it's HTML, create a new HTML file and open it in browser
                    folder_name = clean(subject)
                    if not os.path.isdir(folder_name):
                        # make a folder for this email (named after the subject)
                        os.mkdir(folder_name)
                    filename = "index.html"
                    filepath = os.path.join(folder_name, filename)
                    # write the file
                    open(filepath, "w").write(body)
                    # open in the default browser
                    webbrowser.open(filepath)
                print("=" * 100)
    # close the connection and logout
    imap.close()
    imap.logout()


def sendEmail(email, password, FROM, TO, subject, message):

    # initialize the message we wanna send
    msg = MIMEMultipart("alternative")
    # set the sender's email
    msg["From"] = FROM
    # set the receiver's email
    msg["To"] = TO
    # set the subject
    msg["Subject"] = subject

    # set the body of the email as HTML
    html = "<body>" + message + "</body>" + "<b>\nSent using FOSS Assistant</b>!"
    # make the text version of the HTML
    text = bs(html, "html.parser").text

    # set the body of the email as HTML
    # html = open("mail.html").read()
    # make the text version of the HTML
    text = bs(html, "html.parser").text

    text_part = MIMEText(text, "plain")
    html_part = MIMEText(html, "html")
    # attach the email body to the mail message
    # attach the plain text version first
    msg.attach(text_part)
    msg.attach(html_part)

    print(msg.as_string())

    def send_mail(email, password, FROM, TO, msg):
        # initialize the SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        # connect to the SMTP server as TLS mode (secure) and send EHLO
        server.starttls()
        # login to the account using the credentials
        server.login(email, password)
        # send the email
        server.sendmail(FROM, TO, msg.as_string())
        # terminate the SMTP session
        server.quit()

    # send the mail
    send_mail(email, password, FROM, TO, msg)
