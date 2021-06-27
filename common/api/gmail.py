from __future__ import print_function

import logging
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

logger = logging.getLogger()
logger.setLevel('DEBUG')

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service


def get_labels(service):
    """
    return a list of labels
    [{'id': 'INBOX', 'name': 'INBOX', 'messageListVisibility': 'hide', 'labelListVisibility': 'labelShow', 'type': 'system'},
    ...]
    """

    # Call the Gmail API
    logging.info('getting all labels')
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    label_list = [label['name'] for label in labels]
    logging.info(f"labels: {label_list}")
    return label_list


def get_user_profile(service):
    """
    {'emailAddress': 'wangqiman0111@gmail.com', 'messagesTotal': 81955, 'threadsTotal': 76605, 'historyId': '15612103'}
    """
    logging.info('getting user profile')
    profile = service.users().getProfile(userId='me').execute()
    logging.info(f"profile: {profile}")
    return profile


def list_email_ids_by_label(service, label, max_results=500, q=None):
    """
    get email ids for label,
    :param service:
    :param label: label
    :param max_results: how much to query per request
    """
    email_ids = set()
    next_page_token = ''

    while True:
        response = service.users().messages().list(userId='me', labelIds=label, maxResults=max_results,
                                                   pageToken=next_page_token, q=q).execute()
        # logging.debug(f"response: {response}")
        """ response format
        { 'messages' : [{'id': '17a4a8c83e4dbd9f', 'threadId': '17a4a8c83e4dbd9f'},...]
        'resultSizeEstimate' : 162,
        'nextPageToken' : '10552015227373681158'
        }
        """
        if not response.get('messages'):
            logging.info('No emails found')
            break

        for msg_id in response['messages']:
            email_ids.add(msg_id['id'])
        logging.debug(f"total message ids: {len(email_ids)}")

        if 'nextPageToken' in response:
            next_page_token = response['nextPageToken']
        else:
            break
    logging.debug(email_ids)
    return email_ids


if __name__ == '__main__':
    service = get_service()
    # user_info = get_user_profile(service)
    # labels = get_labels(service)
    list_email_ids_by_label(service, 'CATEGORY_UPDATES')
    # ['CHAT', 'SENT', 'INBOX', 'IMPORTANT', 'TRASH', 'DRAFT', 'SPAM', 'CATEGORY_FORUMS', 'CATEGORY_UPDATES', 'CATEGORY_PERSONAL', 'CATEGORY_PROMOTIONS', 'CATEGORY_SOCIAL', 'STARRED', 'UNREAD', 'Notes', 'stocks']
