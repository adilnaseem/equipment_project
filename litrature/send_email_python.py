import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender_email, receiver_email, subject, body):
  """
  Sends an email using Gmail's SMTP server.

  Args:
    sender_email: The email address of the sender.
    receiver_email: The email address of the recipient.
    subject: The subject of the email.
    body: The body of the email.

  Raises:
    Exception: If there's an error sending the email.
  """

  try:
    # Create a multipart message
    msg = MIMEMultipart()

    # Set the sender and recipient addresses
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Set the message body
    msg.attach(MIMEText(body, 'plain'))

    # Connect to Gmail's SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    ## Connect to Yahoo's SMTP server
    # server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
    server.starttls() 

    # Get your Gmail password (or create an app password)
    password ='birahgnocoeafdao' #for google Create your app password from here https://myaccount.google.com/apppasswords
    server.login(sender_email, password)

    # Send the email
    server.sendmail(sender_email, receiver_email, msg.as_string())

    print("Email sent successfully!")

  except Exception as e:
    print(f"Error sending email: {e}")

  finally:
    server.quit()

# Example usage
if __name__ == "__main__":
  sender_email = "adilnaseem.pak@gmail.com"
  receiver_email = "adilnaseempk@yahoo.com"
  subject = "Test Email from Python"
  body = "This is a test email sent from Python."

  send_email(sender_email, receiver_email, subject, body)