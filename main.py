#!/usr/bin/python

""" Daily e-mails with goals
"""
from __future__ import print_function
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import argparse
import os.path
import sys
import urllib2
import quip
import httplib2
import os
import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
from apiclient import errors

reload(sys)
sys.setdefaultencoding('utf8')

# Canned method for Google Authentication
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://mail.google.com/'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'
flags = None
def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    # Get Quip document
    auth_key = open('quip_credentials.json').read().rstrip('\n')
    client = quip.QuipClient(
        access_token=auth_key,
        base_url="https://platform.quip.com",
        retry_rate_limit=True, request_timeout=120)
    user = client.get_authenticated_user()
    thread = client.get_thread("hD7jAZ1Rau8Z")

    # Get credentials for Google
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    # Create and send message
    message = MIMEText(thread["html"].encode('utf-8'), 'html')
    message['to'] = "joefarned@gmail.com"
    message['from'] = "joefarned@gmail.com"
    message['subject'] = "Daily Goal Report"
    service.users().messages().send(userId="me",
        body={'raw': base64.urlsafe_b64encode(message.as_string())}).execute()

if __name__ == '__main__':
    main()
