from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import email, smtplib, ssl
from email import encoders
import getpass
import os.path
import sys

"""
A Python bot that sends files via email (pdf, images, music,...).
Files need to be drag and dropped into the shell. Can handle multiple files drop, but the files
must be dropped one after the other.
Requires to set up a gmail account for the bot and add some receiver email adresses.
"""


port = 465  # For SSL

print("Sup'")

# Enter password for PyBot's email adress
password = getpass.getpass('Password: ')

# Modify bot adress here
sender_email = 'botsadress@gmail.com'
receiver_name = input('Send mail to:')
# Bunch of emails to add
if receiver_name == 'John':
    receiver_email = 'johnsadress@gmail.com'
elif receiver_name == 'Bot':
    receiver_email = 'botsadress@gmail.com'
else:
    print('Who dis?')
    sys.exit(0) 

body = "This email was sent by PyBot, a personnal Python mail assistant."

# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
subject = ''

# Works with pdf, pptx, image, music files
filenames = input('Drag and drop file(s): ')
filenames = filenames.replace("\\", "/").replace('"', "")
filelist = filenames.split("C:")
for file in filter(lambda x: x != '', filelist):
	subject += ' ' + os.path.split(file)[1]
	print('Preparing ', os.path.split(file)[1], ' ...')
	try:
		# Open file in binary mode
		with open(file, "rb") as attachment:
		    # Add file as application/octet-stream
		    # Email client can usually download this automatically as attachment
		    part = MIMEBase("application", "octet-stream")
		    part.set_payload(attachment.read())
	except:
		print(sys.exc_info())
		input('Error - 1')
	# Encode file in ASCII characters to send by email    
	encoders.encode_base64(part)
	# Add header as key/value pair to attachment part
	part.add_header(
	    "Content-Disposition",
	    f"attachment; filename= {os.path.split(file)[1]}",
	)
	# Add attachment to message and convert message to string
	message.attach(part)

message["Subject"] = subject
text = message.as_string()
message.attach(MIMEText(body, "plain"))

# Log in to server using secure context and send email
# Create a secure SSL context
context = ssl.create_default_context()
try:
	with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
	    server.login(sender_email, password)
	    server.sendmail(sender_email, receiver_email, text)  
	input('Mail sent!')
except:
	print(sys.exc_info())
	input('Error - 2')